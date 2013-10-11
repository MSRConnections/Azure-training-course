import numpy as np
import nitroplot as plt
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction import DictVectorizer
import random

for sheet in all_sheets():
    active_sheet(sheet)
    if Cell("A1").value == 'Carat':
        break

n = 1000 #sample size
d = [] # data

for row in CellRange("A2:D53941").table:
    d.append({'Carat': row[0], 'Cut':row[1], 'Color':row[2], 'Clarity':row[3]})

t = CellRange("E2:E53941").value # target
seed = random.random() # take matching samples from d and t
random.seed(seed)
d = random.sample(d, n)
random.seed(seed)
t = random.sample(t, n)

vec = DictVectorizer(sparse = False)
d = vec.fit_transform(d)

X, y = shuffle(d, t, random_state=13)
# X = X.astype(np.float32)
offset = int(X.shape[0] * 0.8)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

###############################################################################
# Fit regression model
params = {'n_estimators': 300, 'max_depth': 3, 'min_samples_split': 1,
          'learning_rate': 0.01, 'loss': 'ls'}
clf = ensemble.GradientBoostingRegressor(**params)

clf.fit(X_train, y_train)
mse = mean_squared_error(y_test, clf.predict(X_test))
# print("MSE: %.4f" % mse)

###############################################################################
# Plot training deviance

# compute test set deviance
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)

for i, y_pred in enumerate(clf.staged_decision_function(X_test)):
    test_score[i] = clf.loss_(y_test, y_pred)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
        label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
        label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

###############################################################################
# Plot feature importance
feature_importance = clf.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], align='center')
#raise
plt.yticks(pos, np.array(vec.get_feature_names())[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')

plot_sheet = 'ML'
if plot_sheet not in all_sheets():
    new_sheet(plot_sheet)
plt.graph(sheet = plot_sheet, scale = True, height = 0.75, width = 0.75)
display_sheet(plot_sheet)

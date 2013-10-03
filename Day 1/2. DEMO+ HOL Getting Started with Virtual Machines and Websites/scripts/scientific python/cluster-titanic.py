from azure.storage import BlobService
from sklearn.cluster import KMeans
import numpy as np
import pandas 
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.manifold import MDS

account_name = "" # REPLACE WITH YOUR ACCOUNT
account_key = "" # REPLACE WITH YOUR KEY
NUM_CLUSTERS = 16

####################################
# Get data from azure blob and write it to temp file
blob_service = BlobService(account_name, account_key)
content = blob_service.get_blob('data', 'clustering_data')
with open("tmpfile", "w") as f:
    f.write(content)

####################################
# DATA LOADING AND PREPARATION
# Load data as pandas dataframe
data = pandas.io.parsers.read_csv('tmpfile', sep=";") 
# Remove name and survived dimension to learn
names = data.pop('name')
survived = data.pop('survived')

####################################
# CLUSTERING
# Create KMeans
kmeans = KMeans(n_clusters=NUM_CLUSTERS, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None, copy_x=True, n_jobs=1)
# Train KMeans
kmeans.fit(data)

# Get the results
kmeans_labels = kmeans.labels_
kmeans_cluster_centers = kmeans.cluster_centers_
kmeans_labels_unique = np.unique(kmeans_labels)

####################################
# PLOT PREPARATION
# Reduce to two dimensions for plotting
mds = MDS(n_components=2)
mds.fit(data)
scaled_coordinates = mds.embedding_

# PLOT ON TWO DIMENSIONS
labelled_data_x = (dict(), dict())
labelled_data_y = (dict(), dict())
for label in kmeans_labels_unique:
    labelled_data_x[0][label] = []
    labelled_data_y[0][label] = []
    labelled_data_x[1][label] = []
    labelled_data_y[1][label] = []

for i in range(0, len(names)):
    label = kmeans_labels[i]
    labelled_data_x[survived[i]][label].append(scaled_coordinates[i][0])
    labelled_data_y[survived[i]][label].append(scaled_coordinates[i][1])

####################################
# PLOTTING
colors = cm.rainbow(np.linspace(0, 1, NUM_CLUSTERS))    
markers = ['x', '^']
for i in kmeans_labels_unique: 
    for j in [0, 1]:
        plt.scatter(labelled_data_x[j][i], labelled_data_y[j][i], color=colors[i], marker=markers[j], s=40)
    
plt.show()

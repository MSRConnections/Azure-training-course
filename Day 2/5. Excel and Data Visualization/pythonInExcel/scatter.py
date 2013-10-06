# scatter plot per attribute- need to sort s
# -- add color
# -- add clarity (alpha; add small 'fire' to center of each diamond - maybe rainbow ellipse?)
# -- stick histogram on top of everything

import numpy as np
import nitroplot as plt
from random import sample
from matplotlib.ticker import NullFormatter, FuncFormatter

for sheet in all_sheets():
    active_sheet(sheet)
    if Cell("A1").value == 'Carat':
        break
    
n = 10

# get data

all_data = CellRange("A2:E53941").table
data = []

for i in range(6):
    s = [x for x in all_data if i < x[0] <= i+1]
    data += sample(s, min(len(s),n))


color_to_coord = {'D':6, 'E':5, 'F':4, 'G':3, 'H':2, 'I':1, 'J':0}
coord_to_color_label = {v:k for k, v in color_to_coord.items()}

coord_to_color = {0:'#ff0000',
                  1:'#ff8800',
                  2:'#ffff00',
                  3:'#00ff00',
                  4:'#00ffff',
                  5:'#0000ff',
                  6:'#9822ff'}        

clar_to_coord = {'IF':8, 'VVS1':7, 'VVS2':6, 'VS1':5, 'VS2':4, 'SI1':3, 'SI2':2, 'I1':1}
coord_to_clar = {v:k for k, v in clar_to_coord.items()}

cut_to_coord = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Ideal': 3, 'Premium': 4}
coord_to_cut = {v:k for k, v in cut_to_coord.items()}

N = len(data)
data = zip(*data) # transpose
data[1] = [cut_to_coord[c] for c in data[1]]
data[2] = [color_to_coord[c] for c in data[2]]
data[3] = [clar_to_coord[c] for c in data[3]]
carat, cut, color, clarity, price = data

all_data = zip(*all_data)
all_data[1] = [cut_to_coord[c] for c in all_data[1]]
all_data[2] = [color_to_coord[c] for c in all_data[2]]
all_data[3] = [clar_to_coord[c] for c in all_data[3]]
#raise
area = [1000*c for c in carat]
color = [coord_to_color[c] for c in color]
clar_area = [float(c)/10 * a for c, a in zip(clarity, area)]


null = NullFormatter()

# plt.scatter(range(10), range(10), s = 500,
#             color = color_to_color.values(), alpha = 0.3)
                                                    

left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = bottom + height + 0.03

def price_format(x, pos):
    # the two args are the value and tick position
    return ('$%s,000' % (int(x/1000))) if x else ''

c_dicts = [coord_to_cut, coord_to_color_label, coord_to_clar]
def c_format(c_dict):
    def c(x):
        try:
            return c_dict[x]
        except KeyError:
            return ''
    return c

plt.figure(1, figsize = (4,8))

for i, label in enumerate(['Carat', 'Cut', 'Color', 'Clarity']):
    left_start = left + i*(width + 0.03)
    
    rect_main = [left_start, bottom, width, height]
    rect_hist = [left_start, bottom_h, width, 0.2]

    axScatter = plt.axes(rect_main)
    axHist = plt.axes(rect_hist)

    axScatter.scatter(data[i], price, s = area, c = color, alpha = 0.3)
    axScatter.scatter(data[i], price, s = clar_area, c = color, alpha = 0.5)
    axScatter.set_ylim((0, 20000))
    axScatter.set_xlabel(label)
    axScatter.minorticks_on()

    if i == 0:
        axScatter.set_ylabel('Price')
        xlim = (0, 5)
    elif i == 1:
        xlim = (-1, 5)
    elif i == 2:
        xlim = (-1, 7)
    elif i == 3:
        xlim = (0, 9)

    if i == 0:
        axHist.hist(all_data[i], log = True)
    else:
        axHist.hist(all_data[i], bins = (xlim[1] - xlim[0] - 1), log = True)

    axHist.set_ylim((10**0, 10**5))

    axScatter.set_xlim(xlim)

    if i == 0:
        axScatter.yaxis.set_major_formatter(FuncFormatter(price_format))
    else:
        axScatter.yaxis.set_major_formatter(null)
        axScatter.xaxis.set_ticklabels(map(c_format(c_dicts[i-1]),
        range(xlim[0], xlim[1] + 1)), rotation = 45)

    padding = [41, 0, 38, 21]
    axScatter.xaxis.labelpad = padding[i]

    axHist.xaxis.set_major_formatter(null)
    if i > 0:
        axHist.yaxis.set_major_formatter(null)

# price histogram
priceHist = plt.axes([left + 4*(width + 0.03) + 0.02, bottom, 0.3, height])
priceHist.set_ylim((0, 20000))
priceHist.hist(all_data[4], orientation = 'horizontal', log = True)
priceHist.yaxis.set_major_formatter(null)

plot_sheet = 'scatter'
if plot_sheet not in all_sheets():
    new_sheet(plot_sheet)
plt.graph(sheet = plot_sheet, scale = True, height = 0.6, width = 0.6)
display_sheet(plot_sheet)

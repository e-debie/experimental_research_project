import plotting_helper as plth
import numpy as np
from matplotlib import pyplot as plt
import yaml
import pathlib

plth.start(24)

path = pathlib.Path(__file__).parent.resolve()
data = yaml.safe_load(open("sediment_results.yml"))

plastics_order = data['P']
A = data['A']
B = data['B']
C = data['C']
D = data['D']
OCEAN = np.asarray(data['Ocean'])
own_test = data['OT']

production_data = data['WorldProduction']

rows = ['  ', '   ', '    ', '     ']
masses = np.asarray([14.0632, 16.5189, 14.2263, 22.3569])
volumes = [50 for i in masses]

values = np.zeros((4,len(plastics_order)))
for i,(j,k,l) in enumerate(zip(np.vstack((A,C,D,B)), masses, volumes)):
    values[i] = j*l/k
values_cum = values.cumsum(axis=1)

colours = plth.colours(len(plastics_order), colourmap='Set2')

fig, ax = plt.subplots()
ax.invert_yaxis()
ax.xaxis.set_visible(False)
ax.set_xlim(0, np.sum(values, axis=1).max())

OCEAN_cum = OCEAN.cumsum()
for i,(color,colname) in enumerate(zip(colours, plastics_order)):
    widths = OCEAN[i]
    starts = OCEAN_cum[i] - widths
    rects = ax.barh(' ', widths, left=starts, height=0.8, color=color)
    plth.start(20)
plth.start(24)

for i,(color,colname) in enumerate(zip(colours, plastics_order)):
    widths = values[:,i]
    starts = values_cum[:,i] - widths
    rects = ax.barh(rows, widths, left=starts, height=0.8,
            label=colname, color=color)
    plth.start(20)
    ax.bar_label(rects, fmt='{:.1f}', label_type='center', rotation='vertical')
plth.start(24)

plt.legend()
plt.title('Plastic distribution across depth (ng/g)')


plth.start(20)

figpies, axpies = plt.subplots(2,2)

plt.suptitle('Plastic Fractionation')

axpies[1,0].pie(A, labels=plastics_order, colors=colours, autopct='%1.1f%%')
axpies[1,0].set_title('Surface layer')

# axpies[0,1].pie(B, labels=plastics_order, colors=colours, autopct='%1.1f%%')
#
# axpies[1,0].pie(C, labels=plastics_order, colors=colours, autopct='%1.1f%%')
#
axpies[1,1].pie(D, labels=plastics_order, colors=colours, autopct='%1.1f%%')
axpies[1,1].set_title('Deepest tested layer')
#
# axpies[1,1].pie(own_test, labels=plastics_order, colors=colours, autopct='%1.1f%%')
# axpies[1,1].set_title('Own calculation')

axpies[0,1].pie(production_data, labels=plastics_order, colors=colours, autopct='%1.1f%%')
axpies[0,1].set_title('Production [4]')

axpies[0,0].pie(OCEAN, labels=plastics_order, colors=colours, autopct='%1.1f%%')
axpies[0,0].set_title('Deep ocean')

plt.show()
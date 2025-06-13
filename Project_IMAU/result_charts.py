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

production_data = data['WorldProduction']

rows = [' ', '  ', '   ', '    ']
values = np.asarray([A,C,D,B])
values_cum = values.cumsum(axis=1)

colours = plth.colours(len(plastics_order), colourmap='Set2')

fig, ax = plt.subplots()
ax.invert_yaxis()
ax.xaxis.set_visible(False)
ax.set_xlim(0, np.sum(values, axis=1).max())

for i,(color,colname) in enumerate(zip(colours, plastics_order)):
    widths = values[:,i]
    starts = values_cum[:,i] - widths
    rects = ax.barh(rows, widths, left=starts, height=0.5,
            label=colname, color=color)
plt.legend()
plt.title('Plastic distribution across depth')

fig_pie, ax_pie = plt.subplots()
ax_pie.pie(A, labels=plastics_order, colors=colours)
plt.title('Plastic fractionation in A')

fig_prod, ax_prod = plt.subplots()
ax_prod.pie(production_data, labels=plastics_order, colors=colours)
plt.title('Relevant plastic fractionation in production [BRON]')

plt.show()
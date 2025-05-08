import numpy as np
from matplotlib import pyplot as plt
import datetime as dt

data = np.loadtxt(r"D:\\DATA.TXT").T
ts = data[0]
Ts = data[1]
ps = data[2]
Hs = data[3]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

T, = ax1.plot(ts, Ts, 'r.', label='Temperature (°C)')
H, = ax1.plot(ts, Hs, 'b.', label='Relative Humidity (%)')
p, = ax2.plot(ts, ps, 'g.', label='Pressure (Pa)')

ax1.set_xlabel('Time (ms)')
plt.legend(handles=[T,H,p])
plt.show()
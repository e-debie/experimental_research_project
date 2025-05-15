import numpy as np
from matplotlib import pyplot as plt
import datetime as dt

data = np.loadtxt(r"D:\\DATA.TXT", dtype=str, skiprows=1).T
ts_unix = np.int64(data[0])
Ts = np.float64(data[3][:np.where(ts_unix==964569660)[0][0]])
ps = np.float64(data[4][:np.where(ts_unix==964569660)[0][0]])
Hs = np.float64(data[5][:np.where(ts_unix==964569660)[0][0]])

ts_datetime = np.array(data[1][:np.where(ts_unix==964569660)[0][0]]+' '+data[2][:np.where(ts_unix==964569660)[0][0]], dtype=np.datetime64)
ts_unix = ts_unix[:np.where(ts_unix==964569660)[0][0]]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

T, = ax1.plot(ts_datetime, Ts, 'r.', label='Temperature (°C)')
H, = ax1.plot(ts_datetime, Hs, 'b.', label='Relative Humidity (%)')
p, = ax2.plot(ts_datetime, ps, 'g.', label='Pressure (Pa)')

ax1.set_xlabel('Time (ms)')
plt.legend(handles=[T,H,p])
plt.show()
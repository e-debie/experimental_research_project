import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 18})

figcounter = 0
def fig_title():
    global figcounter
    figcounter += 1
    return f'Figure {figcounter}'

def run_ex2():
    phi = lambda v, R=987.4, C=10.11e-9: np.arctan(-v * R * C)
    r = 2
    c = 2


    vbounds = np.linspace(0, 2*np.pi, 1000)
    pnts = phi(vbounds)

    plt.figure()
    plt.semilogx(vbounds, pnts)
    plt.vlines(1/(r*c), min(pnts), max(pnts), linestyles='--', colors='orange')
    plt.xlabel(r'Frequency ($\omega$, arb.u.)')
    plt.ylabel(r'Phase characteristic ($\varphi$, arb.u.)')
    plt.title(fig_title())


def run_ex3():
    G = lambda v,R=9.874e3,C=10.11e-9 : np.sqrt(np.reciprocal(1+np.square(v*R*C)))
    phi = lambda v,R=9.874e3,C=10.11e-9 : np.arctan(-v*R*C)

    fs = np.asarray([.1, 1, 5, 10, 50])*1e3
    vs = fs*2*np.pi
    vs_theo = np.linspace(min(vs), max(vs), 10000)
    Vis = np.asarray([1000.2, 996.4, 995.8, 997.6, 1000.3])*1e-3
    Vus = np.asarray([989, 835.6, 298.3, 154.6, 30])*1e-3
    dts = -2*np.pi*(np.asarray([.1, 80, 40, 22, 5.7])*1e-6)/np.reciprocal(fs)
    sdts = 2*np.pi*(np.asarray([.1, 30, 5, 4, .7])*1e-6)/np.reciprocal(fs)

    VuVis = Vus/Vis

    dVuVis = np.asarray([np.sqrt(np.square(20/b) + np.square(20*a/np.abs(np.square(b)-100))) for a,b in zip(Vus, Vis)])
    print(f'Uncertainties Vu/Vi: {dVuVis}')

    plt.figure()
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(vs_theo, G(vs_theo), 'r--', label='Theoretical')
    plt.errorbar(vs, VuVis, fmt='bo', label='Practical')
    plt.legend()
    plt.xlabel(r'Angular frequency $\omega$')
    plt.ylabel(r'Amplitude response $G$')
    plt.title(fig_title())

    plt.figure()
    plt.xscale('log')
    plt.plot(vs_theo, phi(vs_theo), 'r--', label='Theoretical')
    plt.errorbar(vs, dts, sdts, fmt='bo', label='Practical')
    plt.legend()
    plt.xlabel('Angular frequency $\omega$')
    plt.ylabel('Phase response $\phi$')
    plt.title(fig_title())


def run_ex4():
    R = 9.874e3 #ohm
    C = 10.11e-9 #farad
    V0 = 1 #volt

    ts = np.asarray([32.02, 69.47, 106.5, 181.4, 255.8, 330.7, 404.7, 479.2])*1e-6
    vs = np.asarray([-443.48, 0, 302.6, 660.9, 830.2, 911.7, 950.7, 968.6])*1e-3


    Vu = lambda t, V0=V0,R=R,C=C : V0*(1-2*np.exp(-t/(R*C)))

    tbounds = np.linspace(min(ts), max(ts), 1000)
    Vus = Vu(tbounds)

    fig, ax1 = plt.subplots()
    ax1.plot(tbounds, Vus, '--', color='#7D7D7D')
    # ax2 = ax1.twinx()
    ax1.plot(ts, vs, 'o', color='#B00B1E')
    plt.xlabel('Time (V)')
    plt.ylabel('Step response (s)')
    plt.title(fig_title())

    raw_data = np.genfromtxt('A3_sq1kHz.csv', delimiter=',').T
    raw_ts = raw_data[0]
    raw_Vin = raw_data[1]
    raw_Vout = raw_data[2]

    plt.figure()
    plt.plot(raw_ts, raw_Vin, '--', color='orange', label=r'$V_\text{in}$')
    plt.plot(raw_ts, raw_Vout, '-', color='blue', label=r'$V_\text{out}$')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.title(fig_title())

run_ex4()

plt.show()
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import signal
from scipy.integrate import simps

sns.set(font_scale=1.2)

eegData = []

with open('C://Users//Anna Reithmeir//Downloads//matlabdll64//matlabdll64//Ram-Trial1-attention.csv') as dataFile:
    data = csv.reader(dataFile)
    for row in data:
        eegData.append(float(row[0]))

eegData = np.array(eegData)

Fs = 512
time = np.arange(eegData.size) / Fs

def bandpower(data, Fs, window, relative=False):

    assert(len(data) == window, "Window size mismatch. Data length: %d, Window length: %d" % (len(data), window))

    deltaBand = [0.5, 4]
    thetaBand = [4, 8]
    alphaBand = [8, 12]
    betaBand = [12, 30]
    gammaBand = [30, 49]

    window = Fs*2
    freqs, psd = signal.welch(data, Fs, nperseg=window)
    freqRes = freqs[1]-freqs[0]

    deltaBandIdx = np.logical_and(freqs >= deltaBand[0], freqs <= deltaBand[1])
    thetaBandIdx = np.logical_and(freqs >= thetaBand[0], freqs <= thetaBand[1])
    alphaBandIdx = np.logical_and(freqs >= alphaBand[0], freqs <= alphaBand[1])
    betaBandIdx = np.logical_and(freqs >= betaBand[0], freqs <= betaBand[1])
    gammaBandIdx = np.logical_and(freqs >= gammaBand[0], freqs <= gammaBand[1])
    restIdx = np.logical_not(freqs <= gammaBand[1])
    freqs[restIdx] = 0

    totalPower = simps(psd, dx=freqRes)
    deltaPower = simps(psd[deltaBandIdx], dx=freqRes)
    thetaPower = simps(psd[thetaBandIdx], dx=freqRes)
    alphaPower = simps(psd[alphaBandIdx], dx=freqRes)
    betaPower = simps(psd[betaBandIdx], dx=freqRes)
    gammaPower = simps(psd[gammaBandIdx], dx=freqRes)

    attention = thetaPower

    if relative:
        deltaPower = deltaPower / totalPower
        thetaPower = thetaPower / totalPower
        alphaPower = alphaPower / totalPower
        betaPower = betaPower / totalPower
        gammaPower = gammaPower / totalPower

    powers = [deltaPower, thetaPower, alphaPower, betaPower, gammaPower, totalPower]

    return powers

def analyze_eeg(data, window_size, window_step):

    assert(window_size >= 2, "Small window size: %d second(s). Should be >= 2 seconds." % (window_size))

    window = window_size * Fs

    delta = []
    theta = []
    alpha = []
    beta = []
    gamma = []
    total = []

    for idx in range(window, len(data)-window, window_step):

        bandpowers = bandpower(data[idx:idx+window], Fs, window, relative=True)

        delta.append(bandpowers[0])
        theta.append(bandpowers[1])
        alpha.append(bandpowers[2])
        beta.append(bandpowers[3])
        gamma.append(bandpowers[4])
        total.append(bandpowers[5])

    delta = np.array(delta)
    theta = np.array(theta)
    alpha = np.array(alpha)
    beta = np.array(beta)
    gamma = np.array(gamma)
    total = np.array(total)

    deltaLabel = 'Delta = %.2f' % delta.mean()
    thetaLabel = 'Theta = %.2f' % theta.mean()
    alphaLabel = 'Alpha = %.2f' % alpha.mean()
    betaLabel = 'Beta = %.2f' % beta.mean()
    gammaLabel = 'Gamma = %.2f' % gamma.mean()

    time = np.arange(data.size - (2 * window)) / Fs

    plt.close('all')
    fig, (ax1, ax2) = plt.subplots(nrows=2,ncols=1)

    ax1.plot(time, data[window:len(data)-window], color='b')
    ax1.set_xlabel('Time (s)', fontsize=12)
    ax1.set_ylabel('Voltage (uV)', fontsize=12)
    ax1.set_xlim([time.min(), time.max()])
    ax1.set_ylim([data.min()-100, data.max()+100])
    ax1.set_title('EEG signal', fontsize=12)

    ax2.plot(time, delta, color='r')
    ax2.plot(time, theta, color='g')
    ax2.plot(time, alpha, color='y')
    ax2.plot(time, beta, color='m')
    ax2.plot(time, gamma, color='c')
    ax2.set_xlabel('Time (s)', fontsize=12)
    ax2.set_ylabel('Power (uV^2/Hz)', fontsize=12)
    ax2.set_xlim([time.min(), time.max()])
    ax2.set_ylim([delta.min()-0.25, delta.max()+0.25])
    ax2.set_title('Spectral powers', fontsize=12)
    ax2.legend([deltaLabel, thetaLabel, alphaLabel, betaLabel, gammaLabel], loc='best', mode='expand', ncol=5, fontsize=12)

    plt.tight_layout(w_pad=0.5, h_pad=0.5)

    plt.show()

    powers = np.array([delta, theta, alpha, beta, gamma, total])

    return powers

bandpowers = analyze_eeg(eegData, 2, 1) # Window size = 2 secs = 1024 points & Window step size = 1 point = 1 ms
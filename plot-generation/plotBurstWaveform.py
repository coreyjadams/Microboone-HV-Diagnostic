from matplotlib import pyplot as plt
import numpy


def fftWire(wire):

    fft = numpy.fft.rfft(wire)
    freqs = numpy.fft.rfftfreq(len(wire), 0.5E-3)
    return freqs, numpy.absolute(fft)


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also: 

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = numpy.r_[x[window_len-1:0:-1], x, x[-1:-window_len:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = numpy.ones(window_len, 'd')
    else:
        w = eval('numpy.'+window+'(window_len)')

    y = numpy.convolve(w/w.sum(), s, mode='valid')
    return y[(window_len/2):-(window_len/2)]


def main():

    # Read in the waveforms for the 4 wires
    burst_x, burst_y = numpy.loadtxt('csv/R10203_E5225_burst_U_wire.csv',
                                     skiprows=1, delimiter=',',
                                     usecols=(0, 1),
                                     unpack=True)

    dead_x, dead_y = numpy.loadtxt('csv/R10203_E5225_burst_U_wire-dead.csv',
                                   skiprows=1, delimiter=',',
                                   usecols=(0, 1),
                                   unpack=True)

    makeWaveformPlots(burst_x, burst_y,
                      dead_x, dead_y)

    makeWaveformPlotsZoom(burst_x, burst_y,
                          dead_x, dead_y)


def makeWaveformPlots(burst_x, burst_y,
                      dead_x, dead_y):

    f, ax = plt.subplots(figsize=(20, 5))

    plt.plot(0.5*burst_x,
             burst_y,
             linewidth=2,
             label="Burst Signal")
    # plt.plot(0.5*dead_x,
    #          dead_y,
    #          linewidth=2,
    #          color='black',
    #          label="Unresponsive Wire")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    # ax.set_xlim([0.5*burst_x[3200],0.5*burst_x[3350]])

    ax.tick_params(axis='x', pad=15)
    ax.tick_params(axis='y', pad=15)

    plt.xlabel("Readout Time [us]", fontsize=20)
    plt.ylabel("ADC", fontsize=20)

    plt.legend(fontsize=30, loc='upper right')
    plt.grid(True)

    plt.tight_layout()

    plt.savefig('figures/burstWaveforms.pdf')

    plt.show()


def makeWaveformPlotsZoom(burst_x, burst_y,
                          dead_x, dead_y):

    f, ax = plt.subplots(figsize=(20, 5))

    start = 0
    end = start + 1000

    plt.plot(0.5*burst_x[start:end],
             burst_y[start:end],
             linewidth=2,
             label="Burst Signal")
    plt.plot(0.5*dead_x[start:end],
             dead_y[start:end],
             linewidth=2,
             color='black',
             label="Unresponsive Wire")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    ax.set_xlim([0.5*burst_x[start], 0.5*burst_x[end]])

    ax.tick_params(axis='x', pad=15)
    ax.tick_params(axis='y', pad=15)

    plt.xlabel("Readout Time [us]", fontsize=20)
    plt.ylabel("ADC", fontsize=20)

    plt.legend(fontsize=30, loc='upper right')
    plt.grid(True)

    plt.tight_layout()

    plt.savefig('figures/burstWaveforms_zoom.pdf')

    plt.show()


if __name__ == '__main__':
    main()

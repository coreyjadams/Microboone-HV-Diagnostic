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
    zigzag_x, zigzag_y = numpy.loadtxt('csv/zigZag-wire1991_R9767_S11.csv',
                                       skiprows=1, delimiter=',',
                                       usecols=(0, 1),
                                       unpack=True)

    normal_x, normal_y = numpy.loadtxt('csv/zigZag-wire1991_R10500_S20.csv',
                                       skiprows=1, delimiter=',',
                                       usecols=(0, 1),
                                       unpack=True)

    makeWaveformPlots(zigzag_x, zigzag_y,
                      normal_x, normal_y)
    makeFFTPlots(zigzag_y,
                 normal_y)


def makeWaveformPlots(zigzag_x, zigzag_y,
                      normal_x, normal_y):

    f, ax = plt.subplots(figsize=(16, 9))

    x = 50
    windowSize = 2*x + 1

    plt.plot(0.5*zigzag_x[3200:3350],
             zigzag_y[3200:3350],
             linewidth=2,
             label="Noise State")
    plt.plot(0.5*normal_x[3200:3350],
             normal_y[3200:3350],
             linewidth=2,
             color='black',
             label="Normal State")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    ax.set_xlim([0.5*zigzag_x[3200],0.5*zigzag_x[3350]])

    ax.tick_params(axis='x', pad=15)
    ax.tick_params(axis='y', pad=15)


    plt.xlabel("Readout Time [us]", fontsize=20)
    plt.ylabel("ADC", fontsize=20)

    plt.legend(fontsize=30,loc='upper left')
    plt.grid(True)

    plt.tight_layout()

    plt.savefig('figures/zigzagWaveforms.pdf')

    plt.show()


def makeFFTPlots(zigzag_y, normal_y):

    f, ax = plt.subplots(figsize=(16, 9))

    x = 5
    windowSize = 2*x + 1

    zigzag_x_fft, zigzag_y_fft = fftWire(zigzag_y)
    normal_x_fft, normal_y_fft = fftWire(normal_y)


    plt.semilogy(zigzag_x_fft,
             smooth(zigzag_y_fft,
                    window_len=windowSize,
                    window='flat'),
             linewidth=2,
             label="Noise State")
    plt.semilogy(normal_x_fft,
             smooth(normal_y_fft,
                    window_len=windowSize,
                    window='flat'),
             linewidth=2,
             color='black',
             label="Normal State")

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    ax.tick_params(axis='x', pad=15)
    ax.tick_params(axis='y', pad=15)


    plt.xlabel("Frequency [kHz]", fontsize=20)
    plt.ylabel("Power Spectrum [Arb.]", fontsize=20)

    plt.legend(fontsize=30,loc='upper left')
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('figures/zigzagPowerSpectrum.pdf')

    plt.show()


if __name__ == '__main__':
    main()

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas
import numpy


def calcNominal():
    df = pandas.read_csv("csv/ft1-nominal-current-draw.csv",
                         delimiter='\t',
                         skiprows=19)

    mean = numpy.mean(df['uB_OnDetPower_TPCPS_1_1_0/CURR_READ Value'])
    _max = numpy.max(df['uB_OnDetPower_TPCPS_1_1_0/CURR_READ Value'])
    _min = numpy.min(df['uB_OnDetPower_TPCPS_1_1_0/CURR_READ Value'])

    return mean, _max - _min


def main():

    # Read the file in to a pandas dataframe

    df = pandas.read_csv("csv/ft1-jan27-high-current-draw.csv",
                         delimiter='\t',
                         skiprows=28)

    df = df.rename(
        columns={'uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value':
                 'pickoffV',
                 'uB_OnDetPower_TPCPS_1_1_0/CURR_READ Value':
                 'FT1A_I'})

    df['Time'] = pandas.to_datetime(df['Time'])

    # Initialize a plot:
    f, ax = plt.subplots(figsize=(16, 9))

    daysFmt = mdates.DateFormatter('%D %H:%M')

    # Plot the pickoff voltage:
    plt.plot(df['Time'], df['FT1A_I'],
             linewidth=2, label="FT1 Asic LV")

    plt.subplots_adjust(bottom=0.17)

    ax.xaxis.set_major_formatter(daysFmt)

    mean, sigma = calcNominal()

    ax.axhspan(mean - 2*sigma, mean + 2*sigma,
               color='r', alpha=0.5, label="Nominal Range")

    plt.xlabel("Time", fontsize=20)
    # plt.plot(df['Time'],df['pickoffV'])

    ax.set_ylabel('Current Draw [A]', fontsize=20)
    # ax.tick_params('y', colors='b',width=2, size=10, labelsize=20)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        # specify integer or one of preset strings, e.g.
        # tick.label.set_fontsize('x-small')
        tick.label.set_rotation(30)
        tick.label.set_horizontalalignment('right')
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)

    ax.axvspan("01/28/17 13:15",
               "01/28/17 13:30",
               color='black', alpha=0.25)
    ax.axvspan("01/28/17 16:25",
               "01/28/17 16:40",
               color='black', alpha=0.25)
    ax.axvspan("01/29/17 9:10",
               "01/29/17 9:25",
               color='black', alpha=0.25)
    ax.axvspan("01/29/17 13:10",
               "01/29/17 13:25",
               color='black', alpha=0.25, label="FT Power Cycle")

    plt.ylim([1.5, 4])
    plt.legend(fontsize=20, loc='upper left')
    plt.grid(True)

    # plt.show()

    plt.savefig("figures/ft1-Jan27-Deviation.pdf")


if __name__ == '__main__':
    main()

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas
import numpy


def calcNominalPickoffRMS():
    df = pandas.read_csv("csv/pickoffPointNominalRMS.csv",
                         delimiter='\t',
                         skiprows=19)

    mean = numpy.mean(df['uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value'])
    _max = numpy.max(df['uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value'])
    _min = numpy.min(df['uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value'])

    return mean, _max - _min


def main():

    # Read the file in to a pandas dataframe

    df = pandas.read_csv("csv/jan27-pickoff-deviations.csv",
                         delimiter='\t',
                         skiprows=37)

    df = df.rename(columns={'uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value': 'pickoffV',
                            'uB_TPCDrift_HV01_keithleyCurrMon/getVoltage Value': 'glassmanV',
                            'uB_TPCDrift_HV01_keithleyCurrMon/calcCurrent Value': 'glassmanI'})

    df['Time'] = pandas.to_datetime(df['Time'])

    # Initialize a plot:
    f, ax = plt.subplots(figsize=(16, 9))

    daysFmt = mdates.DateFormatter('%D %H:%M')


    # Plot the pickoff voltage:
    plt.plot(df['Time'], df['pickoffV'],
             linewidth=2, label="Pickoff Point Voltage")

    plt.subplots_adjust(bottom=0.17)

    mean, rms = calcNominalPickoffRMS()

    ax.xaxis.set_major_formatter(daysFmt)


    ax.axhspan(mean - 2*rms, mean + 2*rms, color='r', alpha=0.5, label="Nominal Range")

    plt.xlabel("Time", fontsize=20)
    # plt.plot(df['Time'],df['pickoffV'])

    ax.set_ylabel('Voltage [V]', fontsize=20, color='b')
    ax.tick_params('y', colors='b',width=2, size=10, labelsize=20)
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
        # specify integer or one of preset strings, e.g.
        #tick.label.set_fontsize('x-small') 
        tick.label.set_rotation(30)
        tick.label.set_horizontalalignment('right')



    plt.ylim([-218, -203])
    plt.legend(fontsize=20,loc='upper left')
    plt.grid(True)



    ax2 = ax.twinx()
    ax2.plot(df['Time'], df['glassmanI'],
             linewidth=2, label="HV Supply Current",
             color='g')


    ax2.set_ylabel('Current [uA*]', fontsize=20, color='g')
    ax2.tick_params('y', colors='g',width=2,size=10,labelsize=20)

    ax2.set_ylim([-3,11])

    plt.legend(fontsize=20)
    # plt.show()

    plt.savefig("figures/pickoffPoint-Jan27-Deviation.pdf")


if __name__ == '__main__':
    main()

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import datetime
import pandas
import numpy
import math

pandas.options.mode.chained_assignment = None  # default='warn'




def main():

    # Read the file in to a pandas dataframe

    df = pandas.read_csv("csv/feb9_pickoff.csv",
                         delimiter='\t',
                         skiprows=46,
                         usecols=(0, 1, 6, 11, 16))

    df = df.rename(columns={'uB_OnDetPower_TPCPS_2_7_604/CURR_READ Value': 'weinerCurr',
                            'uB_OnDetPower_TPCPS_2_7_604/SenseVOLT_READ Value': 'weinerV',
                            'uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value': 'pickoffV'})

    df['Time'] = pandas.to_datetime(df['Time'])


    # daysFmt = mdates.DateFormatter('%D/%Y %H:%M')

    # fig, ax = plt.subplots(figsize=(16,9))

    # plt.subplots_adjust(bottom=0.17)

    # # plt.ylim([-5, 5])
    # plt.legend(fontsize=20,loc='upper left')
    # plt.grid(True)

    # plt.plot(df['Time'], df['weinerV'],
    #     linewidth=2,label="Weiner Voltage",
    #     color="black")

    # ax.set_ylim([-1000,300])

    # ax.set_ylabel('Applied Voltage [V]', fontsize=20, color='black')
    # ax.tick_params('y', colors='black',width=2, size=10, labelsize=20)
    

    # ax2 = ax.twinx()

    # plt.plot(df['Time'], df['pickoffV'],
    #     linewidth=2,label="Pickoff Voltage",
    #     color='green')

    
    # for tick in ax.xaxis.get_major_ticks():
    #     tick.label.set_fontsize(14) 
    #     # specify integer or one of preset strings, e.g.
    #     #tick.label.set_fontsize('x-small') 
    #     tick.label.set_rotation(30)
    #     tick.label.set_horizontalalignment('right')

    # ax2.tick_params('y', colors='g',width=2, size=10, labelsize=20)
    # ax.set_ylabel('Pickoff Voltage [V]', fontsize=20, color='g')

    # plt.xlabel("Time")

    # plt.legend(fontsize=20)
    # plt.show()

    # exit()

    # # plt.savefig("figures/pickoffPoint-Jan27-Deviation.pdf")

    # Make a plot of V vs. I:
    df['appliedV'] = -df['weinerV'].apply(round)

    appliedV = [50, 100, 200, 300, 400, 500, 600, 700, 800, 990]

    pickoffV = []
    pickoffRMS = []
    RC = []
    RC_weight = []

    for V in appliedV:
        sub_df = df.query('appliedV == {}'.format(V))
        # popt, perr = fitExponetial(sub_df, plot)

        # SteadyState value:
        pickoffV.append(numpy.mean(sub_df['pickoffV']))

        # Uncertainty:
        pickoffRMS.append(numpy.std(sub_df['pickoffV']))

    # Initialize a plot:
    f, ax = plt.subplots(figsize=(16, 9))

    appliedV = -numpy.asarray(appliedV)

    # # make a fit of the pickoff V vs applied V
    # m, b = numpy.polyfit(appliedV, pickoffV, 1)

    # xVals = numpy.arange(0, 1.2*numpy.min(appliedV), -10)
    # yVals = b + numpy.asarray(xVals)*m

    plt.errorbar(appliedV, pickoffV,  marker='o',
                 yerr=pickoffRMS,
                 # fmt='',
                 linestyle='',
                 label="Pickoff Voltage",
                 markersize=12,
                 linewidth=2,
                 color='black')
    # plt.plot(xVals, yVals,
    #          label="Linear Fit (R = {:.1f} GOhm)".format((53./m)*1e-3),
    #          linestyle='--',
    #          linewidth=3)

    plt.legend(fontsize=20, loc='upper left')
    ax.set_ylabel('Pickoff Voltage [V]', fontsize=20, color='black')
    ax.set_xlabel('Applied Voltage [V]', fontsize=20, color='black')
    ax.tick_params('y', colors='black', width=2, size=10, labelsize=20)

    plt.xlim([0, -1100])
    plt.ylim([0, -5])

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    #     # specify integer or one of preset strings, e.g.
    #     #tick.label.set_fontsize('x-small')
    #     tick.label.set_rotation(30)
    #     tick.label.set_horizontalalignment('right')

    plt.grid(True)
    # plt.savefig('figures/V-vs-I-successful.pdf')
    plt.show()


if __name__ == '__main__':
    main()

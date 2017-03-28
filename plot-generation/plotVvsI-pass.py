from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import datetime
import pandas
import numpy
import math

pandas.options.mode.chained_assignment = None  # default='warn'


from scipy import optimize


def expWrapper(x, A, B, l):
    return A - B * numpy.exp(- (1./l)*x)


def fitExponetial(_input, plot=False):

    # Get the initial time

    _input['TimeInS'] = _input['Time'].astype(numpy.int64)

    _min_time = numpy.min(_input['TimeInS'])
    # print "Lowest time is " + str(numpy.min(_input['TimeInS']))
    _input['TimeDiff'] = (_input['TimeInS'] - _min_time)*1e-9

    popt, perr = optimize.curve_fit(f=expWrapper,
                                    xdata=_input['TimeDiff'],
                                    ydata=_input['pickoffV'])

    # print "{} : {}".format(_input["appliedV"].iloc[0], popt[0])
    # print "RC: {} +/- {}".format(popt[2], numpy.sqrt(perr[2][2]))

    if plot:

        fig, ax = plt.subplots(figsize=(16, 9))

        line0, = plt.plot(_input['TimeDiff'],
                          _input["pickoffV"],
                          label="Pickoff Voltage",
                          marker='o',
                          # fillstyle='none',
                          markersize=5,
                          linewidth=0,
                          color='black')
        xVals = numpy.asarray(_input['TimeDiff'])
        yVals = expWrapper(xVals, popt[0], popt[1], popt[2])
        line1, = plt.plot(xVals, yVals,
                          label="Exponential Fit (RC = {:.1f}s)".format(
                              popt[2]),
                          linestyle='--',
                          linewidth=3,
                          color='red')

        extraString = 'Applied Voltage: -{}V'.format(_input['appliedV'].iloc[0])
        handles, labels = ax.get_legend_handles_labels()
        handles.append(mpatches.Patch(color='none', label=extraString))
        plt.legend(handles=handles, fontsize=20)

        plt.xlabel("Time [s]", fontsize=20)
        plt.ylabel("Pickoff V [V]", fontsize=20)

        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(20)
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(20)
        #     # specify integer or one of preset strings, e.g.
        #     #tick.label.set_fontsize('x-small')
        #     tick.label.set_rotation(30)
        #     tick.label.set_horizontalalignment('right')

        plt.grid(True)
        # plt.show()
        # print 'figures/RC-Pickoff-{}.pdf'.format(_input['appliedV'].iloc[0])
        plt.savefig(
            'figures/RC-Pickoff-{}.pdf'.format(_input['appliedV'].iloc[0]))
        plt.close()

    return popt, perr


def main():

    # Read the file in to a pandas dataframe

    df = pandas.read_csv("csv/Feb24-V-vs-I-success.csv",
                         delimiter='\t',
                         skiprows=39,
                         nrows=2976)

    df = df.rename(columns={'uB_OnDetPower_TPCPS_2_7_604/CURR_READ Value': 'weinerCurr',
                            'uB_OnDetPower_TPCPS_2_7_604/SenseVOLT_READ Value': 'weinerV',
                            'uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value': 'pickoffV'})

    df['Time'] = pandas.to_datetime(df['Time'])

    daysFmt = mdates.DateFormatter('%D %H:%M')

    # plt.subplots_adjust(bottom=0.17)

    # plt.ylim([-5, 5])
    # plt.legend(fontsize=20,loc='upper left')
    # plt.grid(True)

    # ax2 = ax.twinx()

    # plt.plot(df['Time'], df['weinerV'],
    #     linewidth=2,label="Weiner Voltage")

    # # ax2.set_ylabel('Current [uA*]', fontsize=20, color='g')
    # # ax2.tick_params('y', colors='g',width=2,size=10,labelsize=20)

    # ax2.set_ylim([-1100,100])

    # plt.legend(fontsize=20)
    # plt.show()

    # # plt.savefig("figures/pickoffPoint-Jan27-Deviation.pdf")

    # Make a plot of V vs. I:
    df['appliedV'] = -df['weinerV'].apply(round)

    appliedV = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    pickoffV = []
    pickoffRMS = []
    RC = []
    RC_weight = []

    for V in appliedV:
        sub_df = df.query('appliedV == {}'.format(V))
        if V == 1000:
            plot = True
        else:
            plot = True
        popt, perr = fitExponetial(sub_df, plot)

        # SteadyState value:
        pickoffV.append(popt[0])

        # Uncertainty:
        pickoffRMS.append(numpy.sqrt(perr[0][0]))

        RC.append(popt[2])
        RC_weight.append(1./numpy.sqrt(perr[2][2]))

    # Initialize a plot:
    f, ax = plt.subplots(figsize=(16, 9))


    appliedV = -numpy.asarray(appliedV)

    # make a fit of the pickoff V vs applied V
    m, b = numpy.polyfit(appliedV, pickoffV, 1)

    xVals = numpy.arange(0, 1.2*numpy.min(appliedV), -10)
    yVals = b + numpy.asarray(xVals)*m

    plt.plot(appliedV, pickoffV,  marker='o',
             label="Pickoff Voltage",
             markersize=12,
             linewidth=0,
             color='black')
    plt.plot(xVals, yVals,
             label="Linear Fit (R = {:.1f} GOhm)".format((53./m)*1e-3),
             linestyle='--',
             linewidth=3)

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

    # Next, fit the average RC constant:
    RC_average = numpy.average(RC, weights = RC_weight)
    print "RC Average is {}".format(RC_average)

    plt.grid(True)
    plt.savefig('figures/V-vs-I-successful.pdf')
    plt.show()


if __name__ == '__main__':
    main()

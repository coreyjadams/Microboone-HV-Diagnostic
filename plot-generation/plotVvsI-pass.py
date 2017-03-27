from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime
import pandas
import numpy
import math

pandas.options.mode.chained_assignment = None  # default='warn'


from scipy import optimize


def expWrapper(x, A, B, l):
    return A - B * numpy.exp(- l * x)

def fitExponetial(_input):

    # Get the initial time

    _input['TimeInS'] = _input['Time'].astype(numpy.int64)

    _min_time = numpy.min(_input['TimeInS'])
    # print "Lowest time is " + str(numpy.min(_input['TimeInS']))
    _input['TimeDiff'] = (_input['TimeInS'] - _min_time)*1e-9

    popt, perr = optimize.curve_fit(f = expWrapper,
                                    xdata = _input['TimeDiff'],
                                    ydata = _input['pickoffV'])


    print "{} : {}".format(_input["appliedV"].iloc[0], popt[0])

    # fig, ax = plt.subplots()

    # plt.plot(_input['TimeDiff'], _input["pickoffV"])
    # xVals = numpy.asarray(_input['TimeDiff'])
    # yVals = expWrapper(xVals, popt[0], popt[1], popt[2])
    # plt.plot(xVals, yVals)

    # ax2 = ax.twinx()
    # plt.plot(_input['TimeDiff'], _input["appliedV"])


    # plt.grid(True)
    # plt.show()


    return popt, perr


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

    df = pandas.read_csv("csv/Feb24-V-vs-I-success.csv",
                         delimiter='\t',
                         skiprows=39,
                         nrows=2976)

    df = df.rename(columns={'uB_OnDetPower_TPCPS_2_7_604/CURR_READ Value': 'weinerCurr',
                            'uB_OnDetPower_TPCPS_2_7_604/SenseVOLT_READ Value': 'weinerV',
                            'uB_TPCDrift_HV01_keithleyPickOff/getVoltage Value': 'pickoffV'})

    df['Time'] = pandas.to_datetime(df['Time'])

    # Initialize a plot:
    f, ax = plt.subplots(figsize=(16, 9))

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

    for V in appliedV:
        sub_df = df.query('appliedV == {}'.format(V))
        popt, perr = fitExponetial(sub_df)


        # SteadyState value:
        pickoffV.append(popt[0])

        # Uncertainty:
        pickoffRMS.append(numpy.sqrt(perr[0][0]))


    print appliedV
    print pickoffV
    print pickoffRMS


    plt.errorbar(appliedV, pickoffV, yerr=pickoffRMS, xerr=None, fmt='o')

    ax.set_ylabel('Pickoff Voltage [V]', fontsize=20, color='black')
    ax.set_xlabel('Applied Voltage [V]', fontsize=20, color='black')
    ax.tick_params('y', colors='black', width=2, size=10, labelsize=20)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    #     # specify integer or one of preset strings, e.g.
    #     #tick.label.set_fontsize('x-small')
    #     tick.label.set_rotation(30)
    #     tick.label.set_horizontalalignment('right')

    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()

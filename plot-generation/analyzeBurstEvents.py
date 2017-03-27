import sys

import ROOT
import larlite
import numpy
from matplotlib import pyplot as plt

if len(sys.argv) < 2:
    msg = '\n'
    msg += "Usage 1: %s $INPUT_ROOT_FILE\n" % sys.argv[0]
    msg += '\n'
    sys.stderr.write(msg)
    sys.exit(1)

from ROOT import larlite, evd


# Create ana_processor instance
# my_proc = larlite.ana_processor()

# Set input root file
# for x in xrange(len(sys.argv)-1):
# my_proc.add_input_file(sys.argv[x+1])


# Specify IO mode
# my_proc.set_io_mode(larlite.storage_manager.kREAD)

# Specify analysis output root file name
# my_proc.set_ana_output_file("showerRecoUboone_ana.root")
# Specify data output root file name
# my_proc.set_output_file("noneOutput.root")


ana_unit = evd.DrawUbSwiz()
ana_unit.setInput(sys.argv[-1])


ana_unit.setYDimension(9600, 0)
ana_unit.setYDimension(9600, 1)
ana_unit.setYDimension(9600, 2)


ana_unit.initialize()
ana_unit.SetCorrectData(False)
ana_unit.SetSaveData(False)
ana_unit.SetStepSizeByPlane(48, 0)
ana_unit.SetStepSizeByPlane(48, 1)
ana_unit.SetStepSizeByPlane(96, 2)

# ana_unit.goToEvent(0)
# ana_unit.goToEvent(1)
ana_unit.goToEvent(6)


_u_plane = ana_unit.getArrayByPlane(0)
_v_plane = ana_unit.getArrayByPlane(1)
_y_plane = ana_unit.getArrayByPlane(2)

# Plot the max value of the event as a function of wire:


_max_values_u = numpy.max(_u_plane, axis=1) / 2400.
_max_values_v = numpy.max(_v_plane, axis=1) / 2400.
_max_values_y = numpy.max(_y_plane, axis=1) / 3600.


f, ax = plt.subplots(figsize=(20, 10))

start = 0
end = start + 1000

plt.plot(numpy.arange(0, 2400, 1),
         _max_values_u,
         linewidth=2,
         label="Max ADC, U")
plt.plot(numpy.arange(0, 2400, 1),
         _max_values_v,
         linewidth=2,
         label="Max ADC, V")
plt.plot(numpy.arange(0, 3456, 1),
         _max_values_y,
         linewidth=2,
         label="Max ADC, Y")

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(20)
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(20)

# ax.set_xlim([0.5*burst_x[start], 0.5*burst_x[end]])

ax.tick_params(axis='x', pad=15)
ax.tick_params(axis='y', pad=15)

plt.xlabel("Wire Number", fontsize=20)
plt.ylabel("Fraction of Max. ADC", fontsize=20)

plt.legend(fontsize=30, loc='upper right')
plt.grid(True)

plt.tight_layout()

# plt.savefig('figures/burstWaveforms_zoom.pdf')

plt.show()

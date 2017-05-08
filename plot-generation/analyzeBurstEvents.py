import sys

import ROOT
import larlite
import numpy
from matplotlib import pyplot as plt

from ROOT import evd

_pre_fix_file = "/data/uboone/pulser_data/Feb24-pulser/PhysicsRun-2017_2_24_9_58_26-0010239-00001_20170226T201136_ext_unbiased_20170227T012225_merged.root"
_post_fix_file = "/data/uboone/pulser_data/Feb24-pulser/PhysicsRun-2017_2_24_9_58_26-0010239-00018_20170226T201020_ext_unbiased_20170227T012640_merged.root"



ana_unit_pre = evd.DrawUbSwiz()
ana_unit_pre.setInput(_pre_fix_file)


ana_unit_pre.setYDimension(9600, 0)
ana_unit_pre.setYDimension(9600, 1)
ana_unit_pre.setYDimension(9600, 2)
ana_unit_pre.initialize()
ana_unit_pre.SetCorrectData(False)
ana_unit_pre.SetSaveData(False)
ana_unit_pre.SetStepSizeByPlane(48, 0)
ana_unit_pre.SetStepSizeByPlane(48, 1)
ana_unit_pre.SetStepSizeByPlane(96, 2)
ana_unit_pre.goToEvent(0)


ana_unit_post = evd.DrawUbSwiz()
ana_unit_post.setInput(_post_fix_file)
ana_unit_post.setYDimension(9600, 0)
ana_unit_post.setYDimension(9600, 1)
ana_unit_post.setYDimension(9600, 2)
ana_unit_post.initialize()
ana_unit_post.SetCorrectData(False)
ana_unit_post.SetSaveData(False)
ana_unit_post.SetStepSizeByPlane(48, 0)
ana_unit_post.SetStepSizeByPlane(48, 1)
ana_unit_post.SetStepSizeByPlane(96, 2)
ana_unit_post.goToEvent(0)


_u_plane_pre = ana_unit_pre.getArrayByPlane(0)
# _v_plane = ana_unit.getArrayByPlane(1)
# _y_plane = ana_unit.getArrayByPlane(2)


_u_plane_post = ana_unit_post.getArrayByPlane(0)

# Plot the max value of the event as a function of wire:



_max_values_u_pre = numpy.max(_u_plane_pre, axis=1)
_max_values_u_post = numpy.max(_u_plane_post, axis=1)
# _max_values_v = numpy.max(_v_plane, axis=1) / 2400.
# _max_values_y = numpy.max(_y_plane, axis=1) / 3600.


f, ax = plt.subplots(figsize=(20, 10))

start = 0
end = start + 1000

plt.plot(numpy.arange(0, 2400, 1),
         _max_values_u_pre / _max_values_u_post,
         linewidth=2,
         label="Max ADC, U")
# plt.plot(numpy.arange(0, 2400, 1),
#          _max_values_v,
#          linewidth=2,
#          label="Max ADC, V")
# plt.plot(numpy.arange(0, 3456, 1),
#          _max_values_y,
#          linewidth=2,
#          label="Max ADC, Y")

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

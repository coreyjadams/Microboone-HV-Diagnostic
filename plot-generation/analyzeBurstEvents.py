import sys

import ROOT
import larlite
import numpy

if len(sys.argv) < 2:
    msg  = '\n'
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



ana_unit=evd.DrawUbSwiz()
ana_unit.setInput(sys.argv[-1])


ana_unit.setYDimension(9600,0);
ana_unit.setYDimension(9600,1);
ana_unit.setYDimension(9600,2);


ana_unit.initialize()
ana_unit.SetCorrectData(False)
ana_unit.SetSaveData(False)
ana_unit.SetStepSizeByPlane(48,0)
ana_unit.SetStepSizeByPlane(48,1)
ana_unit.SetStepSizeByPlane(96,2)

# ana_unit.goToEvent(0)
# ana_unit.goToEvent(1)
ana_unit.goToEvent(6)


_u_plane = ana_unit.getArrayByPlane(0)

# Plot the max value of the event as a function of wire:

print _u_plane.shape

_max_values_u = numpy.max(_u_plane, axis=1)
print _max_values_u.shape


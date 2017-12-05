from AmplOutputReader import AmplOutputReader
from AmplDataWriter import AmplDataWriter

# read the config file and write to ampl model
adw = AmplDataWriter(True)
adw.writeDatFile("testFile.dat")



# ( solve the model inside python )
# run ampl script

# read and print the results
#amplOut = '/home/oskar/Desktop/Xsol.out'
#AOR = AmplOutputReader(amplOut)
#AOR.readAmplOutput()

from AmplOutputReader import AmplOutputReader

# Write to config file

# run ampl script

# read and print the results
amplOut = '/home/oskar/Desktop/Xsol.out'
AOR = AmplOutputReader(amplOut)
AOR.readAmplOutput()

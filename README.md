# SSY226

/ampl contains optimization models in AMPL format(.dat, .mod and .run)


## To start optimizing:
modify the `modelspec.py` with desired parameters  
create the `testFile.dat`: running `python3 Initatior.py` (Python 3.5.x needed)
load the `testFile.dat` to `ampl/task2` model using:
`ampl: include task2.run;`

  
##
AmplDataWriter reads layout data files and prints into a AMPL friendly format. 
AmplDataWriter requires both TaskReader and PointPlotter

PointPlotter reads layout data and plots it

TaskReader reads task data

TODO: Divide PointPlotter into PointReader and PointPlotter.

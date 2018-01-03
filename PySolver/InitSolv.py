from ModelSpecParser import *
from Model2 import *

pickle_file = 'model1.pickle'

ModelSpecParser.parse(pickle_file) #generate a pickle file and store it
Model2.load(pickle_file) #load pickle file and the dataset
Model2.init() #run the optimizer
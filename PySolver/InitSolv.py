from ModelSpecParser import *
from Model2 import *
import time


pickle_file = 'model1.pickle'

print('Generating layout...')
ModelSpecParser.parse(pickle_file) #generate a pickle file and store it

print('Parsing pickled data...')
Model2.load(pickle_file) #load pickle file and the dataset

print('Solving...')
a = time.perf_counter()
Model2.solve() #run the optimizer
b = time.perf_counter()
print('--- Solver time used: [s]', round(b-a,8), ' ---')
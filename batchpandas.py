import os
import pandas as pd
from numpy import *
import glob
from mypandas import mypandas

filenames = glob.glob('*.txt')
# Initialize some variables
skiprows = 6

for filename in filenames:
    # customize the header
	names = ['Ppt_group', 'Ppt_No', 'Block_Name', 'Trial_Name', 'Trial_No', 'CumulativeT', 'Ppt_re', 'Input', 'Error_Code', 'RT', 'SOA', 'Operation', 'OpType', 'order', 'Lvalue', 'Rvalue']
	# read in data from files
	data = pd.read_csv(filename, sep = '\t', skiprows = skiprows, names = names)
	filename = open(os.path.join('playground/', filename), 'w+')
	mypandas(data).to_csv(filename, sep = '\t', index = False)

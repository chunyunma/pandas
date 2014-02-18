import os
import pandas as pd
import numpy as np
import glob
from mypandas import mypandas
import pdb

filenames = glob.glob('*.txt')
# Initialize some variables
skiprows = 6
dfs = []

for filename in filenames:
	PptNo = filename.split('.')[0]
    # customize the header
	names = ['Ppt_group', 'Ppt_No', 'Block_Name', 'Trial_Name', 'Trial_No', 'CumulativeT', 'Ppt_re', 'Input', 'Error_Code', 'RT', 'SOA', 'Operation', 'OpType', 'order', 'Lvalue', 'Rvalue']
	# read in data from files
	data = pd.read_csv(filename, sep = '\t', skiprows = skiprows, names = names)
	filename = open(os.path.join('playground/', filename), 'w+')
	dataS = mypandas(data)
	grouped = dataS.groupby(['Operation', 'SOA'])
	df = grouped.RT.aggregate(np.mean)
# 	pdb.set_trace()
	dfs.append(df)
	dataS.to_csv(filename, sep = '\t', index = False)

df = pd.concat(dfs, axis = 1)
df.to_csv('total.csv', sep = '\t', index = False)
	

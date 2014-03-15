import os
import pandas as pd
import numpy as np
import glob
from mypandas import mypandas
import pdb

filenames = glob.glob('*.txt')
# Initialize some variables
skiprows = 6
names = ['Ppt_group', 'Ppt_No', 'Block_Name', 'Trial_Name', 'Trial_No', 'CumulativeT', \
'Ppt_re', 'Input', 'Error_Code', 'RT', 'SOA', 'Operation', 'OpType', 'order', 'Lvalue', 'Rvalue']
dfs = []    # create an empty list
dferr = pd.DataFrame()    # create an empty dataframe for storing incorrect trials
lengths = {}    # create an empty dic for storing total trial numbers

for filename in filenames:
	PptNo = filename.split('.')[0]
    # customize the header
	# read in data from files
	data = pd.read_csv(filename, sep = '\t', skiprows = skiprows, names = names)
	filename = open(os.path.join('result/', filename), 'w+')
	dataS, len_TF, len_ol = mypandas(data)
# 	pdb.set_trace()
	lengths[PptNo] = (len_TF, len_ol)    # add "PptNo: len" as "key: value" in the dict
# 	separate incorrect trails together with their adjacent ones
# 	for index, value in dataS.TF.iteritems():
# 		if value == False:
# 			if index == 0:
# 				dferr = dferr.append(dataS.iloc[index:index+2])
# 			elif index == 339:
# 				dferr = dferr.append(dataS.iloc[index-1:index+1])
# 			else:
# 				dferr = dferr.append(dataS.iloc[index-1:index+2])
# 				
# 	dferr = dferr.append(dataS[dataS.TF == False])    # separate incorrect trials
	grouped = dataS[dataS.Outlier == False].groupby(['Operation', 'SOA'])    # Calculate mean for correct & non-outlier trials only
	df = grouped.RT.aggregate(np.mean)
	df = pd.DataFrame(df)    # convert a series-type of data to dataframe so I can tag the column using "rename()"
# 	pdb.set_trace()
	df = df.rename(columns = {'RT':PptNo})    # tag the column with participant Num.
	dfs.append(df)    # append each dataframe into the list
# 	dataS.to_csv(filename, sep = '\t', index = False)

df = pd.concat(dfs, axis = 1)    # concatenate elements (dataframes) in dfs
df = df.transpose()
df.to_csv('total.txt', sep = '\t')    # 2 by 3 within ANOVA data
# dflen = pd.DataFrame.from_dict(lengths, orient = 'index')    # how many trials are correct, non-outliers
# dflen.to_csv('lengths.txt', sep = '\t')
# dferr.to_csv('errors.txt', sep = '\t', index = True, cols = ['Ppt_group', 'Ppt_No', 'Block_Name', \
# 'Trial_Name', 'Trial_No', 'CumulativeT', 'RT', 'SOA', 'Operation', 'OpType', 'order', 'Lvalue', \
# 'Rvalue', 'Answer', 'Key', 'TF', 'SelfCorr', 'EarlyFire', 'Marked', 'StrAnswer'])
# to_csv does not preserve the column order, so I specify it with "cols ="
	

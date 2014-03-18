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
dfs_omnibus = []    # create an empty list for omnibus ANOVA
dfs_RTbyProb = []    # create another empty list to store median RT for each problem
# dferr = pd.DataFrame()    # create an empty dataframe for storing incorrect trials
dfs_err_by_prob = []    # create an empty list for storing incorrect answers by problem
dfs_count_err_by_prob = []    # create an empty list for storing incorrect trial counts by problem
lengths = {}    # create an empty dict for storing total trial numbers

for filename in filenames:
	dict_count_err = {}    # initialize an empty dict for storing error counts by problem
	dict_err = {}    # initialize an empty dict for storing incorrect answers by problem

	PptNo = filename.split('.')[0]
    # customize the header
	# read in data from files
	data = pd.read_csv(filename, sep = '\t', skiprows = skiprows, names = names)
# 	filename = open(os.path.join('result/', filename), 'w+')    # turn this on/off to generate individual clean data file (1/2)
	dataS, len_TF, len_ol = mypandas(data)    # dataS[imple]--restructured data
# 	pdb.set_trace()
# 	lengths[PptNo] = (len_TF, len_ol)    # add "PptNo: len" as "key: value" in the dict; used as (one) criterion for outliers

# 	separate incorrect trails together with their adjacent ones
# 	for index, value in dataS.TF.iteritems():
# 		if value == False:
# 			if index == 0:
# 				dferr = dferr.append(dataS.iloc[index:index+2])
# 			elif index == 339:
# 				dferr = dferr.append(dataS.iloc[index-1:index+1])
# 			else:
# 				dferr = dferr.append(dataS.iloc[index-1:index+2])
			
# 	dferr = dferr.append(dataS[dataS.Block_Name.str.contains('block') & dataS.TF == False])    # separate incorrect trials

	# This was the first attempt when I tried to look at errors per problem; unsuccessful; multiindex caused trouble in concatenation
# 	df_err_by_prob = dataS[dataS.Block_Name.str.contains('block') & dataS.TF == False]
# 	df_err_by_prob = df_err_by_prob[['Operation','SOA','Lvalue','Rvalue','StrAnswer']]
# 	df_err_by_prob = df_err_by_prob.set_index(['Operation','SOA','Lvalue','Rvalue'])
# 	df_err_by_prob = df_err_by_prob.rename(columns = {'StrAnswer':PptNo})
# 	pdb.set_trace()
# 	dfs_err_by_prob.append(df_err_by_prob)
		
	# tablet incorrect trials by problem
	err_by_prob = dataS[dataS.Block_Name.str.contains('block')].groupby(['Operation','SOA','Lvalue','Rvalue'])    # ignore practice trials
	for key, group in err_by_prob:
		dict_count_err[key] = len(group[group.TF == False])    # count number of incorrect trials per problem	
		dict_err[key] = pd.Series.max(group[group.TF == False].StrAnswer)    # errors by problem; this line is a workaround
		# see log of Week of 2014-03-17, Tuesday, for a fuller explanation
# 		pdb.set_trace()
# 	pdb.set_trace()
	df_count_err_by_prob = pd.DataFrame.from_dict(dict_count_err, orient = 'index')
	df_count_err_by_prob.columns = [PptNo]    # assign PptNo to column name
	dfs_count_err_by_prob.append(df_count_err_by_prob)
	
	df_err_by_prob = pd.DataFrame.from_dict(dict_err, orient = 'index')
	df_err_by_prob.columns = [PptNo]    # assign PptNo to column name
	dfs_err_by_prob.append(df_err_by_prob)
	
	# prepare data for omnibus ANOVA
# 	grouped = dataS[dataS.Outlier == False].groupby(['Operation', 'SOA'])    # Calculate mean for correct & non-outlier trials only
# 	df = grouped.RT.aggregate(np.mean)
# 	df = pd.DataFrame(df)    # convert a series-type of data to dataframe so I can tag the column using "rename()"
# 	df = df.rename(columns = {'RT':PptNo})    # tag the column with participant Num.
# 	pdb.set_trace()
# 	dfs_omnibus.append(df)    # append each dataframe into the list
	
	# Calculate median RT for each problem
# 	group_by_prob = dataS[dataS.Block_Name.str.contains('block') & dataS.TF & (dataS.Marked == False)].groupby(['Operation','SOA','Lvalue','Rvalue'])
# 	df = group_by_prob.RT.aggregate(np.median)
# 	df = pd.DataFrame(df)
# 	df = df.rename(columns = {'RT': PptNo})
# 	dfs_RTbyProb.append(df)
	
# 	dataS.to_csv(filename, sep = '\t', index = False)    # turn this on/off to generate individual clean data file (2/2)


# df = pd.concat(dfs_omnibus, axis = 1)    # concatenate elements (dataframes) in dfs_omnibus
# df = df.transpose()
# df.to_csv('total.txt', sep = '\t')    # prepare 2-by-3 within ANOVA data

# df = pd.concat(dfs_RTbyProb, axis = 1)    # concatenate elements (dataframes) in dfs_RTbyProb
# df.to_csv('RTbyProb.txt', sep = '\t')

# df = pd.concat(dfs_count_err_by_prob, axis = 1)
# df.to_csv('CountErrorByProb.txt', sep = '\t')

# df = pd.concat(dfs_err_by_prob, axis = 1)
# df.to_csv('ErrorByProb.txt', sep = '\t')

# dflen = pd.DataFrame.from_dict(lengths, orient = 'index')    # how many trials are correct, non-outliers
# dflen.to_csv('lengths.txt', sep = '\t')    # turn this on/off
# dferr.to_csv('errors.txt', sep = '\t', index = True, cols = ['Ppt_group', 'Ppt_No', 'Block_Name', \
# 'Trial_Name', 'Trial_No', 'CumulativeT', 'RT', 'SOA', 'Operation', 'OpType', 'order', 'Lvalue', \
# 'Rvalue', 'Answer', 'Key', 'TF', 'SelfCorr', 'EarlyFire', 'Marked', 'StrAnswer'])
# to_csv does not preserve the column order, so I specify it with "cols ="
	

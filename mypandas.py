import pandas as pd
from numpy import *
import mypandasplot
# import matplotlib.pyplot as plt

def mypandas(data):
	# Add a few more columns. Do not use data.Answer = ''. The dot operator is only available once the column has been created
	data['Answer'] = ''    # Response from participants
	data['Key'] = ''    # Answer key for each arithmetic 
	data['TF'] = ''    # Boolean. If participants reported correct answer.
	data['SelfCorr'] = ''    # Boolean. If participants corrected themselves after reporting a wrong answer
	data['EarlyFire'] = ''    # Boolean. If voice key was triggered before participants responded.
	data['Marked'] = ''     # marking trials that have invalid RT (SelfCorr or EarlyFire)
	data['StrAnswer'] = ''    # response from participants stripped of the trailing markers

	# extract left and right operands from the last two digits of "Trial Name" and force type int8
	data.Lvalue = data.Trial_Name.str.get(-1).astype('int8')
	data.Rvalue = data.Trial_Name.str.get(-2).astype('int8')

	# Calculate the answer key for each trial
	for op, group in data.groupby('Operation'):
		if op == 'add':
			group.Key = group.Lvalue + group.Rvalue
			data.update(group)
		elif op == 'multiply':
			group.Key = group.Lvalue * group.Rvalue
			data.update(group)

	# copy and past the solution by participants from 'Input' to a new column--'Answer'
	for index, value in data.Input.iteritems():
		if value is not NaN:    # NaN is from NumPy namespace
			data.ix[index-1, 'Answer'] = value
		else:
			continue


	data.SelfCorr = data.Answer.str.contains('/')
	pattern = r"[0-9]+[*]$"    # cannot directly use '*' within contains()
	data.EarlyFire = data.Answer.str.contains(pattern)
	data.Marked = data.SelfCorr | data.EarlyFire

	# Strip the trailing "/" or "*" from the responses from Ppts
	# "str" may raise errors if the cell is empty, so I used a subset of the dataframe
	for marker, group in data[-pd.isnull(data.Answer)].groupby('Marked'):
		if marker:
			group.StrAnswer = group.Answer.str[:-1]
			data.update(group)
		
		else:
			group.StrAnswer = group.Answer
			data.update(group)

	# filter out duplicate rows		
	data = data[data.index%2 == 0]

	#transform the two columns to float type, so that they can be compared with "=="
	data[['Key', 'StrAnswer']] = data[['Key', 'StrAnswer']].convert_objects(convert_numeric = True)
	data.TF = (data.Key == data.StrAnswer)
	
	# flag outliers
	data = mypandasplot.mypandasbp(data)

	return data
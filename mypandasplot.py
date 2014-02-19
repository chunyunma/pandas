import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
import pdb

# Use this if reading data from external files.
# skip practice trials. 
# data = pd.read_csv('data.txt', sep = '\t', header = 0, skiprows = [1,2,3,4,5,6,7,8,9,10])

def mypandasbp(data):
	# filter out practice trials
	data = data[data.Block_Name.str.contains('block')]
	# select trials with correct and timely response
	data = data[data.TF & (data.Marked == False)]
	
	data['Outlier'] = ''    # boolean variable. 1 = outlier

	for condition, df in data.groupby(['Operation', 'SOA']):
		bp = plt.boxplot(df.RT.values, whis = 3)    # only identify outliers outside of 3IQR, emulating what SPSS does. The tricky part is "RT.values". Normally, df.RT should work with boxplot. But in this case, it kept raising KeyError. Series.values return series as an ndarray
# 		bp = plt.boxplot(df.RT.values)    # default, 1.5IQR
		top_points = bp["fliers"][0].get_data()[1]    # outliers above upper fence
		bottom_points = bp["fliers"][1].get_data()[1]    # outliers below lower fence
		
		if len(top_points) == 0 and len(bottom_points) == 0:
			df.Outlier = 1<1    # if no outliers, fill with False
			data.update(df)
		elif len(top_points) > 0 and len(bottom_points) > 0:
# 			pdb.set_trace()
			bottom_points = sorted(bottom_points, reverse=True)    # use sorted() instead of sort to accommodate lists with only one element
			top_points.sort()    # in-place sort
			df.Outlier = (df.RT <= bottom_points[0]) | (df.RT >= top_points[0])    # boolean
			data.update(df)
		elif len(top_points) == 0 and len(bottom_points) > 0:
			bottom_points = sorted(bottom_points, reverse=True)
			df.Outlier = df.RT <= bottom_points[0]
			data.update(df)
		else:
# 			pdb.set_trace()
			top_points.sort()
			df.Outlier = (df.RT >= top_points[0])
			data.update(df)	
# 	pdb.set_trace()
	return data

# export to csv if using this module along
# data.to_csv('playground/data.txt', sep = '\t', index = False)

# pandas also has data.boxplot(). But it does not return a dictionary like plt.boxplot(df). http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.boxplot
# bp = data.boxplot(column = 'RT', by = ['Operation', 'SOA'])
# plt.show()


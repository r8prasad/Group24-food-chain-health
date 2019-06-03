"""
Created on Sun June 2 2019

@author: adnan
"""

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import subplots
def threshold_on_metric(df, columns_filter, thresh_info):
	assert isinstance(df, pd.DataFrame)
	assert isinstance(columns_filter, list) and len(columns_filter)>0
	assert isinstance(thresh_info, dict) and len(thresh_info) == len(columns_filter)-1
	# Add Final_Score column to dataframe
	df['Final_Score'] = 0.0

	# Thresholding on metrics
	for metric in columns_filter[1:]:
		# Retrieving thresholding information
		thresh = thresh_info[metric][0]
		flip_logic = thresh_info[metric][1]
		# Thresholding each metrics
		df[metric] = (df[metric] > thresh) * 1 #converting True/False to 1/0
		df[metric] = (2*df[metric] - 1) * flip_logic #converting 1/0 to 1/-1 and then flipping the logic if needed
		# Calculating final score based on threholded metric value
		df['Final_Score'] += df[metric]
	return df

def main():
	
	# Initializations
	data_folder = '../Final_CSV'
	extra_str = ''
	ext = '.csv'
	columns_filter = ['Item', 'Carbs Metric', 'Fat Metric', 'Cholesterol Metric', 'Protein Metric']
	thresh_info = {	'Carbs Metric': [1.0, 1],
						'Fat Metric': [1.0, -1],
						'Cholesterol Metric': [1.0, -1],
						'Protein Metric': [1.0, 1]}
	assert len(columns_filter)-1 == len(thresh_info), 'Number of metrics mismatch'
	# Getting names of restaurants
	restaurant_names = os.listdir(data_folder)
	restaurant_names = [name.split('.')[0] for name in restaurant_names]
	assert len(restaurant_names) > 0, 'Need to have atleast one restaurant csv file!'

	# restaurant_names = ['BurgerKing']
	fig, axs = plt.subplots(3, 5, figsize=(14, 6), sharey=True)
	fig.subplots_adjust(hspace = .5, wspace=.2)
	axs = axs.flatten()
	for i in range(0,len(restaurant_names)):
		# Reading the csv file and storing as DataFrame
		restaurant = restaurant_names[i]
		print('Processing info from restaurant - ', restaurant)
		df = pd.read_csv(data_folder+'/'+restaurant+extra_str+ext, encoding = 'iso-8859-1') 
		# Selecting columns with metrics only
		df = df[columns_filter]
		# Thresholding all metrics based on thresh_info
		df = threshold_on_metric(df, columns_filter, thresh_info)
		# Sorting according to final score
		df = df.sort_values(by='Final_Score')
		# Counting according to final score
		df_count = df.groupby(by='Final_Score').count()['Item']
		# Counting how many food items as good, bad or neutral
		info = {'good': sum(df['Final_Score']>0),
				'neutral': sum(df['Final_Score']==0),
				'bad': sum(df['Final_Score']<0)
				}
		# Convert from counts to percentage
		denom = sum(info.values())
		info = {k:v*100/denom for k,v in info.items()}
		# Plotting
		axs[i].bar(list(info.keys()), list(info.values()))
		axs[i].set_title(restaurant)
		# axs[i].set_ylabel('Percent of food')

	plt.show()



if __name__ == '__main__':
	main()
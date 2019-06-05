"""
Created on Thu May 23 2019
Updated on Mon Jun 3 2019

@author: adnan
"""

import pandas as pd
import numpy as np
import os

def main():
	'''
	This function returns a pd.DataFrame object which contains the mean values for each restaurant where
	restaurant name is the column name and row names are the food descriptor

	This function assumes that all csv files are in one folder. It uses the os library to read all file names
	and run the code on each. 
	'''
	data_folder = './Final_CSV'
	extra_str = ''
	ext = '.csv'
	restaurant_names = os.listdir(data_folder)
	restaurant_names = [name.split('.')[0] for name in restaurant_names]
	assert len(restaurant_names) > 0, 'Need to have atleast one restaurant csv file!'
	# print(restaurant_names)
	# columns_filter = ['Total Fat', 'Carbohydrates', 'Protein', 'Sugar', 'Fiber', 'Sodium', 'Cholesterol', 'Calories', 'Saturated Fat', 'Trans Fat', 'Price']
	columns_filter = ['Carbs Metric', 'Cholesterol Metric', 'Fat Metric', 'Sodium Metric','Protein Metric','Price', 'Saturated Fat Metric']
	df_mean = pd.DataFrame()
	for restaurant in restaurant_names:
		print('Processing info from restaurant - ', restaurant)
		# Reading the csv file and storing as DataFrame
		df = pd.read_csv(data_folder+'/'+restaurant+extra_str+ext, encoding = 'iso-8859-1') 
		# Selecting columns with metrics only
		df = df[columns_filter]
		# Mean of each column
		res_mean = df.mean(axis=0)
		# Storing the means for 
		df_mean[restaurant] = res_mean
	df_mean.to_csv('mean.csv')


if __name__ == '__main__':
	main()

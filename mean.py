import pandas as pd
import numpy as np
import os

def get_means():
	'''
	This function returns a pd.DataFrame object which contains the mean values for each restaurant where
	restaurant name is the column name and row names are the food descriptor

	This function assumes that all csv files are in one folder. It uses the os library to read all file names
	and run the code on each. Moreover, it replaces all NaN with 0
	'''
	all_restaurants = os.listdir()
	all_restaurants.remove('mean.py')
	assert len(all_restaurants) > 0, 'Need to have atleast one restaurant csv file!'
	df_mean = pd.DataFrame()

	for restaurant in all_restaurants:
		df = pd.read_csv(restaurant, encoding = 'iso-8859-1') #reading the csv file and storing as DataFrame
		# Extracting digits from all columns
		for i in range(1,len(df.columns)): #start from column 1 because column 0 is food name
			try: 	
				df.iloc[:,i] = df.iloc[:,i].str.extract('(\d+)', expand=False).astype(float)
			except AttributeError: #one of the columns (Calories) has values of type int64 so .str method doesn't work on it
				pass
			df.iloc[:,i] = df.iloc[:,i].fillna(0)
		# Mean of each column
		res_mean = df.mean(axis=0)
		res_name = restaurant.split('_')[0] #only keeping retaurant name
		# Storing the means for 
		df_mean[res_name] = res_mean
	return df_mean


df_mean = get_means()
df_mean.to_csv('mean.csv')
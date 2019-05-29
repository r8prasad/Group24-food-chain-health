import pandas as pd
import numpy as np
import os
from difflib import SequenceMatcher


def map_list_to_list(s1_list,s2_list):
	'''
	Maps each string is s1_list to the closest string in s2_list
	Returns a dictionary where key is string in s1_list and value is string in s2_list
	'''

	assert isinstance(s1_list, list) and bool(s1_list)
	assert isinstance(s2_list, list) and bool(s2_list)
	for s1 in s1_list: assert isinstance(s1, str)
	for s2 in s2_list: assert isinstance(s2, str)

	dict_map = {}
	for s1 in s1_list:
		s2 = map_str_to_list(s1,s2_list)
		dict_map[s1] = s2

	df_map = pd.Series(dict_map, index=dict_map.keys())
	# df_map = pd.Series.to_frame(df_map)
	# df_map = pd.DataFrame.from_dict(dict_map, orient='columns', columns = ['PriceData', 'NutritionData'])
	return df_map

def map_str_to_list(s1,s2_list):
	'''
	Maps string s1 to the closest string in s2_list.
	Returns the string from s2_list which is closest to s1
	'''
	assert isinstance(s1,str)
	assert isinstance(s2_list, list) and bool(s2_list)
	for s2 in s2_list: assert isinstance(s2, str)

	s1_ratio = [SequenceMatcher(None, s1, s2).ratio() for s2 in s2_list]
	ind_max = max(zip(s1_ratio, range(len(s1_ratio))))[1]

	return s2_list[ind_max]

def add_price_column(df_Nd, df_map, df_Pd):
	'''
	Adds a new "Price" column to the Nutrition Data Dataframe and fills it in using the information from price data Dataframe
	df_map[i] = NutritionData
	df_map.keys()[i] = PriceData
	'''
	assert isinstance(df_Nd, pd.DataFrame)
	assert isinstance(df_Pd, pd.DataFrame)
	assert isinstance(df_map, pd.Series)

	# Add "Price" column to the Nutrition Dataframe
	df_Nd['Price'] = 0

	for i in range(0, len(df_map.index)):#len(df_map.index)):
		# Extracting the item name from the ith row of df_map
		item_Nd = df_map[i]
		item_Pd = df_map.keys()[i]
		# Finding row index of the item in Nutrition Data
		index_Nd = df_Nd[df_Nd['Item'] == item_Nd].index.tolist()[0]
		index_Pd = df_Pd[df_Pd['Item'] == item_Pd].index.tolist()[0]
		# Finding Price of item using its row index
		item_price = df_Pd['Price'][index_Pd]
		# Writing Price in Nutrition Data
		df_Nd['Price'][index_Nd] = item_price
	
	return df_Nd

def main():
	'''
	This file - 
	1. Loads Nutrition Data and Price Data
	2. Finds the closest match of an item from Price Data in Nutrition Data and adds the price to it
	3. Save the new dataframe with price column as a csv in a new folder
	'''
	Nd = 'NutritionData'
	Pd = 'PriceData'
	ext = '.csv'
	folder = 'NutritionDataWithPrice'
	restaurant_names = os.listdir('NutritionData')
	restaurant_names = [name.split('_')[0] for name in restaurant_names]
	assert len(restaurant_names) > 0, 'Need to have atleast one restaurant csv file!'
	# print(restaurant_names)

	for i in range(0,len(restaurant_names)):
		restaurant = restaurant_names[i]
		print('Processing info from resaturant - ', restaurant)
		# Reading NutritionData of a restaurant
		df_Nd = pd.read_csv(Nd+'/'+restaurant+'_'+Nd+ext, encoding = 'iso-8859-1') #reading the csv file and storing as DataFrame
		# Reading PriceData of a restaurant
		df_Pd = pd.read_csv(Pd+'/'+restaurant+'_'+Pd+ext, encoding = 'iso-8859-1') #reading the csv file and storing as DataFrame
		# Extracting the Items from dataFrame as a list
		Item_Nd = list(df_Nd['Item'])
		Item_Pd = list(df_Pd['Item'])
		# Map items from Price Data to Nutrition Data
		df_map = map_list_to_list(Item_Pd, Item_Nd)
		df_Nd = add_price_column(df_Nd, df_map, df_Pd)
		# Writing dataframe to csv file
		df_Nd.to_csv(folder + '/' + restaurant + '_' + Nd + ext)

if __name__ == '__main__':
	main()



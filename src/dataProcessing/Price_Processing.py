"""
Created on Sun June 2 2019

@author: adnan
"""


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
		s2, s2_ratio = map_str_to_list(s1,s2_list)
		dict_map[s1] = [s2, s2_ratio]

	df_map = pd.Series(dict_map, index=dict_map.keys())
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

	return s2_list[ind_max], s1_ratio[ind_max]

def add_price_column(df_Nd, df_map, df_Pd):
	'''
	Adds a new "Price" column to the Nutrition Data Dataframe and fills it in using the information from price data Dataframe
	df_map[i] = PriceData
	df_map.keys()[i] = NutritionData
	'''
	assert isinstance(df_Nd, pd.DataFrame)
	assert isinstance(df_Pd, pd.DataFrame)
	assert isinstance(df_map, pd.Series)

	# Add "Price" column to the Nutrition Dataframe
	df_Nd['Price'] = 0.0

	for i in range(0, len(df_map.index)):#len(df_map.index)):
		# Extracting the item name from the ith row of df_map
		item_Nd = df_map.keys()[i]
		item_Pd = df_map[i][0]
		item_ratio = df_map[i][1] #ratio of match from Nutrition Data to Price Data
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
	Nd_folder = '../../data/CleanedNutritionData'
	extra_str = '_Clean'
	Pd = 'PriceData'
	Pd_folder = '../../data/RawPriceData'
	ext = '.csv'
	folder = '../../data/NutritionDataWithPrice'
	restaurant_names = os.listdir(Nd_folder)
	restaurant_names = [name.split('_')[0] for name in restaurant_names]
	assert len(restaurant_names) > 0, 'Need to have atleast one restaurant csv file!'

	for i in range(0,len(restaurant_names)):
		restaurant = restaurant_names[i]

		# Reading NutritionData of a restaurant
		df_Nd = pd.read_csv(Nd_folder+'/'+restaurant+'_'+Nd+extra_str+ext, encoding = 'iso-8859-1') #reading the csv file and storing as DataFrame
		# Reading PriceData of a restaurant
		df_Pd = pd.read_csv(Pd_folder+'/'+restaurant+'_'+Pd+ext, encoding = 'iso-8859-1') #reading the csv file and storing as DataFrame
		# Extracting the Items from dataFrame as a list
		Item_Nd = list(df_Nd['Item'])
		Item_Pd = list(df_Pd['Item'])
		# Map items from Nutrition Data to Price Data so every item has a price
		df_map = map_list_to_list(Item_Nd, Item_Pd)
		df_Nd = add_price_column(df_Nd, df_map, df_Pd)
		# # Writing dataframe to csv file
		if not os.path.exists(folder):
			os.makedirs(folder)
		df_Nd.to_csv(folder +'/' + restaurant +ext, index=False)

if __name__ == '__main__':
	main()


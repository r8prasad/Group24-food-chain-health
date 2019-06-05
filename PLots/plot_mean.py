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
import matplotlib.colors as mcolors

def analysis_1(df):
	# rows = ['Total Fat', 'Carbohydrates', 'Protein', 'Sugar', 'Cholesterol']
	rows = ['Carbs Metric', 'Cholesterol Metric', 'Fat Metric', 'Sodium Metric','Protein Metric','Price', 'Saturated Fat Metric']
	cols = ['DunkinDonuts', 'PandaExpress', 'Subway','BurgerKing', 'PizzaHut', 'Mcdonalds']
	df = df.loc[rows,cols]

	restaurant_names = list(df.keys())
	print(restaurant_names)
	nut_labels = list(df.index.values)
	# Colors
	cnames = ['b', 'g', 'r', 'y', 'c', 'm', 'k', 'tab:blue', 'tab:orange', 'tab:brown','tab:gray']
	# Plotting
	fig, axs = plt.subplots(2, 3, figsize=(14, 6), sharey=True)
	fig.subplots_adjust(hspace = .5, wspace=.2)
	axs = axs.flatten()
	for i in range(0, len(restaurant_names)):
		restaurant = restaurant_names[i]
		S = df.loc[:,restaurant]
		nut_values = list(S)
		nut_values = [n*100/sum(nut_values) for n in nut_values]
		# print(nut_values)
		nut_labels_short = [n[0:3] for n in nut_labels]
		nut_labels_short[0] = 'Fat'
		axs[i].bar(nut_labels_short, nut_values)
		axs[i].set_title(restaurant)
	plt.show()

def analysis_2(df):
	'''
	Plot a bar graph with mean prices for each restaurant
	'''
	df = adjust_for_meal_option(df)
	df = df.sort_values(by='Price', axis=1)
	avg_price = df.loc['Price', :]
	# Plotting
	fig, ax = plt.subplots(figsize=(14,6))
	ax.barh(list(avg_price.keys()), list(avg_price))
	ax.set_title('Average Meal Price per Restaurant')
	ax.set_xlabel('Average Price ($)')
	plt.show()

def analysis_3(df, label='Price'):
	'''
	Plot a bar graph with mean prices for each restaurant and highlight ones in focus
	'''
	focus = ['DunkinDonuts', 'PandaExpress', 'Subway','BurgerKing', 'PizzaHut', 'Mcdonalds']
	df = adjust_for_meal_option(df)
	df = df.sort_values(by=label, axis=1)
	avg_price = df.loc[label, :]
	restaurant_names = avg_price.keys()
	prices = list(avg_price)
	# Plotting
	fig, ax = plt.subplots(figsize=(14,6))
	for i in range(0, len(restaurant_names)):
		p = [0]*len(restaurant_names)
		p[i] = prices[i]
		if restaurant_names[i] in focus:
			ax.barh(restaurant_names, p, color = 'darkblue')
		else:
			ax.barh(restaurant_names, p, color = 'darkblue', alpha = 0.5)
		ax.set_title('Average ' + label + ' per Restaurant')
		ax.set_xlabel('Average ' + label)
	plt.show()

def adjust_for_meal_option(df):
	'''
	Adds an extra amount to Price if restaurant is not a pizza joint to account for meal order
	'''
	extra_amount = 3.0
	restaurant_names = list(df.keys())
	nut_labels = list(df.index.values)
	for restaurant in restaurant_names:
		if not(restaurant in ['PizzaHut', 'Dominos']):
			df.loc['Price', restaurant] = df.loc['Price', restaurant] + extra_amount
	return df

def main():
	# Initializations
	data_folder = '../'
	file_name = 'mean'
	ext = '.csv'
	# Reading the csv file and storing as DataFrame
	df = pd.read_csv(data_folder+file_name+ext, encoding = 'iso-8859-1', index_col=[0])
	# analysis_1(df)
	# analysis_2(df)
	analysis_3(df, label='Cholesterol Metric')
		
if __name__ == '__main__':
	main()
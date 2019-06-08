import pandas as pd
import os
from matplotlib.pylab import subplots
import csv
import collections
import re
import numpy as np

population = {'AL': 4887871, 'AZ': 7171646, 'CA': 39557045, 'CO': 5695564, 'FL': 21299325, 'GA': 10519475,'IL': 12741080, 'KY': 4468402, 'MA': 6902149, 'MN': 5611179, 'MT': 1062305, 'NY': 19542209, 'OK': 3943079, 'TX': 28701845, 'WA': 7535591}
diseaseRate = {
				"Obesity" :{'AL': 36.3, 'AZ': 29.5, 'CA': 25.1, 'CO': 22.6, 'FL': 28.4, 'GA': 31.6,'IL': 31.1, 'KY': 34.3, 'MA': 25.9, 'MN': 28.4, 'MT': 25.3, 'NY': 25.7, 'OK': 36.5, 'TX': 33.0, 'WA': 27.7},
				"Diabetes" : {'AL': 14.1, 'AZ': 10.4, 'CA': 10.5, 'CO': 7.4, 'FL': 10.5, 'GA': 11.4,'IL': 11.0, 'KY': 12.9, 'MA': 9.5, 'MN': 7.8, 'MT': 7.9, 'NY': 10.5, 'OK': 12.7, 'TX': 11.9, 'WA': 9.1},
				"Heart Disease" : {'AL': 274.5, 'AZ': 189.8, 'CA': 203.0, 'CO': 164.8, 'FL': 200.0, 'GA': 236.0,'IL': 220.7, 'KY': 257.3, 'MA': 179.0, 'MN': 145.4, 'MT': 172.2, 'NY': 248.3, 'OK': 272.4, 'TX': 220.4, 'WA': 180.5}
			} 

def remove_punctuations(restaurants_list):
	regExp = r'[^A-Za-z.]+'
	return [re.sub(regExp, '', restaurant) for restaurant in restaurants_list]
def locs(restaurants, goodOrBad, disease):
	"""
		correlate number of locations with diseases
	"""

	#assert statements
	assert(isinstance(restaurants, list))
	assert(isinstance(goodOrBad, list))
	assert(isinstance(disease, str))

	goodBadDict = dict(zip(restaurants, goodOrBad))
	df = pd.read_csv('LocationData.csv', encoding = 'iso-8859-1')
	df1 = df[df.Restaurant.isin(restaurants)]
	df1['goodOrBad'] = df1['Restaurant'].map(goodBadDict)
	df2 = df1.groupby(['State', 'goodOrBad']).sum()
	df2['Population'] = df2.index.get_level_values('State').map(population.get)
	df2["Outlets per population"] = df2['Number of Outlets']/df2['Population']

	groups = df2.groupby(['goodOrBad'])
	badDf = groups.get_group(-1)
	badDf.index = badDf.index.droplevel('goodOrBad')
	multFactor = 10**6
	sorted_dict = dict(sorted(diseaseRate[disease].items(), key=lambda kv: kv[1]))
	x = sorted_dict.keys()
	y1 = sorted_dict.values()
	y2 = [badDf.loc[state ,"Outlets per population"]*multFactor for state in list(x)]

	fig, ax = subplots(figsize=(14,6))
	ax.set_xlabel('States of USA')
	y_label = f'{disease} death rate (per 100k)' if (disease == "Heart Disease") else f'{disease} rate (%)'
	ax.set_ylabel(y_label)

	ind = np.arange(len(x))
	width = 0.6
	ax.bar(ind, y1, width, color='tab:cyan', align='center', alpha=0.3, edgecolor='k')

	if(disease == "Diabetes"):
		ymin, ymax = 5, 16
	elif(disease == "Obesity"):
		ymin, ymax = 18, 38
	else:
		ymin, ymax = 120, 280

	ax.set_ylim([ymin,ymax])
		

	ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
	color = 'tab:red'
	ax2.plot(x, y2, 'or-',label=f'Outlets per million capita of Unhealthy Restaurants')#, x,y3, 'g+-')
		
	ax2.set_ylabel(f'Outlets per million capita', color=color)  # we already handled the x-label with ax1
	ax2.legend(fontsize=14)
	
	fig.savefig(f'figure_{disease}.png', dpi=300)

all_restaurants = os.listdir('../../data/FinalData')

restaurants = remove_punctuations(all_restaurants)
restaurant_metrics = []

for restaurant in restaurants:
	df = pd.read_csv('../../data/FinalData/'+ restaurant, encoding = 'iso-8859-1')
	transFat = df["Trans Fat"].mean()
	sugar = df["Sugar"].mean()
	saturatedFat = df["Saturated Fat Metric"].mean()
	cholesterol = df["Cholesterol Metric"].mean()
	fat = df["Fat Metric"].mean()
	carbs = df["Carbs Metric"].mean()
	
	metric_dict = {}
	metric_dict['Name'] = restaurant.split('.')[0]
	metric_dict['Diabetes Metric'] = sugar  + saturatedFat + transFat
	metric_dict['Heart Disease Metric'] = cholesterol + saturatedFat + transFat
	metric_dict['Obesity Metric'] = saturatedFat + transFat + carbs

	restaurant_metrics.append(metric_dict)

df = pd.DataFrame(restaurant_metrics)
df.set_index('Name', inplace=True)

#plot line graph in sorting order
df.sort_values(by=['Diabetes Metric'], ascending=False, inplace=True)

restaurants = ['Mcdonalds', 'PizzaHut', 'Dominos', 'BurgerKing', 'ChickFilA', 'KFC']
goodOrBad = [-1,-1,-1,-1,-1,-1,-1]
locs(restaurants, goodOrBad, "Diabetes")

df.sort_values(by=['Heart Disease Metric'], ascending=False, inplace=True)
locs(restaurants, goodOrBad, "Heart Disease")

df.sort_values(by=['Obesity Metric'], ascending=False, inplace=True)
locs(restaurants, goodOrBad, "Obesity")
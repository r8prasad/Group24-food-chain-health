import pandas as pd
import re

def clean_extracted_data(df1, fname, thresholdSize, thresholdProtein):
	"""
	Removes drinks and condiments from the menu
	"""
	assert isinstance(df1,pd.DataFrame)
	assert isinstance(fname,str)
	assert isinstance(thresholdSize, int)
	assert isinstance(thresholdProtein, int)

	#drop duplicate rows
	df1.drop_duplicates(subset=None, keep='last', inplace=True)

	#drop rows containing drinks
	drinks = " oz| milk|cappuccino|frappe|macchiato|coffee| latte|caffe|lemonade| juice"
	df2 = df1[~df1.index.str.contains(drinks, flags=re.IGNORECASE, regex=True)]

	#drop row with smaller serving size-condiments
	df3 = df2[df2["Serving Size"] >= thresholdSize]

	#drop row with smaller protein size -> Drinks and sauces barely have proteins (except shakes)
	df4 = df3[df3["Protein"] > thresholdProtein]

	df4.to_csv(f"../../data/CleanedNutritionData/{fname}_Clean.csv", encoding = 'iso-8859-1', index=True)

def str_to_int(df):
	"""
	Takes the dataframe as input for the values of the different food stuffs and converts them to float

	Removes the g and mg at the end.
	"""
	df = df.str.strip('g')
	df = df.str.strip('m').astype(float)
	return df

def data_cleaning(fname, thresholdSize, thresholdProtein):
	"""
	Cleaning the data obtained from scraping the websites.
	Inital pricessing for formatiing the data into the useful format.
	"""
	assert isinstance(fname,str)
	assert isinstance(thresholdSize, int)
	assert isinstance(thresholdProtein, int)

	df = pd.read_csv(f"{fname}.csv", encoding = 'iso-8859-1')

	df['Calories'] = df['Calories'].astype(str)
	df = df.set_index('Item').apply(lambda x: str_to_int(x), axis = 1)

	processedFile = fname.split("/")[-1]
	clean_extracted_data(df, processedFile, thresholdSize, thresholdProtein)

data_cleaning(fname="../../data/RawNutritionData/Arbys_NutritionData", thresholdSize = 70, thresholdProtein = 2)
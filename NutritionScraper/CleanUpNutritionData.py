import pandas as pd
import re

def isNaN(inputString):
	return inputString != inputString

def extract_number(inputString, thresholdSize):
	if (isNaN(inputString)):
		return thresholdSize
	else:
		return float(re.findall(r'[\d\.\d]+', inputString)[0])

def clean_extracted_data(fname, thresholdSize, thresholdProtein):
	df1 = pd.read_csv(f"{fname}.csv", encoding = 'iso-8859-1')

	#drop duplicate rows
	df1.drop_duplicates(subset=None, keep='last', inplace=True)

	#drop rows containing drinks
	drinks = " oz| milk|cappuccino|frappe|macchiato|coffee| latte|caffe|lemonade| juice"
	df2 = df1[~df1.Item.str.contains(drinks, flags=re.IGNORECASE, regex=True)]

	#drop row with smaller serving size-condiments
	df3 = df2[df2["Serving Size"].apply(extract_number, args=[thresholdSize]) >= thresholdSize]

	#drop row with smaller protein size -> Drinks and sauces barely have proteins (except shakes)
	df4 = df3[df3["Protein"].apply(extract_number, args=[thresholdSize]) > thresholdProtein]

	df4.to_csv(f"{fname}_Clean.csv", encoding = 'iso-8859-1', index=False)

clean_extracted_data(fname="PizzaHut_NutritionData", thresholdSize = 70, thresholdProtein = 2)

def str_to_int(df):
    """
    Takes the dataframe as input for the values of the different food stuffs and converts them to float
    
    Removes the g and mg at the end.
    """
    df = df.str.strip('g')
    df = df.str.strip('$')
    df = df.str.strip('m').astype(float)
    return df

def data_cleaning(df):
    """
    Cleaning the data obtained from scraping the websites.
    Inital pricessing for formatiing the data into the useful format.
    """
    assert isinstance(df,pd.DataFrame)
    df['Calories'] = df['Calories'].astype(str)
    df = df.set_index('Item').apply(lambda x: str_to_int(x), axis = 1)
#    df['Serving Size'] = df['Serving Size'].apply(lambda x : 1 if x == 'N/A' else x)
    return df
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:48:49 2019

@author: Varad
"""
import pandas as pd
from Calorie_Multi import multinomial_combinations

def carbs_metric(df):
    """
    Calculates the carbs metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    carbs = 2000/300
    ratio = df['Carbohydrates'] / df['Calories']
    metric = carbs * ratio
    return metric

def chol_metric(df):
    """
    Calculates the Cholestrol metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    chol = 2000/300
    ratio = df['Cholesterol'] / df['Calories']
    metric = chol * ratio
    return metric

def prot_metric(df):
    """
    Calculates the Protein metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    prot = 2000/50
    ratio = df['Protein'] / df['Calories']
    metric = prot * ratio
    return metric

def fat_metric(df):
    """
    Calculates the Fat metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    fat = 2000/77
    ratio = df['Total Fat'] / df['Calories']
    metric = fat * ratio
    return metric

def sodium_metric(df):
    """
    Calculates the Sodium metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    sod = 2000/2400
    ratio = df['Sodium'] / df['Calories']
    metric = sod * ratio
    return metric

def SatFat_metric(df):
    """
    Calculates the Saturated fat metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    satfat = 2000/20
    ratio = df['Saturated Fat'] / df['Calories']
    metric = satfat * ratio
    return metric

def processing(fname):
    """
    This function performs the different categorisation of the items food menu of all the Restaurants
    Operations:
                Calculate and append the corresponding nuttrient metric as a new column.
                Remove the '$' sign from the price columns
    :param Input:
                    fname --> The name of the restaurant that is supposed to be processed (This is the name of the final file too)
           Output:
                    mult_cal --> A data frame which contains all the possible combinations satisfying the 2000 calories criterion.
    """
    df = pd.read_csv(f"../../data/NutritionDataWithPrice/{fname}.csv", encoding = 'iso-8859-1')
    df['Price'] = df['Price'].str.strip('$')
#    data_price = pd.read_csv(f"NutritionDataWithPrice\{fname}.csv", encoding = 'iso-8859-1')
#    mult_cal = pd.DataFrame()
#    df = data_cleaning(data)
    df['Carbs Metric'] = df.apply(lambda x: carbs_metric(x) , axis = 1) # Calculates the Carbs metric for each food ite, basically operating on each column
    df['Cholesterol Metric'] = df.apply(lambda x: chol_metric(x) , axis = 1)# Calculates the Cholesterol metric for each food ite, basically operating on each column
    df['Protein Metric'] = df.apply(lambda x: prot_metric(x) , axis = 1)# Calculates the protein metric for each food ite, basically operating on each column
    df['Fat Metric'] = df.apply(lambda x: fat_metric(x) , axis = 1)# Calculates the Fat metric for each food ite, basically operating on each column
    df['Sodium Metric'] = df.apply(lambda x: sodium_metric(x) , axis = 1)# Calculates the Sodium metric for each food ite, basically operating on each column
    df['Saturated Fat Metric'] = df.apply(lambda x: SatFat_metric(x) , axis = 1)# Calculates the Saturated metric for each food ite, basically operating on each column
    df.to_csv(f"../../data/FinalData/{each}.csv", encoding = 'iso-8859-1', index=False)
    
    #Choosing the combinations of the 2000 calorie combination
    mult_cal = multinomial_combinations(df,fname)
    return mult_cal

import os
loc = '../../data/NutritionDataWithPrice' #Update the appropriate location
names = os.listdir(loc)
names = [each.split('.')[0] for each in names] #If the file name has no '.', then ignore comment out this line
assert len(names) > 0

for each in names:
    final_data = processing(each)
    final_data.to_csv(f"../../data/Combinations/{each}.csv", encoding = 'iso-8859-1', index=False) #The intital f-string is the location of the final cleaned up files with metric

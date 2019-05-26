# -*- coding: utf-8 -*-
"""
Created on Sun May 26 00:03:37 2019

@author: varad
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:48:49 2019

@author: varad
"""
import pandas as pd

def metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    
    assert isinstance(df,pd.DataFrame)
#    columns = ['Serving Size','Fat','Sugar','Protein','Sodium','Calories']
    coefs = [0,0.05,0.0375,0.05,0.00115,0]
    df = df.mul(coefs,axis = 1)
    df['Metric'] = df.sum(axis = 1)
    return df
    
def str_to_int(df):
    """
    Takes the dataframe as input for the values of the different food stuffs and converts them to float
    
    Removes the g and mg at the end.
    """
    df = df.str.strip('g')
    df = df.str.strip('m').astype(float)
    return df

def processing_arbys():
    """
    This function performs the different categorisation of the items on the Arby's food menu,
    into breakfast, lunch and dinner.
    """
    fname = "BurgerKing_NutritionData"
    data = pd.read_csv(f"../Project/Git/NutritionData/{fname}.csv", encoding = 'iso-8859-1')
    data['Calories'] = data['Calories'].astype(str)
    data = data.set_index('Item').apply(lambda x: str_to_int(x), axis = 1)
    
#    data = data.apply(lambda x: x/data['Serving Size'])
    new_data = data.drop(['Trans Fat','Fiber','Carbohydrates','Saturated Fat','Cholesterol'], axis = 1)
    
    data_with_metric = metric(new_data)
    return data_with_metric
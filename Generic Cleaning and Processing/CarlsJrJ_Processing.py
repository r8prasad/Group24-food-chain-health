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
    return df['Metric']
    
def processing():
    """
    This function performs the different categorisation of the items on the Arby's food menu,
    into breakfast, lunch and dinner.
    """
    fname = "BurgerKing_NutritionData"
    data = pd.read_csv(f"{fname}.csv", encoding = 'iso-8859-1')
    df = data_cleaning(data)
#    data = data.apply(lambda x: x/data['Serving Size'])
    new_data =df.drop(['Trans Fat','Fiber','Carbohydrates','Saturated Fat','Cholesterol'], axis = 1)
    
    new_data['Metric'] = metric(new_data)
    new_data['Calorie count'] = new_data['Calories'] / new_data['Serving Size']
    new_data = new_data.fillna(0)
    
    return new_data
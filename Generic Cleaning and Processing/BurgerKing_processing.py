# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:48:49 2019

@author: varad
"""
import pandas as pd
from Calorie_Multi import *
from Data_Cleaning import *
def metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    
    assert isinstance(df,pd.DataFrame)
#    columns = ['Serving Size','Fat','Sugar','Protein','Sodium','Calories']
    df =df.drop(['Trans Fat','Fiber','Carbohydrates','Saturated Fat','Cholesterol'], axis = 1)
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
    df['Metric'] = metric(df).fillna(0)
    
    mult_cal = calories_choices(df)
    
    return df
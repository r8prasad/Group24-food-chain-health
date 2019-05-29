# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:48:49 2019

@author: varad
"""
import pandas as pd
from Calorie_Multi import *
from Data_Cleaning import data_cleaning

def metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    coefs = [0,0.05,0,0.0375,0.05,0,0.00115,0,0,0,0]   
    metric = df.dot(coefs)
    return metric
    
def processing():
    """
    This function performs the different categorisation of the items on the Arby's food menu,
    into breakfast, lunch and dinner.
    """
    fname = "BurgerKing_NutritionData_Clean"
    data = pd.read_csv(f"{fname}.csv", encoding = 'iso-8859-1')
    df = data_cleaning(data)
    df['Metric'] = df.apply(lambda x: metric(x) , axis = 1)  
    mult_cal = calories_choices(df)
    
    return df    
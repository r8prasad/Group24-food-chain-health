# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:48:49 2019

@author: Varad
"""
import pandas as pd
import numpy as np
from Calorie_Multi import *
#from Data_Cleaning import data_cleaning

def carbs_metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    carbs = 2000/300
    ratio = df['Carbohydrates'] / df['Calories']
    metric = carbs * ratio
    return metric

def chol_metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    chol = 2000/300
    ratio = df['Cholesterol'] / df['Calories']
    metric = chol * ratio
    return metric

def prot_metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    prot = 2000/300
    ratio = df['Protein'] / df['Calories']
    metric = prot * ratio
    return metric

def fat_metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    fat = 2000/77
    ratio = df['Total Fat'] / df['Calories']
    metric = fat * ratio
    return metric

def sodium_metric(df):
    """
    Calculates the metric of each food item based on the research papers
    """
    assert isinstance(df,pd.Series)
    sod = 2000/2400
    ratio = df['Sodium'] / df['Calories']
    metric = sod * ratio
    return metric
    
def processing(fname):
    """
    This function performs the different categorisation of the items on the Burger King's food menu,
    into breakfast, lunch and dinner.
    """
    df = pd.read_csv(f"{fname}.csv", encoding = 'iso-8859-1')
    df['Price'] = df['Price'].str.strip('$')
#    data_price = pd.read_csv(f"NutritionDataWithPrice\{fname}.csv", encoding = 'iso-8859-1')
    mult_cal = pd.DataFrame()
#    df = data_cleaning(data)
    df['Carbs Metric'] = df.apply(lambda x: carbs_metric(x) , axis = 1)
    df['Cholesterol Metric'] = df.apply(lambda x: chol_metric(x) , axis = 1)
    df['Fat Metric'] = df.apply(lambda x: fat_metric(x) , axis = 1)
    df['Sodium Metric'] = df.apply(lambda x: sodium_metric(x) , axis = 1)
    mult_cal = ulti(df,fname)
    return mult_cal

fname = "PandaExpress_NutritionData_Clean_Merged"
merged = processing(fname)
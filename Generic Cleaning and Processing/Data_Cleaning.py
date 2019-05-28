# -*- coding: utf-8 -*-
"""
Created on Sun May 26 11:53:10 2019

@author: Varad
"""
import pandas as pd

def str_to_int(df):
    """
    Takes the dataframe as input for the values of the different food stuffs and converts them to float
    
    Removes the g and mg at the end.
    """
    df = df.str.strip('g')
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
    
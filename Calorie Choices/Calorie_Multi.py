# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:06:03 2019

@author: varad
"""
import pandas as pd
import numpy as np
from BurgerKing_processing import *

def calories_choices(df):
    """
    This function returns the 5 best possible combinations from a particular restaurant which roughly
    satisfy the 2000 calories a day criterion
    """
    assert isinstance(df,pd.DataFrame)
    
    calories = df['Calories'].tolist()
    probs = np.asarray(calories)
    dummy = probs
    # This sections finds all the possible combinations for which the sum equals 2000   
    combination = np.where(dummy + dummy[:,None] + dummy[:,None,None]== 2000)
    final = np.flip(combination).T.tolist()
    df = df.reset_index()
    #This part of the code finds the item name from the corresponding indices obtained in the
    #combinations list
    item = []
    list_item = []
    for each in final:
        for element in each:
            item.append(df.loc[element,'Item'])
        list_item.append(item)
        item = []
    #Storing data as a Pandas object to make computations easier later on.
    data = pd.DataFrame(list_item)
    data.columns = ['Item 1','Item 2','Item 3']
    df = df.set_index('Item')
    #Finding the metric for each combination
    list_metric = []
    final_metric = []
    met = 0
    for index,each in data.iterrows():
        for element in each:
            met = metric(df.loc[element]).sum()
            list_metric.append(met)
        final_metric.append(sum(list_metric))
        list_metric = []
    #Sorting accoridng to the metric column
    data['Metric'] = pd.Series(final_metric)
    data = data.sort_values('Metric',ascending = False)
    
    return data
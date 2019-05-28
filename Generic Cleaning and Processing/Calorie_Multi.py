# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:06:03 2019

@author: varad
"""
import pandas as pd
from scipy.stats import multinomial
import numpy as np

def calories_choices(df):
    """
    This function returns the 5 best possible combinations from a particular restaurant which roughly
    satisfy the 2000 calories a day criterion
    """
    assert isinstance(df,pd.DataFrame)
    
    calories = df['Calories'].tolist()
    probs = np.asarray(calories)
    dummy = probs
        
    combination = np.where(dummy + dummy[:,None] + dummy[:,None,None]== 2000)
    final = np.flip(combination).T.tolist()
    df = df.reset_index()
    
    item = []
    list_item = []
    for each in final:
        for element in each:
            item.append(df.loc[element,'Item'])
        list_item.append(item)
        item = []
            
    return list_item
    
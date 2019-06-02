# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:06:03 2019

@author: varad
"""
import pandas as pd
import numpy as np

def ulti(df,fname):
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
    final_price = []
    list_price= []
    final_metric = []
    met = 0
    for index,each in data.iterrows():
        for element in each:
            met = df.loc[element,'Fat Metric'] + df.loc[element,'Carbs Metric'] + df.loc[element,'Cholesterol Metric']
            price = df.loc[element,'Price']
            list_metric.append(met)
            list_price.append(float(price))
        final_metric.append(round(sum(list_metric),5))
        final_price.append(sum(list_price))
        list_metric = []
        list_price = []
    #Sorting accoridng to the metric column
    data['Metric'] = pd.Series(final_metric)
    data['Price'] = pd.Series(final_price)
    data = data.sort_values('Metric')
    data = data.drop_duplicates(subset = 'Metric')
    
    data.to_csv(f"metric_merged\{fname}_Merged.csv", encoding = 'iso-8859-1', index=False)
    return data
"""
This is my function for generating the dictionary.
The X axis are the keys and the Y axes are the dict values
"""
import pandas as pd
import numpy as np
from Choices import choices
import plotly.plotly as py
import plotly.graph_objs as go
import os
plotly.tools.set_credentials_file(username='vajoshi', api_key='sZn24Xy0sIOqOyRMLytK')

"""
The username is the one that you create and the api key is the one you get from plotly->Settings->API keys, and then copy that key value.
def names_maker():
    """
    Following function plots the graph for the best metric dishes of the 5 restaurants agaisnt their prices.
    
    The avergae price for having a full meal at each of the restaurants is calculated. The top 5 dishes in terms of health
    metric are taken their average price is calculated.
    """
    loc = './Final'
    names = os.listdir(loc)
    names = [each.split('_')[0] for each in names]
    assert len(names) > 0
    
    names.pop(8)
    names.pop(8)
    names.pop(3)
    res = {}
    ave_price =  []
    for each in names:
        if each == 'Dominos':
            continue
        else:
            data = pd.read_csv(f'.\Final_CSV\{each}.csv', encoding = 'iso-8859-1')
            df = choices(data,each)  
            row = (df['Price'][:20].sum())/20
            res[row] = each
    return res

Names = names_maker()

Restaurants = dict(sorted(Names.items()))   
data = [go.Bar(
        x = list(Restaurants),
        y = list(Restaurants.values()),
        orientation = 'h',
        marker = dict(color = 'steelblue')
    )]

layout = go.Layout(
    margin=dict(
        pad = 10
    ),
#        xaxis=dict(
 #       range=[5, 35]),
    title = 'Average Price Per Meal',
    font = dict(size=12, color='#7f7f7f'),
)
figure = go.Figure(data=data, layout = layout)
figure['layout'].update(autosize=False, width=800, height=500, margin=dict(l=110))
py.iplot(figure, filename='Best Metric vs Price')
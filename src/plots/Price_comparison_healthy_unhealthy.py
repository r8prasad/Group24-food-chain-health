import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
plotly.tools.set_credentials_file(username='vajoshi', api_key='eZ0l3Qg71TAVdJ7DO86U')
def healthy_maker():
    """
    Following function plots the graph for the bets metric dishes of the 5 restaurants agaisnt their prices.
    
    The avergae price for having a full meal at each of the restaurants is calculated. The top 5 dishes in terms of health
    metric are taken their average price is calculated.
    """
    loc = '../../data/Combinations'
    names = os.listdir(loc)
    names = [each.split('.')[0] for each in names]
    assert len(names) > 0

    res = {}
    ave_price =  []
    for each in names:
        if each == 'Dominos' or each == 'PandaExpress' or each == 'Mcdonalds' or each == 'ChickFilA':
            continue
        else:
            df = pd.read_csv(f'../../data/Combinations/{each}.csv', encoding = 'iso-8859-1')
            l = int(len(df)/2)
            df = df.sort_values('Metric')
            row = (df['Price'][:l].sum())/l
            res[each] = round(row,4)
    return res
Healthy = healthy_maker()

def unhealthy_maker():
    """
    Following function plots the graph for the bets metric dishes of the 5 restaurants agaisnt their prices.
    
    The avergae price for having a full meal at each of the restaurants is calculated. The top 5 dishes in terms of health
    metric are taken their average price is calculated.
    """
    loc = '../../data/Combinations'
    names = os.listdir(loc)
    names = [each.split('.')[0] for each in names]
    assert len(names) > 0

    ave_metric =  {}
    for each in names:
        if each == 'Dominos' or each == 'PandaExpress' or each == 'Mcdonalds' or each == 'ChickFilA':
            continue
        else:
            df = pd.read_csv(f'../../data/Combinations/{each}.csv', encoding = 'iso-8859-1')
            df = df.sort_values('Metric')
            l = int(len(df)/2)
            price = (df['Price'][-l:].sum())/l
            ave_metric[each] = round(price,4)
    return ave_metric
Unhealthy= unhealthy_maker()

#Code for generating the plot of the average price of healthy and unhealthy restaurants on the same grouped bar graph.
def Price_plots():
    healthy = dict(sorted(Healthy.items(), key = lambda kv:(kv[1], kv[0])))
    unhealthy = dict(sorted(Unhealthy.items(), key = lambda kv:(kv[1], kv[0])))
    trace1 = go.Bar(
        x = list(healthy),
        y = list(healthy.values()),
        marker = dict(color = 'green'),
        opacity = 0.6,
        name='Healthy Food'
    )
    trace2 = go.Bar(
        x=list(unhealthy),
        y=list(unhealthy.values()),
        marker = dict(color = 'red'),
        opacity = 0.6,
        name='Unhealthy Food'
    ) 

    data = [trace1, trace2]
    #Changing the layout properties in plotly
    layout = go.Layout(
        barmode='group',
        margin=dict(
        pad = 10
    ),
    yaxis = dict(showgrid = True),
    xaxis = dict(showgrid = False),
    title = '<b>AVERAGE PRICE COMPARISON</b>',
    titlefont=dict(size = 25, color='black', family='Arial, sans-serif'),
    font = dict(size=13, color='black'),
    )

    xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
            text='Restaurants',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    return data,layout

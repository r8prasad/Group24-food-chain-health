# -*- coding: utf-8 -*-
"""
Created on Sun May 26 02:11:14 2019

@author: varad
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 26 00:09:46 2019

@author: varad
"""
import collections as c
def top_metrics(fname):
    """
    Plotting the top 10 metric dishes for the restaurant
    """
    b = processing_arbys()
    v = dict(b['Metric'])
    
    count_dict = dict(c.Counter(v).most_common(5))
    
    return count_dict
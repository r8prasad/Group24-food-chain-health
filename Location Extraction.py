#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, json
def get_lcoation():
    """
    Return a list of locations of the query submitted in the input.
    Can modify the functionality to store the data as well.
    """
api_key = 'AIzaSyAPYbn_KKl9ZEvdHbvNYVluX8s9lfdq79M'

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

query = input('Search query: ')

r = requests.get(url + 'query=' + query +
                        '&key=' + api_key)
x = r.json()
y = x['results']
for i in range(len(y)): 
      
    # Print value corresponding to the 
    # 'name' key at the ith index of y 
    print(y[i]['formatted_address']) 


# In[ ]:





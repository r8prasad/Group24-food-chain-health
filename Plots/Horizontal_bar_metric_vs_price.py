import pandas as pd
def choices_cleaning(fname):
    """
    Cleans the newly created file and retains only the meaningful data. Removes the entries with incomplete or unavailable
    data to simplify the visualisations.
    """
    
    df = pd.read_csv(f'{fname}.csv', encoding = 'iso-8859-1')
    df = df[df.Price > 10]
    df.columns = ['Item1','Item2', 'Item3', 'Metric', 'Price']
    #This removes the entries where two items chosen are the same
    df = df.query('Item1 != Item3')
    
    ind = []
    #Removes the entries which has fries because they get repeated more often.
    for index,each in df.iterrows():
        for element in each:
            if (str(element).find('Fries') != -1):
                ind.append(index)
    df = df.drop(list(set(ind)))
    
    df = df.reset_index().drop('index', axis = 1)
    return df


import numpy as np
import matplotlib.pyplot as plt
def Best_vs_Price():
    """
    Following function plots the graph for the bets metric dishes of the 5 restaurants agaisnt their prices.
    
    The avergae price for having a full meal at each of the restaurants is calculated. The top 5 dishes in terms of health
    metric are taken their average price is calculated.
    """
    plt.rcdefaults()
    #This part of the code reads the individual files for each of the restaurants
    subway = choices_cleaning('Subway')
    arbys = choices_cleaning('arbys')
    cj = choices_cleaning('CarlsJr')
    bk = choices_cleaning('BurgerKing')
    jitb = choices_cleaning('JackInTheBox')
    #Calculates the average price for the best 5 dishes from each of the restaurants.
    res  = [bk,subway,arbys,cj,jitb]
    Restaurants = ['Burger King','Subway','Arbys','Carls Jr','Jack In The Box' ]
    ave_price =  []
    for each in res:
        row = (each['Price'][:5].sum())/5
        ave_price.append(row)

# Plotting the actual horizontal bar graph
        
    y_pos = np.arange(len(Restaurants)) #Deciding the number of entries on the y axis
    Price = ave_price
    
    plt.barh(y_pos, width = Price, align='center', alpha=0.5) #barh makes the bar graph horizontal
    plt.yticks(y_pos, Restaurants)
    plt.xlabel('Average Price per Meal', fontsize = 18)
    #plt.ylabel('Food Chains', fontsize = 20).set_rotation(45)
    
    plt.title('Restaurants' , fontsize = 18)
    plt.savefig("Best vs Price.jpg", bbox_inches='tight') # Saving the image in a file
    
    plt.show() # Showing the plot on the screen
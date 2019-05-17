"""
This file does the web scraping of food nutrition of Whataburger's menu items
and stores it in a csv file

@author: Ritika Prasad
"""

from bs4 import BeautifulSoup, NavigableString
import urllib.request
import csv
import re

nutrition_url = 'https://www3.whataburger.com/food/nutrition'
request = urllib.request.Request(nutrition_url)
response = urllib.request.urlopen(request)

soup = BeautifulSoup(response, 'html.parser')

with open('../NutritionData/Whataburger_NutritionData.csv', 'a', newline="") as csv_file:
	writer = csv.writer(csv_file)
	for index, nutritionContent in enumerate(soup.find_all('div', attrs={'class':'nutrition full'})):
		product = ""
		#getting name of the product
		for divs in nutritionContent.find_previous_siblings('div'):
			p = divs.find("h4")
			if (p):
				product = p.text
		
		headerList = ["Item"]
		rowEntry = [product]
		#getting individual nutritions
		for nutrition in nutritionContent.find_all('span'):
			value = [element for element in nutrition if isinstance(element, NavigableString)][0]
			rowEntry.append(value)
			if(index == 0):
				name = [element for element in nutrition if not isinstance(element, NavigableString)][0].text.strip().replace('\n', ' ')
				name = re.sub(' +', ' ',name)
				headerList.append(name)

		#store it in csv
		if(index == 0):
			writer.writerow(headerList)
		writer.writerow(rowEntry)

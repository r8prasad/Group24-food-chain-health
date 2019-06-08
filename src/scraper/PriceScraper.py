"""
This file does the scraping of pricing of a restaurant's menu items
in a state on https://www.menuwithprice.com/menu-and-price/ and stores 
it in a csv file

@author: Ritika Prasad

"""


from bs4 import BeautifulSoup
import requests
import csv
import re

def price_scraper(url, filename):
	"""
	This function does the web scraping of pricing of restaurant's menu items
	available on https://www.menuwithprice.com/menu-and-price/ and stores it in a csv file
	
	:param: url - url of the website to extract data from
	:type: str

	:param: filename - path of the file where the extracted data will be stored
	:type: str

	:returns: None
	"""

	#assert statements
	assert(isinstance(url, str))
	assert(isinstance(filename, str))

	result = requests.get(url)

	soup = BeautifulSoup(result.content, 'html.parser')

	priceRegExp = r"\$\d+(?:\.\d+)?"

	with open(filename, 'w+', newline="") as csv_file:
		#csv file
		writer = csv.writer(csv_file)
		#write header
		writer.writerow(["Item", "Price"])

		#extract all rows with product and prices
		for tableRow in soup.find_all('tr', attrs={'class':'tr'}):
			
			item = []
			price = ""
			
			for tableData in tableRow.find_all('td'):
				if re.match(priceRegExp, tableData.text):
					price = tableData.text
				else:
					item.append(tableData.text)

			writer.writerow([" ".join(item), price])

#Change price_url and csv_filename as per the restaurant
price_url = 'https://www.menuwithprice.com/menu/whataburger/'
csv_filename = '../../data/RawPriceData/Whataburger_PriceData.csv'
price_scraper(price_url, csv_filename)

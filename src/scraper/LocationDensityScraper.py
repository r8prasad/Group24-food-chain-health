"""
This file does the scraping of locations of a restaurant in a state
on https://www.google.com/maps and stores it in a csv file

@author: Ritika Prasad

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from gmaps import Geocoding

API_KEY = 'AIzaSyCqhyTMd4ok_gznKz2XCJT_BY5EsIrGKSY'
FOLDER = 'location_extraction_helper'

def __has_numbers(inputString):
	"""
	This function checks if the input string contains numbers

	:param: inputString - input string
	:type: str

	:returns: True/False
	:type: bool

	"""
	assert(isinstance(inputString, str))
	return any(char.isdigit() for char in inputString)

def __extract_restaurant_info(restaurantDiv, state):
	"""
	This function extracts the information of a restaurant from a div element and
	returns it as s dictionary

	:param: restaurantDiv - restaurant div element
	:type: str

	:param: state - name of the state; eg. CA
	:type: str

	:returns: None
	"""
	assert(isinstance(state, str))
	
	location_dict = {}
		
	name = restaurantDiv.find('h3', attrs={'class': 'section-result-title'})
	location_dict['Name'] = name.text.strip()

	stars_div = restaurantDiv.find('span', attrs={'class': 'cards-rating-score'})
	stars = stars_div.text if(stars_div is not None) else "N/A"
	location_dict['Rating'] = stars.strip()

	numRating_div = restaurantDiv.find('span', attrs={'class': 'section-result-num-ratings'})
	numRating = numRating_div.text if(numRating_div is not None) else "N/A"
	location_dict['Number of Ratings'] = numRating.strip()

	location = restaurantDiv.find('span', attrs={'class':'section-result-location'})
	location_dict['Location'] = location.text.strip()

	return location_dict

def __process_extracted_data(results, restaurant, state, extractedDataFile, namesAllowed):
	"""
	This function processes the extracted data using pandas and stores the location density in a csv file

	:param: results - list of dictionary of restaurant location data 
	:type: list
	
	:param: restaurant - name of the restaurant; eg. Pizza Hut
	:type: str

	:param: state - name of the state; eg. CA
	:type: str
	
	:param: extractedDataFile - path of the file where the extracted data will be stored
	:type: str

	:param: namesAllowed - names of the restaurant to qualify as valid results; eg. ['Pizza Hut', 'Pizza Hut Express']
	:type: list

	:returns: None
	"""
	
	#assert statements
	assert(isinstance(results, list))
	assert(isinstance(restaurant, str))
	assert(isinstance(state, str))
	assert(isinstance(extractedDataFile, str))
	assert(isinstance(namesAllowed, list))

	df = pd.DataFrame(results)

	#remove restaurants with other name than the restaurant's name
	df = df[df.Name.isin(namesAllowed)]

	#check if the location is within the state
	#get cities name in a list
	citiesFile = f"{FOLDER}/{state}_cities.txt"
	cities = []
	f = open(citiesFile, "r")
	for line in f.readlines():
		cities.append(line.strip().lower())
	f.close()

	geocodeApi = Geocoding(api_key=API_KEY)
	
	for location in set(df['Location']):
		isLocationValid = False
		
		if(not __has_numbers(location) and location.lower() not in cities):
			isLocationValid = False
		elif(not __has_numbers(location) and location.lower() in cities):
			isLocationValid = True
		else:
			try:
				response = geocodeApi.geocode(location + ', ' + state)
				for address in response[0]['address_components']:
					if(address['types'][0] == 'locality'):
						df.replace(location, address['long_name'])
						location =  address['long_name']
					elif(address['types'][0] == 'administrative_area_level_1'):
						isStateValid = address['short_name'] == state
					elif(address['types'][0] == 'country'):
						isCountryValid = address['short_name'] == 'US'

				isLocationValid = isStateValid and isCountryValid
				
			except:
				isLocationValid = False

		if(not isLocationValid):
			df = df[df.Location != location]
	
	#remove duplicate location using dataframes
	df.drop_duplicates(subset=None, keep='last', inplace=True)

	with open(extractedDataFile, 'a', newline="") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow([restaurant, state, str(len(df))])

def location_scraper(restaurant, state, extractedDataFile, namesAllowed):
	"""
	This function does the scraping of locations of a restaurant in a state
	on https://www.google.com/maps and stores it in a csv file

	:param: restaurant - name of the restaurant; eg. Pizza Hut
	:type: str

	:param: state - name of the state; eg. CA
	:type: str

	:param: extractedDataFile - path of the file where the extracted data will be stored
	:type: str

	:param: namesAllowed - names of the restaurant to qualify as valid results; eg. ['Pizza Hut', 'Pizza Hut Express']
	:type: list

	:returns: None
	"""
	url = 'https://www.google.com/maps'

	browser = webdriver.Chrome()
	browser.get(url)
	time.sleep(1)#wait for the page to load

	#get counties name in a list
	countiesFile = f"{FOLDER}/{state}_counties.txt"
	counties = []
	f = open(countiesFile, "r")
	for line in f.readlines():
		counties.append(line.strip())
	f.close()

	results = []

	for county in counties:
		searchBox = browser.find_element_by_id('searchboxinput')
		searchBox.send_keys(county+"\n")#County name+Enter
		time.sleep(4)#wait for the page to load

		#find nearby button
		buttons = browser.find_elements_by_tag_name('button')
		for button in buttons:
			if button.get_attribute('data-value') == 'Nearby':
				button.click()
				time.sleep(3)#wait for the page to load
				break

		#Enter the name of restaurant on nearby search box and click on search
		searchBox.clear()
		searchBox.send_keys(restaurant+"\n")
		time.sleep(3)#wait for the page to load

		search = True

		while(search):
			soup = BeautifulSoup(browser.page_source, 'html.parser')
			contentExists = False

			for element in soup.find_all('div', attrs={'class': 'section-result-content'}):
				contentExists = True
				location_dict = __extract_restaurant_info(element, state)
				results.append(location_dict)

			if contentExists == False:
				searchBox.clear()
				break#didn't return a table of results 
			else:
				#go to next page
				buttons = browser.find_elements_by_tag_name('button')
				for button in buttons:
					if button.get_attribute('aria-label') and button.get_attribute('aria-label').strip() == 'Next page':
						try:
							button.click()
							time.sleep(3)#wait for the page to load
							break
						except:
							search = False
							searchBox.clear()
							break
	browser.close()
	__process_extracted_data(results, restaurant, state, extractedDataFile, namesAllowed)

location_scraper('Pizza Hut', 'AL', '../../data/LocationData/LocationData.csv', ['Pizza Hut', 'Pizza Hut Express'])
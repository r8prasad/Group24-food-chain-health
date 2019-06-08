The src folder contains all the python scripts (scraping, cleaning, processing, plots). 
The data folder contains all the data needed for the processing.

Steps:
1) Data Scraping: You need to install Chrome webdriver for scraping this
	a) Nutrition scraper file
	   -> location: src/scraper/NutritionScraper.py
	   -> run command: python src/scraper/NutritionScraper.py
	   -> description: The function being called is "nutrition_scraper(nutrition_url, csv_filename)".
					The "nutrition_url" is the url to scrape and "csv_filename" is the file in which
					you are storing the scraped data. The script is calling the function to extract
					Arby's data as an example.
	   -> data generated: data generated is stored in data/RawNutritionData
	b) Price scraper file
	   -> location: src/scraper/PriceScraper.py
	   -> run command: python src/scraper/PriceScraper.py
	   -> description: The function being called is "price_scraper(price_url, csv_filename)".
					The "price_url" is the url to scrape and "csv_filename" is the file in which
					you are storing the scraped data. The script is calling the function to extract
					Whataburger's data as an example.
	   -> data generated: data generated is stored in data/RawPriceData
	c) Location scraper file
	   -> location: src/scraper/LocationDensityScraper.py
	   -> run command: python src/scraper/LocationDensityScraper.py
	   -> description: The function being called is "location_scraper(restaurant, state, extractedDataFile, namesAllowed)".
					The "extractedDataFile" is the file in which you add the a row of the location density found for the
					"restaurant" for that "state". The script is calling the function to extract Pizza Hut's location in 
					Alabama as an example. This file also takes the help of helper files for getting the counties in cities
					in a particular state. The helper files for Alabama is located in src/scraper/location_extraction_helper
					as an example.
	   -> data generated: data generated is stored in data/LocationData

2) Data Cleaning:
	a) Data Clean up file
	   -> location: src/dataProcessing/Price_Processing.py
	   -> run command: python src/dataProcessing/Price_Processing.py
	   -> description: The file reads in the data from "data/CleanedNutritionData" folder and generated a new folder with 
					prices data added to the Items. Running the script once would do the price processing for all our restaurants.
	   -> data generated: data generated is stored in data/NutritionDataWithPrice
3) Processing:
	a) Price Processing
	   -> location: src/dataCleaning/Clean_Data.py
	   -> run command: python src/dataCleaning/Clean_Data.py
	   -> description: The function being called cleans up the Raw Nutrition data in the "data/RawNutritionData" folder.
					Each file in data/RawNutritionData is cleaned one at a time. The script is being called to clean up
					Arby's data as an example.
	   -> data generated: data generated is stored in data/CleanedNutritionData
	b)
	
	
	
	
	c)
4) Plotting:
	a) Healthy vs Unhealthy plot
	   -> location: src/plots/HealthyVsUnhealthy.py
	   -> run command: python src/plots/HealthyVsUnhealthy.py
	   -> description: The file reads in the data from "data/FinalData" folder and plots graph comparing the healthy vs unhealthy
					menu items of the restaurants.
	b) Location Density Plot
	   -> location: src/plot/LocationDensityPlot.py
	   -> run command: python src/plot/LocationDensityPlot.py
	   -> description: The files reads in the data from "data/LocationData/LocationData.csv" and plots graphs comparing the
					location density of unhealthy restaurants across states of US and the trend of a particular disease. 
	c)
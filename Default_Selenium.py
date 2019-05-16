# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:37:58 2019

@author: varad
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def click_simulation():
    """
    Simulate the clicks for the page for the specific page.
    This script is for 
    """
    browser = webdriver.Chrome()
    url = "https://www.bk.com/menu/search-by-nutrition"
#    page = requests.get(url)
    browser.get(url)
    time.sleep(1)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    
    ok = browser.find_element_by_id("btnSubmitSearch")
    ok.click()
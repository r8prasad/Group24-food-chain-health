# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:23:33 2019

@author: varad
"""

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    browser = webdriver.Chrome()
    browser.get("https://www.bk.com/menu/search-by-nutrition")
    time.sleep(1)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    ok = browser.find_element_by_id("btnSubmitSearch")
    ok.click()


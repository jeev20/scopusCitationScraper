# -*- coding: utf-8 -*-
"""
Created on Tue May 27 10:32:55 2020

@author: jeev20

The citation information from Engineering Village is sub-standard. 
This program was created to substitute the data obtained from Engineering Village and improve it by accessing scopus database. 
The program takes article DOI as input parameter and scraps www.scopus.com to download all the information about the article in CSV format. 
If needed, other types of files may also be downloaded (ris, bib, txt, mendeley) with some modifications to "Click on CSV" code line.  
"""
import pandas as pd
import time
import os

# Reading csv file for DOIs
df = pd.read_csv("doi.csv", encoding="utf-8")
DOI = []
for index, row in df.iterrows():
    DOI.append(row['DOI'])
   
newDOI = DOI
print (newDOI) 

# Automating the query
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print ("-------------------------------------------------------------------")
print ("Starting to Scrape. Opening scopus.com. \n")
print ("-------------------------------------------------------------------")
# Necessary to avoid the Download popup in firefox
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir","\Data")

# Now we need to specific the extension of files in MIME types - in our case application/x-bibtex for .bib file extension
# text/csv for comma seperated values and application/x-Research-Info-Systems for RefMan .ris file extension
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/x-bibtex,text/csv,application/x-Research-Info-Systems")

# Calls the webdrive.exe to open firefox
# Webdrivers (.exe) should be located in the same directory. Download link: https://pypi.org/project/selenium/ 
driver = webdriver.Firefox(firefox_profile=fp)
driver.get("https://www.scopus.com/")
driver.maximize_window()

# Waiting to load the page
driver.implicitly_wait(10)

# This will try to close the popup from scopus by clicking guest user
# Xpath can be found by right clicking and inspectin in any website
try:
    driver.find_element_by_id("_pendo-close-guide_").click()
except:
    pass
# Click the advanced menu
driver.current_url
driver.find_element_by_css_selector("#advanceSearchLink > a:nth-child(1) > span:nth-child(1)").click()

count = 0
for i in newDOI:
    # Sometimes the popup may appear again
    try:
        driver.find_element_by_id("_pendo-close-guide_").click()
    except:
        pass

    # Click on query field
    wait = WebDriverWait(driver, 10)  #wait initialize, in seconds
    try:
        wait.until(EC.visibility_of_element_located((By.ID, 'contentEditLabel'))).click()
    except:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#searchfield'))).click()
        
    # selecting the searchterm
    searchterm = "DOI({})".format(i)
    
    # Paste the DOI in the searchterm input box
    searchText = driver.find_element_by_id("searchfield")
    searchText.clear()
    searchText.send_keys(searchterm)  
    time.sleep(0.5)

    # Click on search
    searchButton = "#advSearch > span:nth-child(1)"
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, searchButton))).click()

    # Click on all results
    wait.until(EC.visibility_of_element_located((By.ID, "selectAllCheck"))).click()
    
    # Click export
    wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="export_results"]"""))).click()

    if count == 0:
        """ We only need to define it once since the session cookies remember these choices
            count == 0 is the first DOI in the newDOI
        """
        # Click on CSV radio button
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li.radio-inline:nth-child(5) > label:nth-child(2)"))).click()

        # Click on Bibliographical information
        driver.find_element_by_css_selector("#bibliographicalInformationCheckboxes > span:nth-child(1) > label:nth-child(2)").click()
        
        # Click on Abstracts & keywords 
        driver.find_element_by_css_selector("#abstractInformationCheckboxes > span:nth-child(1) > label:nth-child(2)").click()

        # Click Funding details
        driver.find_element_by_css_selector("#fundInformationCheckboxes > span:nth-child(1) > label:nth-child(2)").click()
    
        # Click Other information
        driver.find_element_by_css_selector("#otherInformationCheckboxes > span:nth-child(1) > label:nth-child(2)").click()

    # Click export button
    driver.find_element_by_css_selector("#exportTrigger > span:nth-child(1)").click()

    # driver.switch_to.alert.accept() # Can be used if other pop ups are raised (.alert.dismiss())
    
    print ("Success: Citation for DOI {} has been downloaded. \n".format(i))
    print ("")
    
    if count == (len(newDOI)-1):
        # Quits / closes the browsers after every download
        driver.quit() 
    else:
        # Click search again
        driver.find_element_by_css_selector("#gh-Search > span:nth-child(1)").click()
    count += 1

print ("Citations downloaded to your Downloads folder and process completed")   
print ("-------------------------------------------------------------------")
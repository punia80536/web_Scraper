

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from openpyxl.workbook import Workbook
import pandas as pd

company_name_list,country_name_list,hall_name_list,contact_no_list,email_list,website_list =[],[],[],[],[],[]

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

w = WebDriverWait(driver, 10)

driver.get("https://www.eurobike.com/en/index-exhibitors")
driver.maximize_window()
i = 1
while i <= 44:
    linklist = []
    driver.get(f"https://www.eurobike.com/en/index-exhibitors/exhibitors/?page={i}")
    allLinks = driver.find_elements(By.TAG_NAME, "a")


    for item in allLinks:
        link = item.get_attribute("href")
    
        if type(link) == str:
            if link.count("exhibitor-detail") == 1:
                linklist.append(link)

    for item in linklist:

        driver.get(item)
        company_name = driver.find_element(By.CSS_SELECTOR,"h1[class='underlined']").text
        country = driver.find_element(By.CSS_SELECTOR,"div[class='headline__inner'] h3").text
        hall_name = driver.find_element(By.CSS_SELECTOR,"section[class='module'] h2[class='underlined']").text
        w.until(EC.presence_of_element_located((By.CLASS_NAME,"profile__items")))
        contactlinks = driver.find_elements(By.TAG_NAME,"a")

        for index,item in enumerate(contactlinks):
            link = item.get_attribute("href")
        
            if type(link) == str:
                
                if link.count("tel:") == 1:
                    contact_no =link.removeprefix("tel:").replace(" ","").replace("-","").replace(".","").replace("(","").replace(")","")
                    
                if link.count("mailto:") == 1:
                    
                    email = link.removeprefix("mailto:")
                    website = contactlinks[index+1].get_attribute("href")
    
        company_name_list.append(company_name) 
        country_name_list.append(country)
        hall_name_list.append(hall_name)
        contact_no_list.append(contact_no)
        email_list.append(email)
        website_list.append(website)    
    i += 1

col1,col2,col3,col4,col5,col6 = "Company Name","Country","Hall","Contact No","Email Address","Website"
data = pd.DataFrame({col1:company_name_list,col2:country_name_list,col3:hall_name_list,col4:contact_no_list,col5:email_list,col6:website_list})
data.to_excel('scraped_data.xlsx', sheet_name ='sheet1', index = False)

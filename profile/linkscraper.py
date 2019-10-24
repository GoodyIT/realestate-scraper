import csv
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pdb

with open(parameters.parcel_data, 'r') as f:
    parcelid = []
    for line in f:
        # if 'Parcel' in line:
        #     p = line.split('l:')[1].strip()
        parcelid.append(line)

# pdb.set_trace()
rootpath = os.path.abspath(os.path.dirname(__file__))
driverpath = os.path.join(rootpath,'chromedriver')

# defining new  variable passing two parameters
writer = csv.writer(open(parameters.link_file, 'w'))

# writerow() method to the write to the file object
writer.writerow(['ParcelID', 'Mailing Address', 'Property Address', 'Cordinate Info'])

# specifies the path to the chromedriver.exe

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(driverpath, options = options )
wait = WebDriverWait(driver,3)


print("Loading Page ...")
# driver.get method() will navigate to a page given by the URL address
driver.get(parameters.map_link)
sleep(3)

wait = WebDriverWait(driver, 30)
element = wait.until(EC.element_to_be_clickable((By.ID, 'disclaimerContent')))

# locate accept terms check box
acceptChekbox = driver.find_element_by_xpath('//*[@data-dojo-attach-point="acceptButton"]')
# checkbox
acceptChekbox.click()

# sleep for 0.5 seconds
sleep(2)

# locate search by parcel ID
parcelForm = driver.find_elements_by_xpath('//*[@class="accordion-section"]')

# click to inside the form
parcelForm[0].click()
sleep(3)

parcelselect = driver.find_element_by_xpath('//*[@value="Parcel ID"]')
parcelselect.click()
sleep(0.5)

# locate search form to input the parcel id
parcelSearch = driver.find_element_by_xpath('//*[@class="input-group-input"]')
print("Sraping data in progres ...")

# assigning the source code for the web page to variable sel

for i in (range(len(parcelid))):
    
    # Input the parcel ID
    parcelSearch.send_keys(parcelid[i])
    sleep(0.5)
    parcelSearch.send_keys(Keys.RETURN)
    sleep(5)
    
    wait = WebDriverWait(driver, 30)
    element = wait.until(EC.visibility_of_element_located((By.ID, 'dijit__WidgetBase_2')))
    widget = driver.find_element_by_xpath('//*[@data-widget-name="GoogleStreetView"]')
    webdriver.ActionChains(driver).move_to_element(widget ).click(widget).perform()
    sleep(5)
          
 
    coordinate = driver.find_element_by_xpath('//*[@data-dojo-attach-point="coordinateInfo"]')
    coordinate_info = coordinate.text
    
    try:
        driver.find_elements_by_xpath("//*[contains(@class, 'modal-overlay is-active')]//button[@class='btn btn-small']")[-1].click()
        sleep(1)
        driver.find_elements_by_xpath("//*[contains(@class, 'modal-overlay is-active')]//button[@class='btn btn-small']")[-1].click()
        parcelID = parcelid[i]
    except:
        pass
    
    mailing_address = "No result"
    property_address = "No result"
    try: 
        parcel = driver.find_element_by_xpath('//*[@class="dgrid-cell dgrid-cell-padding dgrid-column-1 field-PARCEL_ID"]')
        parcelID = parcel.text
        try:     
            mailingaddress = driver.find_element_by_xpath('//*[@class="dgrid-cell dgrid-cell-padding dgrid-column-4 field-ADDR"]')
            mailing_address = mailingaddress.text
        except:
            mailing_address = "No result"
            
        try: 
            propertyaddress = driver.find_element_by_xpath('//*[@class="dgrid-cell dgrid-cell-padding dgrid-column-1 field-PARCEL_ID"]')
            property_address = propertyaddress.text
        except:
            property_address = "No result"
    except:
        pass
        
        
    # locate search by parcel ID
    # parcelForm = driver.find_elements_by_xpath('//*[@class="accordion-section"]')

    # # click to inside the form
    # parcelForm[1].click()
    # sleep(1)

    parcelselect = driver.find_element_by_xpath('//*[@class="input-group-input"]')
    parcelselect.click()
    parcelselect.clear()
    # sleep(0.5)
    
    
    print("Scraped " + parcelid[i])
  
    # writing the corresponding values to the header
    writer.writerow([parcelid[i],
                     mailing_address,
                     property_address,
                     coordinate_info
                     ])

# terminates the application
driver.quit()
print("Successfully scraped all data")
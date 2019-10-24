import csv
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os

with open(parameters.parcel_data, 'r') as f:
    parcelid = []
    for line in f:
        if 'Parcel' in line:
            p = line.split('l ')[1].rstrip()
            parcelid.append(p)
rootpath = os.path.abspath(os.path.dirname(__file__))
driverpath = os.path.join(rootpath,'chromedriver')


# Defining new  variable passing two parameters.
writer = csv.writer(open(parameters.value_file, 'w'))

# writerow() method to the write to the file object
writer.writerow(['ParcelID', 'Name', 'PPIN', 'Tax Lien', 'If Tax Paid', 'Property Value'])

# specifies the path to the chromedriver.exe
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(driverpath, options = options )

print("Loading page ...")
# driver.get method() will navigate to a page given by the URL address
driver.get(parameters.value_link)
sleep(3)

print("Sraping data in progres ...")
# locate search form to input the parcel id
parcelSearch = driver.find_element_by_xpath('//*[@name="HTMPARCELNUMBER"]')

for i in (range(len(parcelid))):
    # Input the parcel ID
    parcelSearch.send_keys(parcelid[i])
    sleep(0.5)
    parcelSearch.send_keys(Keys.RETURN)
    sleep(5)
    
    # xpath to extract the text from the class containing the bg color
    table_content = driver.find_element_by_xpath('//*[@bgcolor="#FFFFFF"]/td/a').get_attribute('href')

    property_url = driver.get(table_content)
    sleep(3)

    # assigning the source code for the web page to variable sel
    sel = Selector(text=driver.page_source)
    sleep(0.5)

    # xpath to extract the text from the class containing the name
    tables = driver.find_elements_by_xpath('//body[@bgcolor ="#FFFFFF"]/table')
    for table in tables:
        tbodies = table.find_elements_by_tag_name('tbody')
        contents = []
        for tbody in tbodies:
            content = (tbody.text)
            contents.append(content)
            
    textstring = " ".join(contents)
    try:
        property_value = int((textstring.split('TOTAL VALUE:')[1]).split('   ASSESSED :')[0])
    except IndexError:
        property_value  = 'No Result'
    try:
        ppin = (textstring.split("PPIN   ")[1].split("   ")[0])
    except IndexError:
        ppin = 'No Result'
    try:
        record1 = textstring.split("PPIN   ")[1].split("Tax Paid(Y/N)")[1].split("2016  ")[0]
    except IndexError:
        record1 = 'No Result'
    try:
        name = record1.split("   ")[0].split("  ")[1]
    except IndexError:
        name = 'No Result'
    nameholder = name.count('Tax')
    if nameholder > 0:
        name = 'No Result'
    else:
        name = name
    try:
        tax = record1.split("   ")[1].split("  ")[0].strip('\n')
    except IndexError:
        tax = 'No Result'
    try:
        iftaxpaid = textstring.split("Tax Paid(Y/N)")[1].split("  ")[6].split(' ')[0]
    except IndexError:
        iftaxpaid = 'No Result'
    try:
        parcelno =  (textstring.split('PARCEL ')[1]).split('   ')[0].strip('\n')
 
    except IndexError:
        parcelno = parcelid[i]

    print("Scraped " + parcelno)
    
    # writing the corresponding values to the header
    # encoding with utf-8 to ensure all characters get loaded
    writer.writerow([parcelno,
                     name,
                     ppin,
                     tax,
                     iftaxpaid,
                     property_value])
    
  
    # driver.get method() will navigate to a page given by the URL address
    driver.get(parameters.value_link)
    sleep(3)


    # locate search form to input the parcel id
    parcelSearch = driver.find_element_by_xpath('//*[@name="HTMPARCELNUMBER"]')

# terminates the application
driver.quit()

print("Successfully scraped all data")


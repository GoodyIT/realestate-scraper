import csv
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import pandas

data = pandas.read_csv('data/value.csv')
names = data.Name.tolist()
print("Names to be searched loaded")

rootpath = os.path.abspath(os.path.dirname(__file__))
driverpath = os.path.join(rootpath,'chromedriver')


# defining new  variable passing two parameters
writer = csv.writer(open(parameters.lien_file, 'w'))


# writerow() method to the write to the file object
writer.writerow(['Name', 'If military', 'Lis Pendens', 'Fed Tax Liens', 'Construction Liens' ,'Total Points'])

# specifies the path to the chromedriver.exe
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(driverpath, options = options)


print("Scraper started")
print("Loading page ...")
# driver.get method() will navigate to a page given by the URL address
driver.get(parameters.lien_link)
sleep(3)

print("Sraping data in progres ...")
# locate search form to input the parcel id
parcelSearch = driver.find_element_by_xpath('//*[@name="gname"]')

for i in (range(len(names))):
    # Input the parcel ID
    parcelSearch.send_keys(names[i])
    sleep(0.5)
    parcelSearch.send_keys(Keys.RETURN)
    sleep(3)
    
    # xpath to extract the text from the class containing the name
    tables = driver.find_elements_by_xpath('//*[@id="content"]//table')
    for table in tables:
        tbodies = table.find_elements_by_tag_name('tbody')
        contents = []
        for tbody in tbodies:
            content = (tbody.text)
            contents.append(content)
            
    textstring = " ".join(contents)

    textstring  =  textstring.strip('\n')

    records = int(textstring.split('  ')[1].split(' ')[0])
    liens = ''
    military = 0
    lispendens= 0
    fedtaxliens = 0
    constructionliens = 0
    numberpoint = 0
    if records > 0:
        liens = (textstring.split('  ')[1].split('Type\n')[1])
        military = liens.count('MILITARY DISCHARGE')
        if military > 0:
            military = 1
        else:
            military = 0
        lispendens = liens.count('LIS PENDENS')
        if lispendens > 0:
            lispendens = 1
        else:
            lispendens= 0
        fedtaxliens = liens.count('FEDERAL TAX LIEN')
        if fedtaxliens > 0:
            fedtaxliens = 1
        else:
            fedtaxliens = 0
        constructionliens = liens.count('CONSTRUCTION LIEN')
        if constructionliens > 0:
            constructionliens = 1
        else:
            constructionliens = 0
        
        numberpoint = military + lispendens + fedtaxliens + constructionliens
     
    # writing the corresponding values to the header
    # encoding with utf-8 to ensure all characters get loaded
    writer.writerow([names[i], military, lispendens, fedtaxliens, constructionliens, numberpoint])
    
    
    # driver.get method() will navigate to a page given by the URL address
    driver.get(parameters.lien_link)
    sleep(3)
    print("Scraped " + names[i])
    

    # locate search form to input the parcel id
    parcelSearch = driver.find_element_by_xpath('//*[@name="gname"]')

# terminates the application
driver.quit()
print("Successfully scraped all data")

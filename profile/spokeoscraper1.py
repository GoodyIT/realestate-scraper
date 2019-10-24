import csv
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json 
import pandas
import pdb
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
rootpath = os.path.abspath(os.path.dirname(__file__))
# driverpath = os.path.join(rootpath,'chromedriver')
driverpath = os.path.join(rootpath,'geckodriver')


# defining new  variable passing two parameters
writer = csv.writer(open(parameters.spokeo_file, 'w'))

# writerow() method to the write to the file object
writer.writerow(['Name' , 'Age', 'Gender', 'Marital Status', 'Email Address', 'Phone Numbers', 'Number of home owned','Year Built', 'County Court Record', 'State Court Record',  'Nationwide Court Record', 'If Arrested'])
    
# specifies the path to the chromedriver.exe
options = Options()
# options.add_argument('--headless')
# options.headless = True
# driver = webdriver.Chrome(driverpath, options = options)
driver = webdriver.Firefox(executable_path=driverpath, options = options)
wait = WebDriverWait(driver,10)
print("Spokeo web scraper started")
# driver.get method() will navigate to a page given by the URL address
driver.get(parameters.spokeo_link)
print("Login in spokeo")
# locate email form by_class_name
username =  WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

# send_keys() to simulate key strokes
username.send_keys(parameters.spokeo_username)

# sleep for 0.5 seconds
# sleep(0.5)

# locate password form by_class_name
password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

# send_keys() to simulate key strokes
password.send_keys(parameters.spokeo_password)
# sleep(0.5)
password.send_keys(Keys.RETURN)
sleep(0.5)

# driver.get method() will navigate to a page given by the URL address
# driver.get('https://www.spokeo.com')
# sleep(1)


data = pandas.read_csv('data/value.csv', sep='\n')
names = data.Name.tolist()
print("Names to be searched loaded")
for i in (range(len(names))):
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.spokeo.com')
    sleep(1)
    # locate search form by_name
    # search_query = driver.find_element_by_xpath('//*[@class="css-1p36r7s e1bo1fwa3"]')
    search_query = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="css-1p36r7s e1bo1fwa3"]'))
    )
    # send_keys() to simulate the search text key strokes
    search_query.send_keys(names[i])
    # sleep(0.5)
    # .send_keys() to simulate the return key
    search_query.send_keys(Keys.RETURN)
    # sleep(3)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-view')))
    except:
        pass
    # assigning the source code for the web page to variable sel
    sel = Selector(text=driver.page_source)
    
    # xpath to extract the personal content from the carousel 
    search_content = driver.find_element_by_xpath("//*[@name='description']").get_attribute("content")
    try:
        search_content = int((search_content.split(' ')[0]))
    except ValueError:
        search_content == 0
        
    if search_content == 0:
        # driver will navigate to a page given by the URL address
        # driver.get('https://  www.spokeo.com')
        # sleep(1)
        pass
    else:
        # locate URL by_class_name
        spokeo_urls = driver.find_elements_by_xpath('//*[@class="single-column-list"]/*[contains(@class, "single-column-list-item")]')
        url_list =[]
        for spokeo_url in spokeo_urls:
            url_item = spokeo_url.get_attribute('href')
            url_list.append(url_item)
        # sleep(1)
   
        for url in url_list:
            try:
                urlmatch = url.split('/')[4]
            except:
                pdb.set_trace()
            # pdb.set_trace()
            print('urlmatch === ', urlmatch, ' -- url', url)
    
            if urlmatch == 'Colorado':
                print("found Colorado in ", url)
                driver.get(url)
                sleep(3)
    
                # xpath to extract the personal content from the carousel 
                pdb.set_trace()
                try:
                    data_content = driver.find_element_by_xpath("//*[@data-react-class='packs/v10/premium/ultimate_profile/containers/UltimateProfile']").get_attribute("data-react-props")
                except:
                    continue

                dict_content = json.loads(data_content)
                try:
                    name = (dict_content['profile']['full_name'])
                except KeyError:
                    name = 'No Result'
                try:
                    age = (dict_content['profile']['age'])
                except KeyError:
                    age = 'No Result'
                try:
                    gender = (dict_content['profile']['gender'])
                except KeyError:
                    gender = 'No Result'
                try:
                    marital_status = (dict_content['profile']['marital_status'])
                except KeyError:
                    marital_status = 'No Result'
                home_owned = (len(dict_content['profile']['locations']))
                try:
                    mylist = (dict_content['locations']['data_cards'])
                    year_built = mylist[0]['attributes']['year_built']['year']
                except KeyError:
                    year_built = 'No Result'
                email_list = (dict_content['contact']['emails'])
                emails = []
                for e_list in email_list:
                    email = (e_list['email_address'])
                    emails.append(email)
                emails = ' '.join(emails)
                
                phones = (dict_content['contact']['phones'])
                phone_numbers = []
                for phone in phones:
                    phone_number = (phone['number'])
                    phone_numbers.append(phone_number)
                phone_numbers = ', '.join(phone_numbers)
                   
            
                # assignment of the current URL
                spokeo_url = driver.current_url
                
                courts = driver.find_elements_by_xpath("//*[@class ='app_content_up profile-section court ']")
                court_data = []
                for court in courts:
                    elem = court.text
                    court_data.append(elem)
                court_string = " ".join(court_data)
                try:
                    county_result = court_string.split('States')[0].split('Residence|')[1]
                    county_result = county_result.count('No ')
                    if county_result > 0:
                        county_result = 0
                except IndexError:
                    county_result = 1
                try:
                    states_result = court_string.split('Nationwide')[0].split('Residence|')[1]
                    states_result = states_result.count('No ')
                    if states_result > 0:
                        states_result = 0
                except IndexError:
                    states_result = 1
                try:
                    nationwide_result = court_string.split('DISCLAIMER')[0].split(' Search|')[1]
                    nationwide_result = nationwide_result.count('No ')
                    if nationwide_result > 0:
                        nationwide_result = 0
                except IndexError:
                    nationwide_result = 1
                arrested = states_result + county_result + nationwide_result
                if arrested > 0:
                    if_arrested = 1
                else :
                    if_arrested = 0
                # writing the corresponding values to the header
                # encoding with utf-8 to ensure all characters get loaded
                writer.writerow([names[i],
                                 age,
                                 gender,
                                 marital_status,
                                 emails,
                                 phone_numbers,
                                 home_owned,
                                 year_built,
                                 county_result,
                                 states_result,
                                 nationwide_result,
                                 if_arrested])
            else:
                print('not found Colorado')
        print("Scraped " + names[i])        
print("Successfully scraped all names")           
# terminates the application
driver.quit()
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

# make selenium driver
svc=  Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=svc)
driver.maximize_window()

# final list all amplitude mentions
call_urls = []
data_tracked = []
# input URL
driver.get("https:www.kahoot.it")

time.sleep(2)

links = driver.find_elements(By.TAG_NAME, 'a')
link_xpath = ['', '', '']
buttons = driver.find_elements(By.TAG_NAME, 'button')

# fill in name
ID_field = driver.find_element(By.NAME, 'gameId')
ID_field.send_keys('1235')
time.sleep(2)

j = 0
while (j < len(links)):
    link_xpath[j] = links[j].get_attribute('xpath')
    j = j + 1

for i in buttons:
    i.click()

for i in links:
    try:
        i.click()
    except:
        call_urls.append("ERROR")
        data_tracked.append("ERROR")
    driver.back()


for request in driver.requests:
    if request.response:
        if ('amplitude' in str(request.url)):
            call_urls.append(request.url)
            if("api" in str(request.url)):
                body = str(request.body).split('&')
                information = urllib.parse.unquote(body[2])
                print("This is an api call that tracks information, AMPL is tracking at " + request.url)
                data_tracked.append(information)
            else:
                print("We noticed that amplitude is called at " + request.url)
                data_tracked.append('')

time.sleep(2)

# print final output
print("Here's my final amplitude list:")
print(call_urls)
print(data_tracked)
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time

from selenium.webdriver.chrome.service import Service

# make selenium driver
svc=  Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=svc)
driver.maximize_window()

# final list all amplitude mentions
call_urls = []
data_tracked = []
# input URL
driver.get("https:www.kahoot.it")

# init requests
for request in driver.requests:
    if request.response:
        if ('amplitude' in str(request.url)):
            call_urls.append(request.url)
            data_tracked.append('')
            # print(str(request.body).split('&'))
            print(
                request.url,
            )
            # print(request.response)
            # print("found an ampl" + str(request.url))
            # print(request.response)

time.sleep(2)

#  populate game ID
ID_field = driver.find_element(By.NAME, 'gameId')
ID_field.send_keys('1235')
time.sleep(2)

# click the submit button
button = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div[3]/div[2]/main/div/form/button')
button.click()

for request in driver.requests:
    if request.response:
        if ('amplitude' in str(request.url)):
            call_urls.append(request.url)
            if("api" in str(request.url)):
                body = str(request.body).split('&')
                information = urllib.parse.unquote(body[2])
                print("This is an api call that tracks information, AMPL is tracking at" + request.url)
                data_tracked.append(information)
            else:
                print("We noticed that amplitude is called at" + request.url)
                data_tracked.append('')

time.sleep(2)

# print final output
print("Here's my final amplitude list:")
print(call_urls)
print(data_tracked)

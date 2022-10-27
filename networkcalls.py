from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.chrome.service import Service

# make selenium driver
svc=  Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=svc)
driver.maximize_window()

# final list all amplitude mentions
list = []

# input URL
driver.get("https:www.kahoot.it")

# init requests
for request in driver.requests:
    if request.response:
        if ('amplitude' in str(request.url)):
            list.append(request.url)
            print(request)
            # print("found an ampl" + str(request.url))
            # print(request.response)
        # # print(
        # #     request.url,
        #     request.response
        # #     # request.headers,
        # #     # request.response.headers
        # # )
time.sleep(4)

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
            list.append(request.url)
        print(
            request.url,
            # request.response.status_code,
            # request.headers,
            # request.response.headers
        )
time.sleep(2)

# print final output
print("Here's my final amplitude list:")
print(list)

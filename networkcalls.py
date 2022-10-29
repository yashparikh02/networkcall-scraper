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

# final list of all amplitude mentions
call_urls = []
urls_no_back = []
data_tracked = []
data_no_back = []

# input URL
driver.get("https:www.kahoot.it")

time.sleep(2)

# find all the clickable elements using html (for links, look for the tag name <a>; for buttons, look for tag <button>)
links = driver.find_elements(By.TAG_NAME, 'a')
buttons = driver.find_elements(By.TAG_NAME, 'button')

# final list of all clickable elements (in a readable form)
clickables = []

# converts the links and buttons from web element form to their respective titles for readability
for i in links:
    clickables.append(i.text)
for i in buttons:
    clickables.append(i.text)

# fill in name (kahoot specific: done so that "Enter" button can be pressed)
ID_field = driver.find_element(By.NAME, 'gameId')
ID_field.send_keys('1235')
time.sleep(2)

# click all buttons
for i in buttons:
    i.click()

# to make sure the banner goes away so the links below are clickable
time.sleep(10)

# click all links
j = 0
while (j < len(links)):
    # update the associated web element (necessary since we go back to the original page from the clicked link)
    element = driver.find_element(By.PARTIAL_LINK_TEXT, clickables[j])
    element.click()
    time.sleep(3)
    # go back to the original page from the link
    driver.back()
    time.sleep(3)
    j = j + 1

# iterate through all requests
for request in driver.requests:
    if request.response:
        # if amplitude is involved in the request url, add the url to call_urls
        if ('amplitude' in str(request.url)):
            call_urls.append(request.url)
            # if amplitude api is involved, append the information stored to data_tracked
            if("api" in str(request.url)):
                body = str(request.body).split('&')
                information = urllib.parse.unquote(body[2])
                # print("This is an api call that tracks information, AMPL is tracking at " + request.url)
                data_tracked.append(information)
            # if api isn't involved, append an empty space to the data tracked (representing no data tracked)
            else:
                # print("We noticed that amplitude is called at " + request.url)
                data_tracked.append('')

# populates the list of amplitude url calls made without including the calls made when we return to the original site
urls_no_back.append(call_urls[0])
for i in call_urls:
    if i != "https://cdn.amplitude.com/libs/amplitude-5.3.0-min.gz.js":
        urls_no_back.append(i)

# populates the list of amplitude url calls made without including the calls made when we return to the original site
data_no_back.append(data_tracked[0])
for i in data_tracked:
    if i != "":
        data_no_back.append(i)

# print final output
print("Here are all the clickable elements on the website: " + str(clickables))

print("Here's my final list of Amplitude calls and data tracked:")
print("Here are all the url calls we make: " + str(call_urls))
print("Here are all the data that we track (indices corresponding to the respective call url): " + str(data_tracked))
print("Here are all the url calls we make, " +
      "not including the calls made when we return to the original site: " + str(urls_no_back))
print("Here are all the data that we track, " +
      "not including the calls made when we return to the original site: " + str(data_no_back))

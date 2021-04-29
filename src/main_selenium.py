import os
from selenium import webdriver
from selenium.common import exceptions
import test_domains as websites
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# TEST using chrome

# Selenium browser driver setup
driver_name = "chromedriver.exe"
PATH = os.path.join(os.getcwd(), driver_name)

driver = webdriver.Chrome(PATH)
driver.get(websites.CANVAS_LOGIN)

# Let user log in 
# finish loggin in in 30 seconds, check if successful with url
# TODO: replace with GUI confirm
timeout = 30
print("Please log into page within {} seconds".format(timeout))
try:
    wait = WebDriverWait(driver, timeout) # timeout in 30s
    element = wait.until(EC.url_contains("login_success=1"))
except exceptions.TimeoutException:
    print("Error: did not log in in time")
    driver.quit()
    exit()
print("Successfully logged in\n")

# let user select course
# TODO: replace with GUI confirm course selection
# currently will latch onto first course selected
print("Click on the canvas course to crawl")
try:
    wait = WebDriverWait(driver, 30) # timeout in 30s
    element = wait.until(EC.url_contains("/courses/"))
except exceptions.TimeoutException:
    print("Error: did not choose course in time")
    driver.quit()
    exit()
print("Course selected: {}".format(driver.title))

# strip canvas unique course number
domain_url = driver.current_url
regex = r"(?<=lrccd.instructure.com)[^$]+"
regex_search = re.search(regex, domain_url)
course_number = regex_search.group(0)

# get images and links
css_search =  '[href*="{}"]'.format(course_number)
domain_links = driver.find_elements_by_css_selector(css_search)

driver.quit()
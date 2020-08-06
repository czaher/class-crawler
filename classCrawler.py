'''
Pulls course data from University of Cincinnati's course database.
'''

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
import re

chrome_options = Options()  
chrome_options.add_argument("--headless") 

driver = webdriver.Chrome("chromedriver", options=chrome_options)
driver.get("https://www.classes.catalystatuc.org/psc/psclass/EMPLOYEE/SA/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL")

subjectList = open("subjectList.txt")
subjectArray = subjectList.read().split('\n')

for x in subjectArray:
    print("Entering subject page for: " + x + '\n')

# on search page

    # subject selector
    driver.find_element_by_xpath(
        '//*[@id="SSR_CLSRCH_WRK_SUBJECT_SRCH$0"]').send_keys(x)

    # submit button
    driver.find_element_by_xpath(
        '//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]').click()

    time.sleep(2)

# on class subject page

    # grab source html from subject page
    with open("workingPageSource.html", "w") as f:
        f.write(driver.page_source)

    # open and search html file
    soup = BeautifulSoup(open("workingPageSource.html"), 'lxml')
    classTitles = soup.find_all('td', class_="PAGROUPBOXLABELLEVEL1")
    courseData = soup.find_all('table', class_="PSGROUPBOX")
    try:
        courseDataTable = courseData[2].find_all(
            'tr', id=re.compile(r'^trSSR_CLSRCH_MTG'))
    except:
        print("No course data.\n")

    i = 0
    for n in classTitles:
        print(n.text.strip())

        courseDateTime = courseDataTable[i].find(
            'span', id=re.compile(r'^MTG_DAYTIME'))
        print(courseDateTime.text)

        courseCampus = courseDataTable[i].find(
            'span', id=re.compile(r'^UC_DERIVED_SRCH_DESCR'))
        print(courseCampus.text)

        courseMethod = courseDataTable[i].find(
            'span', id=re.compile(r'^UC_DERIVED_SRCH_DESCR1'))
        print(courseMethod.text)

        courseRoom = courseDataTable[i].find(
            'span', id=re.compile(r'^MTG_ROOM'))
        print(courseRoom.text)

        courseCollege = courseDataTable[i].find(
            'span', id=re.compile(r'^UC_DERIVED_SRCH_DESCR2'))
        print(courseCollege.text)

        courseProf = courseDataTable[i].find(
            'span', id=re.compile(r'^MTG_INSTR'))
        print(courseProf.text)

        courseDates = courseDataTable[i].find(
            'span', id=re.compile(r'^MTG_TOPIC'))
        print(courseDates.text)

        print('\n')
        i = i + 1
    time.sleep(1)

# navigate back to search page
    driver.get(
        "https://www.classes.catalystatuc.org/psc/psclass/EMPLOYEE/SA/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL")
    time.sleep(1)

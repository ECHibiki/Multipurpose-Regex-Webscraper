from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3 as sql

import os
import re
import time
# # instantiate a chrome options object so you can set the size and headless preference https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=720x480")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--remote-debugging-port=9222")
# # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# # current directory
# chrome_driver = os.getcwd() +"\\chromedriver.exe"
# browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

# '''
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.javascriptEnabled"] = False
cap["phantomjs.page.settings.userAgent"] = "Mozilla"
browser = webdriver.PhantomJS(desired_capabilities=cap)

url = input('Enter URL address to rip: ')
pattern = input('Enter regex pattern: ')

sql_con = sql.connect('matches.db')
curs = sql_con.cursor()

if input("Delete store data(type YES): ") == "YES":
    print('Clearing DB')
    curs.execute("DROP TABLE Matches")
    sql_con.commit()
else:
    print('Data will be added to previous sessions')

curs.execute("CREATE TABLE IF NOT EXISTS Matches(matches text PRIMARY KEY, pattern text, site text)")
sql_con.commit()
# \b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b
print('Loading Pseudo-browser...')

browser.get(url)
matches = re.findall(pattern, browser.page_source)
print(browser.page_source)
print(matches)
print(time.time())
# '''
# browser.get('https://free-proxy-list.net/')
# match = re.findall(, browser.page_source)
# print(match)
# print(time.time())

# browser.get('https://www.4chan.org/banned')
# print(browser.page_source)

insert_string = []
for match in matches:
    found = False
    for insert_item in insert_string:
        if insert_item.find(match) > -1:
            found = True
            break
    if not found:
        insert_string.append("('" + match + "','" + pattern + "','" + url + "')")
if len(matches) > 0:
    insert_string = ','.join(insert_string)
    print(insert_string )
    curs.execute("INSERT OR IGNORE INTO Matches VALUES " + insert_string)
    sql_con.commit()

curs.execute("SELECT * FROM Matches")
items = curs.fetchall()
match_file = open('matches.txt', 'w')
match_file.write("\tMatch\t\t\t\t\t\tPattern\t\t\t\t\t\t\t\t\tURL\n")
for item in items:
    print(',\t'.join(item))
    match_file.write(',\t\t'.join(item) + "\n")
match_file.close()
sql_con.close()
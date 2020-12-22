import sys
from selenium import webdriver
import urllib
from random import randint
import smtplib
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-notifications")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.implicitly_wait(30)

ep = 0
df = pd.DataFrame()
print('Enter Start Mumber')
s = int(input())
print("Enter End Number")
e = int(input())
print('Scraping Results')
for b_id in range(s,e+1):
  ep = b_id
  try:
    url = "https://www.goodreads.com/book/show/"+str(b_id)
    uro = urllib.request.urlopen(url)
    driver.get(uro.geturl())
    bs = BeautifulSoup(driver.page_source,features='lxml')
    data_dict = {}
    title = bs.find(id="bookTitle").text.strip()
    data_dict.update({"BOOK TITLE":title})
    data_dict.update({"BOOK GOODREADS URL":uro.geturl()})
    try:
      img_url = bs.find('img',id="coverImage")['src']
      data_dict.update({"COVER IMAGE URL":img_url})
    except:
      None
    author = bs.find_all('a',class_="authorName")
    try:
      pub_rows = bs.find(id='details').find_all('div',class_=['row'])
      pub = "".join(list([s.contents[0].string.strip() for s in pub_rows if 'Published' in s.text]))
    except:
      None


    df = df.append([data_dict])
  except urllib.error.HTTPError as ex:
    continue
  except Exception as e:
    print('Script Stopped at',b_id)
    driver.quit()
    print('Sleep')
    time.sleep(20)
    b_id = b_id - 1
    print('Scraping')
    continue
driver.quit()
print("Generating Excel")
fn = str(s)+"_"+str(ep)+"_results.xlsx"
df.to_excel(fn,index=False)
print("Closed")


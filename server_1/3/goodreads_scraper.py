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

def start():
  global driver
  chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
  driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
  driver.implicitly_wait(30)

def send_mail(msg):
  gmail_user = 'chapabrigade@gmail.com'
  gmail_password = 'asddsaasddsa12'
  sent_from = gmail_user
  to = 'haseebahmadkt@gmail.com'
  subject = 'Script Alert'
  body = msg
  email_text = "\r\n".join(["From: "+sent_from,"To: "+to,"Subject: "+subject,"",msg])
  try:
      server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      server.ehlo()
      server.login(gmail_user, gmail_password)
      server.sendmail(sent_from, to, email_text)
      server.close()
      print("MAIL SENT!")
  except Exception as e:
    print("Sending Mail Failed")
    print(e)

def scrape():
  global driver
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
      try:
        published_date = pub.split('Published')[-1].split('by')[0].strip()
        data_dict.update({"PUBLISHED DATE":published_date})
      except:
        None
      try:
        publisher = pub.split('by')[-1].strip()
        data_dict.update({'PUBLISHER':publisher})
      except:
        None
      try:
        pages = bs.find('span',itemprop="numberOfPages").text.strip()
        data_dict.update({"PAGES":pages})
      except:
        None
      try:
        desc = bs.find(id="description").find_all('span')[-1].text
        data_dict.update({'DESCRIPTION':desc})
      except:
        None
      try:
        isbn = bs.find(class_=['infoBoxRowTitle'],text='ISBN').find_next_sibling('div').text.strip()
        isbn = " ".join(isbn.split())
        data_dict.update({"ISBN":isbn})
      except:
        None
      try:
        lang = bs.find(class_=['infoBoxRowTitle'],text='Edition Language').find_next_sibling('div').text.strip()
        data_dict.update({"LANGUAGE":lang})
      except:
        None

      try:
        amz_url = "http://goodreads.com"+get_urls.find('a',text='Amazon')['href']
        data_dict.update({"AMAZON LINK":amz_url})
      except:
        None
      try:
        adb_url = "http://goodreads.com"+get_urls.find('a',text='Audible')['href']
        data_dict.update({"AUDIBLE LINK":adb_url})
      except:
        None
      try:
        bernes = "http://goodreads.com"+get_urls.find('a',text='Barnes & Noble')['href']
        data_dict.update({"BERNES & NOBLE LINK":bernes})
      except:
        None
      try:
        wal_url = "http://goodreads.com"+get_urls.find('a',text='Walmart eBooks')['href']
        data_dict.update({"WALMART EBOOKS LINK":wal_url})
      except:
        None
      try:
        app_url = "http://goodreads.com"+get_urls.find('a',text='Apple Books')['href']
        data_dict.update({"APPLE BOOKS LINK":app_url})
      except:
        None
      try:
        google_url = "http://goodreads.com"+get_urls.find('a',text='Google Play')['href']
        data_dict.update({"GOOGLE PLAY LINK":google_url})
      except:
        None
      try:
        abebooks = "http://goodreads.com"+get_urls.find('a',text='Abebooks')['href']
        data_dict.update({"ABEBOOKS LINK":abebooks})
      except:
        None
      try:
        depost_url = "http://goodreads.com"+get_urls.find('a',text='Book Depository')['href']
        data_dict.update({"BOOK DEPOSITORY LINK":depost_url})
      except:
        None
      try:
        alibris = "http://goodreads.com"+get_urls.find('a',text='Alibris')['href']
        data_dict.update({"ALIBRIS LINK":alibris})
      except:
        None
      try:
        indigo = "http://goodreads.com"+get_urls.find('a',text='Indigo')['href']
        data_dict.update({"INDIGO LINK":indigo})
      except:
        None
      try:
        better_url = "http://goodreads.com"+get_urls.find('a',text='Better World Books')['href']
        data_dict.update({"BETTER WORLD BOOKS LINK":better_url})
      except:
        None
      try:
        libraries = "http://goodreads.com"+get_urls.find('a',text='Libraries')['href']
        data_dict.update({"LIBRARIES LINK":libraries})
      except:
        None
      try:
        indie = "http://goodreads.com"+get_urls.find('a',text='IndieBound')['href']
        data_dict.update({"INDIEBOUND LINK":indie})
      except:
        None
      
      if author is not None:
        authors = [[x.text,x['href']] for x in author]
        at = 0
        while at < len(authors):
          data_dict.update({'AUTHOR NAME '+str(at+1):authors[at][0]})
          url2 = authors[at][1]
          r = requests.get(url2)
          bs = BeautifulSoup(r.content,features='lxml')
          try:
            author_born = bs.find(class_=['dataTitle'],text='Born').next_sibling.string.strip()
            data_dict.update({"AUTHOR BORN "+str(at+1):author_born})
          except:
            None
          try:
            author_site = bs.find(class_=['dataTitle'],text='Website').find_next(class_=['dataItem']).a.text
            data_dict.update({"AUTHOR WEBSITE "+str(at+1):author_site})
          except:
            None
          try:
            author_twitter = bs.find(class_=['dataTitle'],text='Twitter').find_next(class_=['dataItem']).a.text
            data_dict.update({"AUTHOR TWITTER "+str(at+1):author_twitter})
          except:
            None
          try:
            author_genre = bs.find(class_=['dataTitle'],text='Genre').find_next(class_=['dataItem']).text.strip()
            data_dict.update({'AUTHOR GENRE '+str(at+1):author_genre})
          except:
            None
          try:
            mem_since = bs.find(class_=['dataTitle'],text='Member Since').find_next(class_=['dataItem']).text
            data_dict.update({'MEMBER SINCE '+str(at+1):mem_since})
          except:
            None
          try:
            author_desc = bs.find(class_=['aboutAuthorInfo']).find_all('span')[-1].text
            data_dict.update({'AUTHOR DESCRIPTION '+str(at+1):author_desc})
          except:
            None
          data_dict.update({"AUTHOR GOODREADS URL "+str(at+1):url2})
          at = at + 1


      df = df.append([data_dict])
    except urllib.error.HTTPError as ex:
      continue
    except Exception as e:
      msg = "UBUNTU Server 1 Instance 3 Stopped at "+str(b_id)+" \n\n Error Message:"+str(e)
      print('Script Stopped at',b_id)
      send_mail(msg)
      driver.quit()
      print('Sleep')
      time.sleep(20)
      start()
      b_id = b_id - 1
      print('Scraping')
      continue
  driver.quit()
  print("Generating Excel")
  fn = str(s)+"_"+str(ep)+"_results.xlsx"
  df.to_excel(fn,index=False)
  msg = "UBUNTU Server 1 Instance 3 Completed at "+str(b_id)+" \n\n Sucess"
  send_mail(msg)
  print("Closed")

start()
scrape()


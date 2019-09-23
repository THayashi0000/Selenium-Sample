from tqdm import tqdm_notebook as tqdm
from selenium import webdriver
import pandas as pd
import time

#Access to page
browser = webdriver.Chrome('/usr/local/bin/chromedriver') # DO NOT FORGET to set path
url = "http://b.hatena.ne.jp/search/text?safe=on&q=Python&users=1500"
browser.get(url)
df = pd.DataFrame()
#Insert title,date,bookmarks into CSV file
page = 1 #This number shows the number of current page later
while True: #continue until getting the last page
   if len(browser.find_elements_by_link_text("次のページ")) >= 0:
       print("######################page: {} ########################".format(page))
       print("Starting to get posts...")
       #get all posts in a page
       posts = browser.find_elements_by_css_selector(".bookmark-item")
       for post in posts:
           title = post.find_element_by_css_selector("h3").text
           date = post.find_element_by_css_selector(".entry-contents-date").text
           bookmarks = post.find_element_by_css_selector(".centerarticle-users").text
           se = pd.Series([title, date, bookmarks],['title','date','bookmarks'])
           df = df.append(se, ignore_index=True)
       if len(browser.find_elements_by_link_text("次のページ")) == 0:
            break
       #after getting all posts in a page, click pager next and then get next all posts again
       btn=browser.find_elements_by_link_text("次のページ")[0].get_attribute("href")
       print("next url:{}".format(btn))
       browser.get(btn)
       page+=1
       browser.implicitly_wait(1)
       print("Moving to next page......")
       time.sleep(1)
print(df)
df.to_csv("trend.csv")
print("DONE")

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
import time
from tqdm import tqdm


a = list(np.array(pd.read_csv("notice_no.csv")))
notices=[]
for i in a:
    x = str(i).replace("[","").replace("]","").replace("#","").replace("'","")
    notices.append(int(x))

data=pd.DataFrame()
unopened=[]
browser = webdriver.Chrome()
for i in tqdm(range(0,len(notices)+1),unit="notice"):
    try:
        code = notices[i]
        url = "https://www.sahibinden.com/"+str(code)
        browser.get(url)
        time.sleep(4)
        price = browser.find_element_by_xpath("/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/h3")
        f = price.text
        location = browser.find_element_by_xpath("/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/h2/a[2]")
        k = location.text
        x = browser.find_element_by_css_selector("ul[class='classifiedInfoList']")
        h = x.text
        ho = "Location\n" + str(k) +"\n" + "Price\n" + str(f) + "\n" + h
        hom = ho.replace("\n", ",")
        home = hom.split(",")
        key = home[::2]
        value = home[1::2]
        d = dict(zip(key, value))
        data = data.append(d, ignore_index=True)
    except NoSuchElementException:
        unopened.append(str(code))
        print(len(unopened))
        print(unopened)
data.to_csv("scraped_notice.csv", index=False, encoding="utf-8")

browser.close()
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np
from tqdm import tqdm
districts=["adalar","arnavutkoy","atasehir","avcilar","bagcilar","bahcelievler","bakirkoy",
         "basaksehir","bayrampasa","besiktas","beykoz","beylikduzu","beyoglu","buyukcekmece",
         "catalca","cekmekoy","esenler","esenyurt","eyupsultan","fatih","gaziosmanpasa","gungoren",
         "kadikoy","kagithane","kartal","kucukcekmece","maltepe","pendik","sancaktepe","sariyer",
         "sile","silivri","sisli","sultanbeyli","sultangazi","tuzla"]

types = ["daire","residence","mustakil-ev","villa","ciftlik-evi","kosk-konak",
       "yali","yali-dairesi","yazlik","prefabrik-ev","kooperatif"]
browser = webdriver.Chrome()
notice_no = []
for district in tqdm(districts,unit="ditrict"):
    for typ in types:
        try:
            url = "https://www.sahibinden.com/satilik-"+str(typ)+"/istanbul-"+str(district)+"?pagingSize=50&sorting=date_desc&viewType=List"

            browser.get(url)
            time.sleep(4)

#check the total sales notice of page

            total_notice = browser.find_element_by_xpath("//*[@id='searchResultsSearchForm']/div/div[3]/div[1]/div[2]/div[1]/div[1]/span")

            print(district+" district total "+typ+" number of notice: "+total_notice.text)
            total = total_notice.text

            total_num = int(total.replace(".","").replace(" notice",""))
            if total_num <=50:
                if total_num>=2:
                    scrap_num=2
                else:
                    scrap_num=1
            else:
                scrap_num = round(total_num*0.05)
            print("Number of notice to scrape: "+str(scrap_num))
        except NoSuchElementException:
            print(str(district) + " district " + str(type) + " no notice")

#scraping every number of notice

        if scrap_num<=50:
            elements = browser.find_elements_by_css_selector("div.searchResultsClassifiedId")
            limit=0
            for i in elements:
                ilan_no.append(i.text)
                limit+=1
                if limit >= scrap_num:
                    break

        else:
            pages = [50, 100, 150, 200, 250]
            elements = browser.find_elements_by_css_selector("div.searchResultsClassifiedId")
            for i in elements:
                ilan_no.append(i.text)
            for i in pages:
                url_i = "https://www.sahibinden.com/satilik-"+str(typ)+"/istanbul-"+str(district)+"?pagingOffset="+str(i)+"&pagingSize=50&sorting=date_desc&viewType=List"
                browser.get(url_i)
                time.sleep(10)
                elements = browser.find_elements_by_css_selector("div.searchResultsClassifiedId")
                limit=0
                for i in elements:
                    ilan_no.append(i.text)
                    limit+=1
                    if limit >= scrap_num:
                        break
                break

browser.close()
print(notice_no)
print(len(notice_no))
array= np.array(notice_no)
a= pd.DataFrame(array,columns=["notice_no"])
a.to_csv("notice_no.csv",index=False)


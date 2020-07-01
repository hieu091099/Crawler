# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 06:02:05 2020

@author: vai22
"""
import urllib.request
import requests
import re
import newspaper
from newspaper import Article
from newspaper import Config
from urllib.parse import urlparse
from bs4 import BeautifulSoup 
import os
# 'https://www.express.co.uk'
# 'https://vnexpress.net'
# 'https://dantri.com.vn'
# 'https://edition.cnn.com'
# 'https://kenh14.vn'
# 'https://baomoi.com'
# 'https://thanhnien.vn'
# 'https://gamek.vn'
# 'https://tuoitre.vn'
urlgoc = 'https://vnexpress.net'


    

def getNameUrl(url):
    url2 = url.split('//')[-1]
    return url2
def createFolderSave(namefile):
	tf=True
	for root, dirs, files in os.walk("././", topdown=False):
	    for name in dirs:
	    	if name == namefile:
	    		tf=False
	if tf==True:
		os.mkdir(namefile)
        
def createFolderParent(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        return 

def writeFile(txtArrAfter, outputName, path):
    f = open(path + "/" + outputName + ".txt", "a", encoding="utf8")
    f.write(str(txtArrAfter))
    f.close()
    

def getData(url):
    data_url = []  
    try:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        config = Config()
        config.browser_user_agent = user_agent
        page = Article(url, config=config)
        page.download()
        page.parse()
        data_url.append(page.text)
    except:
        print('***FAILED TO DOWNLOAD***',page.url)   
    return data_url
#load từ topic -> html
def getHtmlFromTopic(url, urlgoc):
    links2 = []
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    for link in soup.findAll('a'):
        links = link.get('href')
        sub = str(links)
        if(len(sub)> 40):
            if(sub.startswith('https')):
                links2.append(sub)
            else:
                sub2 = urlgoc + sub
                links2.append(sub2)
    return links2
# get content from topics
def getText(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup.prettify()
# hàm xóa giá trị rỗng trong array list
def strip_list_noempty(mylist):
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
    return [item for item in newlist if item != '']
#hàm get topics from url
def getTopics(url):
    topics = urlparse(url).path.split('/')[-1]
    topics = topics.split('.')[0]
    return topics
def getHtml(link):
	try:
		response = requests.get(link)
		return response
	except NameError:
		print("Can't not read")
######################################################

topics = []
path = []
html = []
data = []
html_test = "https://"
input_paper = newspaper.build(urlgoc)
a = input_paper.category_urls()
for x in a: 
    topics.append(getTopics(x))
print("List topics")
i = 1
topics = strip_list_noempty(topics)
a = strip_list_noempty(a)

for x in topics:
    print(str(i) +":"+ x)
    i = i + 1
    
print('-1:Break!')
h = 1
for l in range(len(topics)):  
    # h= int(input('Choose topics:'))
    pattern = re.compile(topics[h-1])
    for i in a:
        if pattern.search(i):
            temp_html = getHtmlFromTopic(i,urlgoc)
    #Tạo thư mục lưu file       
    createFolderSave("Data")
    createFolderParent("Data"+"/"+getNameUrl(urlgoc)+"/"+topics[h-1])
    print("Data"+"/"+getNameUrl(urlgoc)+"/"+topics[h-1]+"/"+topics[h-1]+".txt")
    k = 1
    for i in temp_html:
        # print(getData(i))
        writeFile(getData(i),topics[h-1],"Data/"+getNameUrl(urlgoc)+"/"+topics[h-1])
        if k==30:
            break
        k = k + 1
    print("Save file sucessfully")
    h = h + 1
    if h==-1:
        break
    



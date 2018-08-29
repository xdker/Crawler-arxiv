# coding=utf-8
import requests
import codecs
import os.path
import os
from bs4 import BeautifulSoup
import sys, re
import time

baseUrl = "https://arxiv.org"

def myGet(url):
    for i in range(1, 10):
        try:
            response = requests.get(url, timeout=50)
        except requests.exceptions.Timeout:
            time.sleep(5)
            print ("请求超时，第 {} 次重复请求".format(i))
            continue
        else:
            if response.status_code == 200:
                print("scrawling "+url+" done")
                return response
    return -1


#通过翻页来获得所有标题
def getAllTitlesByFanYe(res):
    soup = BeautifulSoup(res.text,'html.parser')

    otherLinks=[]
    try:
        nums = soup.find("small").text
        if(nums.find("|")==-1):
            raise Exception("该项目没有内容")
    except:
        otherLinks = []
    else:
        if(nums.find("...")==-1):
            nums = soup.find("small").find_all("a")
            otherLinks = [link+num["href"] for num in nums]
        else:
            nums = nums.split("|")[-1].split("-")[-1]
            nums = int(re.sub('\D','',nums))
            temp_url = link+"?skip={}&show=200"
            for i in range(25,nums,200):
                otherLinks.append(temp_url.format(i))


    allPapers = []
    # 获得本页的title
    titles = soup.find_all("div",{"class":"list-title mathjax"})
    for title in titles:
        allPapers.append(title.text.replace("Title:","").strip()+"\r\n")

    # 获得其他页的title
    for otherLink in otherLinks:
        res = myGet(otherLink)
        soup = BeautifulSoup(res.text,'html.parser')

        titles = []
        titles = soup.find_all("div",{"class":"list-title mathjax"})

        for title in titles:
            allPapers.append(title.text.replace("Title:","").strip()+"\r\n")

    return allPapers


# 通过all按钮获得所有标题
def getAllTitlesByAllButton(res):
    allPapers = []

    soup = BeautifulSoup(res.text,'html.parser')

    allLink = baseUrl + soup.find("a",text="all")["href"]
    res = myGet(allLink)
    soup = BeautifulSoup(res.text,'html.parser')

    titles = soup.find_all("div",{"class":"list-title mathjax"})
    for title in titles:
        allPapers.append(title.text.replace("Title:","").strip()+"\r\n")
    return allPapers

if __name__ == "__main__":
    f = codecs.open('./data/1.CS下面的所有类别.txt','r','utf-8')
    lines = f.readlines()
    f.close()

    for line in lines:

        link = line.strip().split("|")[0]
        name = line.strip().split("|")[1]
        year = link.split("/")[-1]

        print("====================================================================")
        print("begin crawl {}_{}".format(name,year))

        res = myGet(link)
        if(res==-1):
            print("crawl {} failure...".format(link))
            continue

        try:
            allPapers = getAllTitlesByAllButton(res)
        except:
            allPapers = getAllTitlesByFanYe(res)

        f = codecs.open('./data/2.{}_{}.txt'.format(name,year),'w','utf-8')
        f.writelines(allPapers)
        f.close()

        print("crawl end {}_{} we got {} titles".format(name,year,len(allPapers)))
        print()
        print("sleeping 2 s...")
        time.sleep(2)
        print("====================================================================")
        print()

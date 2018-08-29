# coding=utf-8
import requests
import codecs
import os.path
import os
from bs4 import BeautifulSoup
import sys, re, urllib
import traceback

if __name__ == "__main__":
    f = codecs.open('./data/1.CS下面的所有类别.txt','r','utf-8')
    lines = f.readlines()
    f.close()

    for line in lines:

        link = line.strip().split("|")[0]
        name = line.strip().split("|")[1]
        year = link.split("/")[-1]

        print("begin crawl {}_{}".format(name,year))

        res = requests.get(link,timeout=10)
        soup = BeautifulSoup(res.text,'html.parser')

        otherLinks=[]
        nums = soup.find("small").text
        if(nums.find("...")==-1):
            nums = soup.find("small").find_all("a")
            otherLinks = [link+num["href"] for num in nums]
            print(otherLinks)
        else:
            nums = nums.split("-")[-1]
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
            try:
                res = requests.get(otherLink,timeout=50)
            except:
                time.sleep(5)
                res = requests.get(otherLink,timeout=500)
            soup = BeautifulSoup(res.text,'html.parser')

            titles = []
            titles = soup.find_all("div",{"class":"list-title mathjax"})
            for title in titles:
                allPapers.append(title.text.replace("Title:","").strip()+"\r\n")
            print("scrawling "+otherLink+" done")

        f = codecs.open('./data/2.{}_{}.txt'.format(name,year),'w','utf-8')
        f.writelines(allPapers)
        f.close()

        print("crawl end {}_{} we got {} titles".format(name,year,len(allPapers)))
        print()

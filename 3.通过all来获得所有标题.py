# coding=utf-8
import requests
import codecs
import os.path
import os
from bs4 import BeautifulSoup
import sys, re, urllib
import traceback

baseUrl = "https://arxiv.org"

if __name__ == "__main__":
    f = codecs.open('./data/1.CS下面的所有类别.txt','r','utf-8')
    lines = f.readlines()
    f.close()

    for line in lines:
        allPapers = []

        link = line.strip().split("|")[0]
        name = line.strip().split("|")[1]

        print("begin crawl "+name)

        res = requests.get(link,timeout=10)
        soup = BeautifulSoup(res.text,'html.parser')

        allLink = baseUrl + soup.find("a",text="all")["href"]
        res = requests.get(allLink,timeout=50)
        soup = BeautifulSoup(res.text,'html.parser')

        titles = soup.find_all("div",{"class":"list-title mathjax"})

        for title in titles:
            allPapers.append(title.text.replace("Title:","").strip()+"\r\n")

        f = codecs.open('./data/2.'+name+'.txt','w','utf-8')
        lines = f.writelines(allPapers)
        f.close()

        print("crawl end "+name)
        print()

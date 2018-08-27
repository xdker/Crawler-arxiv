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
        allPapers = []

        link = line.strip().split("|")[0]
        name = line.strip().split("|")[1]

        print("begin crawl "+name)

        res = requests.get(link,timeout=10)
        soup = BeautifulSoup(res.text,'html.parser')


        nums = soup.find("small").find_all("a")
        otherLinks = [link+num["href"] for num in nums]
        print(otherLinks)

        titles = soup.find_all("div",{"class":"list-title mathjax"})

        for title in titles:
            allPapers.append(title.text.replace("Title:","").strip()+"\r\n")


        for otherLink in otherLinks:
            res = requests.get(otherLink,timeout=10)
            soup = BeautifulSoup(res.text,'html.parser')

            titles = []
            titles = soup.find_all("div",{"class":"list-title mathjax"})
            for title in titles:
                allPapers.append(title.text.replace("Title:","").strip()+"\r\n")

        f = codecs.open('./2.'+name+'.txt','w','utf-8')
        lines = f.writelines(allPapers)
        f.close()

        print("crawl end "+name)
        print()

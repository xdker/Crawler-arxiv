# coding=utf-8
import requests
import codecs
import os.path
import os
from bs4 import BeautifulSoup
import sys, re, urllib
import traceback


url = 'https://arxiv.org/'
baseUrl = 'https://arxiv.org'

if __name__=='__main__':

    res = requests.get(url,timeout=10)
    soup = BeautifulSoup(res.text,'html.parser')
    h2 = soup.find('h2',string=re.compile("Computer Science"))
    links = h2.find_next_sibling("ul").find('li').find_all('a')

    hrefs = [baseUrl+link['href'] + "|" + link.text+"\r\n" for link in links if(link['href'].endswith("recent") and link['href'].find(".") != -1) ]


    f = codecs.open('./data/1.CS下面的所有类别.txt','w','utf-8')
    f.writelines(hrefs)
    f.close()

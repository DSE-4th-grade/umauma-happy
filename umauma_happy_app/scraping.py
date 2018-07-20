# -*- coding:utf-8 -*-
import urllib.request
import bs4
import logging

url = 'http://race.netkeiba.com/?pid=race_list'
soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read())



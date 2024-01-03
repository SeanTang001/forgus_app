import requests
from requests_html import HTMLSession
import bs4
import pprint
import time
import json
import re
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

t = time.time()
browser = webdriver.Firefox(executable_path='path/geckodriver')
maindict = {}
def search(zip):
    browser.get("https://www.target.com/store-locator/find-stores/"+zip+"")
    x = browser.find_element_by_class_name("react-rendered")
    maindict[zip] = parse(x.get_attribute('innerHTML'))

def parse(x):
    #i used regex cuz i wanted to practice my regex skills
    h = {}
    a = re.findall(r"\"\/sl\/(.*?)\"", x)
    f = re.findall(r"rel=\"noopener\"\>(.*?)\<\/a\>", x)
    for i in range(len(f)):
        x = i*2
        b, a[x] = re.split("/", a[x])
        h[a[x]] = re.split(",", f[i])
        h[a[x]].pop(2)
    return h


x = open("../jsons/target_page.html", "r+")
b = x.read()
x.close()
g = json.loads(b)
print(g)
maindict = {}

k = list(g.keys())
for i in range(len(k)):
    a = list(g[k[i]].keys())
    for u in range(len(a)):
        maindict[a[u]] = g[k[i]][a[u]]

print(maindict)
# for i in range(len(b)):
#     search(b[i])
#     print maindict
x = open("../jsons/target_page.html", "w")
x.write(json.dumps(maindict, indent=2))
x.close()
print(time.time() - t)
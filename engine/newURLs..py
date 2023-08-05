from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse
import os

def custom_selector(tag):
  return tag.name == "title" or tag.name == "h1" or tag.name == "p"


with open('logs/URLID2.json','w') as w:
  new_data = dict()
  for subdir, _, files in os.walk("C:/Users/Ben/Downloads/DEV"):
    for file in files:
      with open(os.path.join(subdir, file),'r') as f:
        data = json.load(f)

      #adds url to list of URL IDs 
      url = urlparse(data['url'])._replace(fragment="").geturl()

      #tokenizes text, lxml works well with broken html so it is used to parse
      raw_html = BeautifulSoup(data['content'], 'html.parser' )

      try:
        new_data[url] = raw_html.find(custom_selector).get_text()
      except:
        new_data[url] = urlparse(url).hostname
      
      print(new_data[url])
    
  
  w.write(json.dumps(new_data))



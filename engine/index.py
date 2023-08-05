import json
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from urllib.parse import urlparse
import glob
from collections import defaultdict


CHARLIE_PATH = 'C:/School/CS121/SearchEngine/developer/DEV'
BEN_PATH = '/DEV'
ALPHANUMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

rootdir = BEN_PATH
ps = PorterStemmer()


def tokenize(text: str) -> list:
  '''splits text into a list of tokens'''
  text = text.lower()
  # separator_pattern = "[^a-zA-Z\d]+"
  # tokens = re.split(separator_pattern,text)
  tokenizer = RegexpTokenizer(r'\w+')
  tokens = tokenizer.tokenize(text)
  for i,token in enumerate(tokens):
    tokens[i] = ps.stem(token)
  return tokens


def index(b = False):
  '''initial read of files to create inverse index and other files for later use'''

  if b: print('Reindexing webpages...')

  idx = 0
  data = ''
  url_ID = []
  tokenDict = {char:dict() for char in ALPHANUMS}

  #pagerank
  outgoing_dict = defaultdict(set)

  #for duplicate detection
  bit_lengths = set()

  for subdir, _, files in os.walk(rootdir):
    for file in files:
      if(b and idx%1000 == 0): print(idx)

      with open(os.path.join(subdir, file),'r') as f:
        data = json.load(f)

      #removes exact duplicates
      if len(data['content']) in bit_lengths:
        continue
      else:
        bit_lengths.add(len(data['content']))

      #adds url to list of URL IDs 
      defrag = urlparse(data['url'])._replace(fragment="").geturl()
      url_ID.append(defrag)

      #tokenizes text, lxml works well with broken html so it is used to parse
      raw_html = BeautifulSoup(data['content'], 'lxml')

      #adding outgoing links for pagerank
      for link in raw_html.findAll('a'):
        new_url = link.get('href')
        new_url = urlparse(new_url)._replace(fragment="").geturl()
        outgoing_dict[defrag].add(new_url)
  
      #tokenizes visible text
      #removes non visible text
      for script in raw_html(["script","style"]):
        script.extract()
      tokens = tokenize(raw_html.get_text())

      #tokenizes important string, bs4 works with broken html
      importantString = ""
      for tag in ['title','h1','h2','h3','h4','h5','h6']:
        importantString += ' '.join([t.text.strip() for t in raw_html.find_all(tag)])
      
      imp_tokens = tokenize(importantString)

      boldstring = ""
      for tag in ['b','strong']:
        ' '.join([t.text.strip() for t in raw_html.find_all(tag)])
      bold_tokens = tokenize(boldstring)

      #inserting tokens into indexDict
      for word in tokens:
        if len(word) == 0:
          continue
        if word[0].upper() not in ALPHANUMS:
          continue
        letterDict = tokenDict[word[0].upper()]
        if word in letterDict:
          #check if any of this token have been found in the current document
          if letterDict[word][-1][0] == idx:
            #if so, increase count by 1
            letterDict[word][-1][1] += 1
          else:
            #if not, initialize count to 1
            letterDict[word].append([idx,1])

        else:
          #if token not in dictionary, initialize nested list with count of 1 at the current document
          letterDict[word] = [[idx,1]]
      
      #parsing through important tokens
      for word in imp_tokens:
        if len(word) == 0:
          continue
        if word[0].upper() not in ALPHANUMS:
          continue
        letterDict = tokenDict[word[0].upper()]
        if word in letterDict:
          #check if any of this token have been found in the current document
          if letterDict[word][-1][0] == idx:
            #if so, increase count by 100, as it is weighted more than normal text
            letterDict[word][-1][1] += 500
          else:
            #if not, initialize count to 100
            letterDict[word].append([idx,500])

        else:
          #if token not in dictionary, initialize nested list with count of 1 at the current document
          letterDict[word] = [[idx,500]]
      
      #parsing through bold tokens
      for word in bold_tokens:
        if len(word) == 0:
          continue
        if word[0].upper() not in ALPHANUMS:
          continue
        letterDict = tokenDict[word[0].upper()]
        if word in letterDict:
          #check if any of this token have been found in the current document
          if letterDict[word][-1][0] == idx:
            #if so, increase count by 1, as it is weighted more than normal text
            letterDict[word][-1][1] += 2
          else:
            #if not, initialize count to 3
            letterDict[word].append([idx,2])

        else:
          #if token not in dictionary, initialize nested list with count of 1 at the current document
          letterDict[word] = [[idx,2]]
      
      if(idx%1000 == 0):
        with open(f'logs/index_part{idx//1000}.json', 'w') as f:
          json.dump(tokenDict,f)
        tokenDict = {char:dict() for char in ALPHANUMS}

      #loop finished, next file
      idx += 1
      
  #dump remaining after done
  with open(f'logs/index_part{idx//1000+1}.json', 'w') as f:
    json.dump(tokenDict,f)
  
  #dump urls
  with open('logs/URLID.json', 'w') as f:
    json.dump(url_ID, f)



  #calculate and dump pagerank information
  print("calculating pagerank...")
  #calculate incoming links by iterating through all the links in incoming
  incoming_dict = defaultdict(set)
  for i,page in enumerate(outgoing_dict):
    print(i, "out of", len(outgoing_dict))
    for out_link in outgoing_dict[page]:
      #if the outgoing link is in the pages, we will add it to a dict that tracks the links incoming
      if out_link in url_ID:
        incoming_dict[out_link].add(page)

  #pagerank default value
  sumurl = len(url_ID)
  pagerank = dict()
  for url in url_ID:
    pagerank[url] = 1/sumurl
  
  #5 iterations of updating page rank for stability
  for n in range(5):
    print("iteration",n)
    #algorithm for pagerank
    for url in pagerank:
      pagerank[url] = (1-0.85) + 0.85*(sum([pagerank[i]/len(outgoing_dict[i]) for i in incoming_dict[url]]))
  
  with open(f'logs/PAGERANK.json', 'w') as f:
    json.dump(pagerank,f)
  

  #merge after finish indexing
  merge(idx//1000+1)


  if b: print('Reindexing complete.\n', "Total pages indexed: ",idx, sep = '')


def merge(maxidx):
  '''merges the partial indices and separates it by character start'''
  filelist = list()

  #open all partial files that are going to be read from
  for partNum in range(1,maxidx+1):
    filelist.append(open(f'logs/index_part{partNum}.json','r'))
  
  #for each character, scan every file and combine lists 
  for startChar in ALPHANUMS:
    print("Merging for letter",startChar)

    dict_per_letter = dict()
    with open(f'logs/index_{startChar}.json','w') as charFile:
      for partFile in filelist:
        #pointer back to start of file
        partFile.seek(0)
        data = json.loads(partFile.read())

        #add contents to character dict
        for word,occurences in data[startChar].items():
          if word in dict_per_letter:
            dict_per_letter[word].extend(occurences)
          else:
            dict_per_letter[word] = occurences
      
      json.dump(dict_per_letter,charFile)
  
  for f in filelist:
    f.close()
  
  splitLetterIndices()


def splitLetterIndices():
  '''for each letter, split it further into files for each 2 character start'''
  for firstChar in ALPHANUMS:
    print("splitting dict for", firstChar)
    #dict for single letter words
    singleLetterWords = dict()

    twoLetterSplitDict = {firstChar+char:dict() for char in ALPHANUMS}

    with open(f'logs/index_{firstChar}.json','r') as charFile:
      entireLetterDict = json.load(charFile)

      for term,postings in entireLetterDict.items():
        if len(term) == 1:
          singleLetterWords[term] = postings
        
        else:
          if term[:2].upper() in twoLetterSplitDict:
            twoLetterSplitDict[term[:2].upper()][term] = postings
    
    for startLetters,words in twoLetterSplitDict.items():
      with open(f'logs/index_{startLetters}.json','w') as f:
        json.dump(words,f)
    
    with open(f'logs/index_{firstChar}_.json','w') as f:
      json.dump(singleLetterWords,f)


if __name__ == "__main__":
  index(True)
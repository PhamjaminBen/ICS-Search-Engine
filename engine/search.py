# Read stored json file here
import json
from nltk.stem import PorterStemmer
import math
from queue import PriorityQueue
from index import tokenize
from collections import defaultdict

ALPHANUMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
ps = PorterStemmer()

file_dict = dict()

cached_terms = dict()

#prepare files for reading
for char in ALPHANUMS:
  for char2 in '_' + ALPHANUMS:
    f = open(f'logs/index_{char+char2}.json','r')
    file_dict[char+char2] = f


def accumulateScores(list1: list, list2: list) -> list:
  '''accumulates the scores for 2 respective inverted lists and combines them'''
  ret = []
  l1 = 0
  l2 = 0
  while l1 < len(list1) and l2<len(list2):
    #if theres a common docID, add that to the common list
    if list1[l1][0] == list2[l2][0]:
      combined_occurences = list1[l1][1] + list2[l2][1]
      ret.append([list1[l1][0],combined_occurences])
      l1 += 1
      l2 += 1
    else:
      #if theres no common element, increment lower docID
      if list1[l1][0] < list2[l2][0]:
        ret.append(list1[l1])
        l1 += 1
      else:
        ret.append(list2[l2])
        l2 += 1
      
  return ret


def Search(query) -> list:
  '''search function employing tf-idf scoring'''
  wordLists = list()

  queryWordCounts = defaultdict(int)

  tokenized_q = tokenize(query)

  #occurences of word in search, will be used to modify tf idf
  for word in tokenized_q:
    queryWordCounts[word] += 1

  #does aset because we already have the num occurences for each unique term in query
  for word in set(tokenized_q):

    inverted_list = []
    
    #if already cached no need to open again
    if word in cached_terms:
      inverted_list = cached_terms[word]

    else:
      if len(word) == 1:
        letterDict = json.load(file_dict[f'{word.upper()}_'])
        #resetting read pointer back to 0
        file_dict[f'{word.upper()}_'].seek(0)
      else:
        #accesses respective dictionary
        letterDict = json.load(file_dict[word[:2].upper()])
        #resetting read pointer back to 0
        file_dict[word[:2].upper()].seek(0)

      #if word doesn't exist ignore it in query
      if word not in letterDict:
        continue
      
      inverted_list = letterDict[word]

      #if inverted list is long store it in memory
      if len(inverted_list) >= 10_000:
        cached_terms[word] = inverted_list
    
    #computing tf_idf score for every document for specific word
    tf_idf_list = list()

    #21688 is the number of indexed document after duplicate detection
    idf_score = math.log10(21688/ len(inverted_list) )
    for doc,frequency in inverted_list:
      tf_score = 1+math.log10(frequency)
      #modifies the score by how many times the term occurs in the query
      tf_idf_list.append([doc,queryWordCounts[word]*tf_score*idf_score])
    
    wordLists.append(tf_idf_list)
  
  #does this so we start with word with least docs to save trime
  wordLists.sort(key = lambda x: len(x))

  #keep reducing until finding documents with all words
  while len(wordLists) > 1:
    new = accumulateScores(wordLists[0],wordLists[1])
    wordLists[0] = new
    wordLists.pop(1)

  if not wordLists: return []
  return wordLists[0]


def matchID(intersect) -> list:
  '''matches the ID to the respective url and pagerank, and returns a list of tuples of the information'''
  ret = []
  with open('logs/URLID.json','r') as f:
    url_ID = json.load(f)
  with open('logs/PAGERANK.json', 'r') as f:
    pagerank = json.load(f)

  #only print top 5 elements
  for idx in intersect:
    url = url_ID[idx[0]]
    if url in pagerank:
      ret.append( (url, round(idx[1],3), round(pagerank[url],3) ))
    else:
      ret.append( (url, round(idx[1],3), 0) )
      
  return ret

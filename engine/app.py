from flask import Flask, request, jsonify
from search import Search, matchID
import time
import json
from flask_cors import CORS
import re


app = Flask(__name__)
CORS(app)

id_file = open('logs/URLID2.json','r')
id_dict = json.load(id_file)

@app.route("/search/<term>")
def get_user(term: str):
  term = term.replace("-"," ")
  result = []
  #begin timer
  t1 = time.perf_counter()

  #get all the tf-idf scores of the documents
  intersect = Search(term)

  #end timer and calculate search time elapsed
  t2 = time.perf_counter()
  elapsed = t2-t1

  #sort docs by tf-idf score after timing the search

  #sorting by total score
  intersect = matchID(intersect)
  intersect.sort(key = lambda x: -x[1]-0.5*x[2])

  for (url, score, pagerank) in intersect[:50]:
    title = id_dict[url].strip()
    # title = re.sub(r'\/.',"",title)
    # print(title)

    if len(title) > 200:
      title = title[:200] + '...'
    result.append({"url": url, "title": title })
    pass
  
  response = jsonify(result)
  return response, 200


if __name__ == "__main__":
    app.run(debug=True)
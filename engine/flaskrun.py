from flask import Flask, request, jsonify
from search import Search, matchID
import time
import json

app = Flask(__name__)

id_file = open('logs/URLID2.json','r')
id_dict = json.load(id_file)

@app.route("/search/<term>")
def get_user(term):

  #begin timer
  t1 = time.perf_counter()

  #get all the tf-idf scores of the documents
  intersect = Search("article")

  #end timer and calculate search time elapsed
  t2 = time.perf_counter()
  elapsed = t2-t1

  #sort docs by tf-idf score after timing the search

  #sorting by total score
  intersect = matchID(intersect)
  intersect.sort(key = lambda x: -x[1]-0.5*x[2])

  for (url, score, pagerank) in intersect:
    print(url,score,pagerank)

  data = {"test": "hello world"}
  return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)
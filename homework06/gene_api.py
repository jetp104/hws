from flask import Flask, request
import requests
import redis
import json 

app = Flask(__name__)



def get_redis_client():
    return redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
rd = get_redis_client()


@app.route('/data', methods=['POST','GET','DELETE'])
def handle_data():
    if request.method == 'GET':
        try:
            data = rd.hgetall('hgnc') 
            the_data = json.loads(data['the_data']) 
            return the_data
        except KeyError: 
            return "There is no data\n" 
    
    elif request.method == 'POST': 
        response = requests.get("https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json")
        the_data = response.json() 
        json_string = json.dumps(the_data) 
        rd.hset('hgnc', 'the_data', json_string) 
        return "data has been loaded\n "  

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted, there are {rd.keys()} keys in the db\n'

    else:
        return "The method you want isn't working\n"

@app.route('/genes', methods=['GET'])
def get_genes():
    data = rd.hget('hgnc', 'the_data') 
    json_data = json.loads(data) 

    hgnc_ids = [doc['hgnc_id'] for doc in json_data['response']['docs']] 
    return hgnc_ids 

@app.route('/genes/<hgnc_id>', methods=['GET'])
def get_gene(hgnc_id):
    data = rd.hget('hgnc','the_data') 
    json_data = json.loads(data) 
    docs = json_data['response']['docs']
    matching_docs = [doc for doc in docs if doc['hgnc_id'] == hgnc_id] 
    matching_doc = matching_docs[0]
    return matching_doc
     

if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0') 

from flask import Flask, request
import requests
import redis
import json 
import os 

app = Flask(__name__)



def get_redis_client():
    """
    Connects to a redis database

    Args: 
        None

    Return:
        returns a redis alias for use for docker files 

    """
    redis_host = os.environ.get('REDIS_HOST')
    return redis.Redis(host= redis_host, port=6379, db=0, decode_responses=True)
rd = get_redis_client()


@app.route('/data', methods=['POST','GET','DELETE'])
def handle_data():
    """
    This function posts the data to a redis database, gets all the data from that database and also deletes all
    the data from the database

    Args: 
        None

    Return: 
        the_data (dict): returns a dicitoanry for all the data in the data set
        (string): A string that shows the data has been posted 
        (string): to show that the data has been deleted 
        (string): to show one of the methods is broken 

    """
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
def get_genes() -> list:
    """
    Gives a list of all the gene id's to the user

    Args: 
        None

    Return:
        hgnc_ids(list): Returns a list of all hgnc ids from the data set

    """
    try:
        data = rd.hget('hgnc', 'the_data') 
        json_data = json.loads(data) 

        hgnc_ids = [doc['hgnc_id'] for doc in json_data['response']['docs']] 
        return hgnc_ids 
    except TypeError:
        return "The data may be empty try posting it\n" 


@app.route('/genes/<string:hgnc_id>', methods=['GET'])
def get_gene(hgnc_id: str) -> dict:
    """
    Gives all the values associated with a single hgnc id 

    Args: 
        hgnc_id(string): The specific hgnc_id that a user wants

    Return: 
        matching_doc (list): This returns all the values associated with a single hgnc id as a list of values

    """
    try:
        data = rd.hget('hgnc','the_data') 
        json_data = json.loads(data) 
        docs = json_data['response']['docs']
        matching_docs = [doc for doc in docs if doc['hgnc_id'] == hgnc_id] 
        matching_doc = matching_docs[0]
        return matching_doc
    except TypeError: 
        return "Invalid input or data has not been loaded or deleted\n" 
     

if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0') 

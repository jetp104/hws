from flask import Flask, request 
import xmltodict
import requests
import math  


app = Flask(__name__)

def get_data() -> list:
    """
    Gets the data from the NASA website for the ISS trejectories 

    Args: 
        No args for this function 
    
    Returns: 
        data (list): The data from the ISS trajectory xml 

    """
    r = requests.get("https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    if r.status_code == 200:
        data = xmltodict.parse(r.text)
        return data
 

@app.route('/', methods=['GET']) 
def data() -> list:  
    """
    Gets the ISS Trajectory data from the NASA website. 

    Args: 
        No args for this function.

    Returns: 
        iss_data (dict): The dictionary of the data that was imported using the requests library, the imported data was an 
        xml file. 
    """
    if iss_data == {}: 
        return "Data has been deleted\n"
    else:
        return iss_data 

@app.route('/keys', methods=['GET'])
def keys() -> list:   
    """
    Goes thrrough all the keys in the data set to find which one epochs is under. 

    Args:
        No args for this function.

    Returns: 
        list1 (list): returns a list of keys associated with the xml data
        list2 (list): returns a list of keys associated with the "ndm" key
        list3 (list): returns a list of keys associated with the "oem" key
        list4 (list): returns a list of keys associated with the "body" key
        list5 (list): returns a list of keys associated with the "segment" key
        list6 (list): returns a list of keys associated with the "data" key
        list7 (list): returns the epochs and the values associated with it using the stateVector key. 
    """

    key_data = data() 
    
    try:
        list1 = list(key_data.keys())
        # return list1
        list2 = list(key_data['ndm'].keys()) 
        #return list2 
        list3 = list(key_data['ndm']['oem'].keys())
        #return list3
        list4 = list(key_data['ndm']['oem']['body'].keys())
        #return list4
        list5 = list(key_data['ndm']['oem']['body']['segment'].keys())
        #return list5
        list6 = list(key_data['ndm']['oem']['body']['segment']['data'].keys())
        #return list6
        list7 = list(key_data['ndm']['oem']['body']['segment']['data']['stateVector'])
        return list7
    except AttributeError: 
        return "Data has been deleted\n" 

@app.route('/epochs', methods=['GET']) 
def epochs()->  list:  
    """
    Returns the epochs in the dictionary and every value assoicated with the epochs.

    Args: 
        No args for this function. 

    Returns: 
        epochs_data (list): returns the epoch data from the dictionary as a list along with all values
        associated with it.
    """    
    epochs_data = keys()  
   
    offset = request.args.get('offset',0)
    if offset: 
        try: 
            offset = int(offset)
        except ValueError: 
            return "Invalid start parameter; start must be an integer. \n"
    limit = request.args.get('limit', len(epochs_data)) 
    if limit: 
        try: 
            limit = int(limit)
        except ValueError: 
            return "Invalid start parameter; start must be an integer. \n" 
    if limit > len(epochs_data) or offset > len(epochs_data) or offset < 0 or limit < 0:
        return "Change query paramater \n"

    counter = 0 
    result = [] 
    for d in range(len(epochs_data)): 
        if counter == limit: 
            break 
        if d >= offset:
            try: 
                result.append(epochs_data[d]['EPOCH'])
                counter = counter + 1
            except TypeError: 
                return "Data has been deleted\n" 
    return result   


@app.route('/epochs/<string:epoch>', methods=['GET'])
def an_epoch(epoch: str) -> list:
    """
    This function returns a single epoch from the list of epochs

    Args: 
        epoch (string): The epoch value this function takes in is a string of the specific 'EPOCH' value 
        associated with this certain epoch 

    Returns: 
        single_epoch (list): The single_epoch is the list that stores the values associated with the certain
        epoch chosen by the user 
        

    """  
    try:     
        epochs_data = keys()
        single_epoch = [] 
        for i in range(len(epochs_data)): 
            if epoch == str(epochs_data[i]['EPOCH']):
                single_epoch = epochs_data[i] 
                return  single_epoch  
        if single_epoch == []: 
            return "Please enter a valid epoch ID\n" 
    except TypeError: 
        return "Data has been deleted\n" 
    
     

@app.route('/epochs/<string:epoch>/speed', methods=['GET'])
def speed(epoch: list) -> str:
    """
    This function calculates the instantaneous speed of the epoch by squaring each x_dot,y_dot,z_dot 
    respectively adding them toghether and then taking the square root of the total.

    Args: 
        epoch (string): The epoch value this function takes in is a string of the specific 'EPOCH' value
        associated with this certain epoch

    Returns: 
        awnser (f string): Returns the insatntaneous speed in an F string with the message "The speed of 
        the epoch is:"  
    """
    try: 
        single_epoch = an_epoch(epoch) 

        x_dot = float(single_epoch['X_DOT']['#text'])
        y_dot = float(single_epoch['Y_DOT']['#text'])
        z_dot = float(single_epoch['Z_DOT']['#text']) 

        speed = math.sqrt(x_dot**2+y_dot**2+z_dot**2) 
        awnser = f'The speed for this epoch is: {speed} \n'
        return awnser
    except TypeError: 
        return "Data has been deleted\n" 


@app.route('/help', methods=['GET'])
def help() -> str:
    """
    Pulls up a help menu for the user to know the commands for the program

    Args:
        None

    Returns: 
        paths (str): A string with all the commands for this function 

    """

    paths = """These are the paths and methods used for this application

Paths:
    t(/)                           This path uses the GET method and returns the entire data set
    (/epochs)                      This path uses the GET method and returns the list of all Epochs in the data set
    (/epochs?limit=int&offset=int) This path uses the GET method and returns a modified list of Epochs given query parameters
    (/epochs/<epoch>)              This path uses the GET method and returns the state vectors for a sepecifc Epoch from the data set
    (/keys)                        This path uses the GET method to find all the keys within the data set
    (/epochs/<epoch>/speed)        This path uses the GET method to return instantaneous speed for a specific Epoch in the data set 
    (/help)                        This path uses the GET method to return help text that briefly describes each route
    (/delete-data)                 This path uses the DELETE method to delete all data from the dictioanry object
    (/post-data)                   This path uses the POST method to reload the dictionary object with data from the web""" 
    return paths

@app.route('/delete-data', methods=['DELETE'])
def delete() -> str:
    """
    Deletes all the data from the iss_data set

    Args: 
        No args 

    Returns: 
        (str): A string that says deleted to show the data has been deleted

    """
    global iss_data
    iss_data.clear()

    return "Deleted \n"

@app.route('/post-data', methods=['POST'])
def post() -> str:
    """
    Deletes all the data from the iss_data set

    Args:
        No args

    Returns:
        (str): A string that says "data posted" to show the data has been deleted

    """
    global iss_data
    iss_data = get_data()    
    return "data posted\n"   

#Global variable called iss_data 
iss_data = get_data()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

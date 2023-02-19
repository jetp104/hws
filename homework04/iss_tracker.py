from flask import Flask 
import xmltodict
import requests
import math 

app = Flask(__name__)


@app.route('/', methods=['GET']) 
def data() -> dict:  
    """
    Gets the ISS Trajectory data from the NASA website. 

    Args: 
        No args for this function.

    Returns: 
        data (dict): The dictionary of the data that was imported using the requests library, the imported data was an 
        xml file. 
        Error (string): A string that tells the user the data has not been found.

    """
    r = requests.get("https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    if r.status_code == 200: 
        data = xmltodict.parse(r.text)
        return data
    else:
        Error = "Data not found"
        return Error

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

@app.route('/epochs', methods=['GET']) 
def epochs() -> dict:  
    """
    Returns the epochs in the dictionary and every value assoicated with the epochs.

    Args: 
        No args for this function. 

    Returns: 
        epochs_data (list): returns the epoch data from the dictionary as a list along with all values
        associated with it.
    """   
    epochs_data = keys()  
    return epochs_data

@app.route('/epochs/<string:epoch>', methods=['GET'])
def an_epoch(epoch: list) -> list:
    """
    This function returns a single epoch from the list of epochs

    Args: 
        epoch (string): The epoch value this function takes in is a string of the specific 'EPOCH' value 
        associated with this certain epoch 

    Returns: 
        single_epoch (list): The single_epoch is the list that stores the values associated with the certain
        epoch chosen by the user 
        error (string): A simple error message if the epoch that was searched for isn't in the data set

    """
    epochs_data = epochs()
    single_epoch = [] 
    for i in range(len(epochs_data)): 
        if epoch == str(epochs_data[i]['EPOCH']): 
            single_epoch = epochs_data[i] 
            return  single_epoch  
    if single_epoch == []:  
        error = "Data Not Found \n" 
        return error 

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
    single_epoch = an_epoch(epoch) 

    x_dot = float(single_epoch['X_DOT']['#text'])
    y_dot = float(single_epoch['Y_DOT']['#text'])
    z_dot = float(single_epoch['Z_DOT']['#text']) 

    speed = math.sqrt(x_dot**2+y_dot**2+z_dot**2) 
    awnser = f'The speed for this epoch is: {speed} \n'
    return awnser  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

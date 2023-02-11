import json 
import requests 
import math 

def turbidity(calibration_constant: float, detector_current: float) -> float:
    """
    Calculates the turbidity by multiplying two floats it's given togehter 

    Args: 
        calibration_constant (flaot): The calibration constant
        detector_current (float): The ninety degree detector current 

    Returns: 
        turb (float): The turbidity of that those specific values 
    """
    turb = calibration_constant * detector_current
    return round(turb,4) 

def decay(current_turb: float, threshold: float, decay_factor: float) -> float: 
    """
    Calcualtes the amount of time it takes for the water to reach a safe point by taking in three floats and then putting them into a modified version of the 
    exponential decay function 

    Args: 
        current_turb (float): The average turbidity of the most recent 5 data points
        threshold (float): The turbitity threshold for safe water
        decay_factor (float): The decay factor per hour 

    Returns: 
        time (float): The amount of time the water takes to get to a safer turbidity 
    """
    time = (math.log(threshold/current_turb))/(math.log(1-decay_factor)) 
    return round(time,2) 
    
def main(): 
    turb_data = requests.get('https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    data = turb_data.json() 

    i = 0  
    total = 0 
    NTU = 1.0 
    total_time = 0 
    decay_factor = 0.2
    for row in list(reversed(data['turbidity_data'])):  
        total += turbidity(row['calibration_constant'],row['detector_current'])
        i = i + 1 
        if i == 5: 
            break

    average = total/i

    print(f"Average turbidity based on most recent five measurements = {average:.4} NTU")  
    if average < NTU: 
        print("Info: Turbidity is below threshold for safe us")
        print("Minimum time required to return below a safe threshold = 0 hours") 
    else:  
        print("Warning: Turbidity is above threshold for safe us")
        total_time = decay(average,NTU,decay_factor) 
        print(f"Minimum time required to return below a safe threshold = {total_time:.2} hours") 

if __name__ == "__main__": 
    main() 

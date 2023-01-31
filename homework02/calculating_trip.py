import math
import json 
mars_radius = 3389.5    # km

def calc_gcd(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:

        lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
        d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
        return ( mars_radius * d_sigma )

 
#opens the json file 
with open('sites.json') as f: 
    data = json.load(f) 

#variables needed 
robot_start_lat = 16.0
robot_start_lon = 82.0
robot_speed = 10
total_time = 0
total_distance = 0
i = 0
count = 0 

#for loop that runs 5 times for the 5 sites in the json file
for i in range(5):  
    if i == 0: 
        current_lat, current_lon = robot_start_lat, robot_start_lon
    else: 
        current_lat, current_lon = data['sites'][i-1]['latitude'], data['sites'][i-1]['longitude']
    next_lat, next_lon =  data['sites'][i]['latitude'], data['sites'][i]['longitude'] 
    distance = calc_gcd(current_lat,current_lon,next_lat,next_lon) 

    travel_time = distance/robot_speed 
    
    #checks the composition of meteorite and then assigns it sample time based on it 
    if data['sites'][i]['composition'] == 'stony': 
        sample_time = 1
    elif data['sites'][i]['composition'] == 'iron':
        sample_time = 2
    elif data['sites'][i]['composition'] == 'stony-iron':
        sample_time = 3 
    # calculates the total time     
    total_time += travel_time + sample_time 
    count += 1 
    #print statment for each leg of the trip 
    print("leg = ", count,",", f"time to travel = {travel_time:.2f} hr,", "time to sample = ", sample_time, " hr")  
    

#print statement for the total trip 
print("number of legs = ", count, ",", f"total time elapsed = {total_time:.2f} hr")

 

# Robotic Vehicle on Mars That Investigates Five Meteorite Landing Sites
The purpose of this project is to create a json file using a dictionary with one key whose value is a list of dictionaries. Then using those data values to calculate the 
time it takes for a robotic vehicle to get to the site of each landing, in order from the json list, from an initial starting point using the great-circle distance 
algorithm. Once at the site it will add a sample time based on the composition of the meteorite and then at the end will calculate the total time the robotic vehicle took
to travel and sample every meteorite on the list.

## Description of Pyhton Scripts 
This program has two parts: calculating_trip and generate_sites. 

calculating_trip: 
This script creates a json file called "sites.json" using a dictionary with one key word "sites" whose value is a list of dictionaries that include: site id, longitude,
latitude, and composition. 

generate_sites: This script takes the json file and uses the great-circle distance algorithm to find the amount of time it takes the robotic vehicle to reach each site, 
from the json list in order and sample the composition of the meteorite. It also splits each distance into "legs" and at the end of the script it calculates the total 
time of all the "legs" by adding the sample time to the travel time of each individual "leg."

## Running the Code
This code has two scripts to run: generate_sites and calculating_trip (run in that order). 

To create the json file needed for the calculations: run the generate_sites script.

To do the calculations for the entire trip using the json file created by generate_sites: run the calculating_trip script.

## Output 
If generate_sites runs correctly it will create a json file called "sites.json."

If calculating_trip runs correctly the output should look like this. 
![image](https://user-images.githubusercontent.com/122917623/215623585-e00c5add-b519-4f62-8ea9-16f4d5f172f8.png)

### Interpretation
To interpret this output from the image: each line starts with the leg the robotic vehicle is on. It then tells you the time it took to reach that site from the robotic
vehicles last location and the time it took to sample the meteorite at that location. The final line printed prints the number of sites visited and the total time it took
to get there and sample the meteorite.

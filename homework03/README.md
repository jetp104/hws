# Testing the Turbidity of Water and the Amount of Time it Takes to Decay

The purpose of this project was to be able to pull data from a URL using the requests library.
Once the data was obtained from the URL we then had to find the amount of Turbidity of the 
five most recent data points. After the turbidity is calculated, if it is greater than the NTU
value it will read the amount of time it takes for the water to be safe otherwise it reads the
water is safe and takes zero hours to be safe. 

## How to Access the Data Used for the Scripts 

To access the json data used for the scripts visit this link https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json

## Description of Python Scripts 
This program has one part and a unit test to go along: analyze_water and test_analyze_water

analyze_water: This script reads in the data from the URL using the requests library. After it
reads in the data it takes the most recent five data points and calculates the average turbidity.
After it calcualtes the turbidity if it is greater than the NTU it calcualtes the amount of 
time it takes for the water to become safe. 

test_analyze_water: This script calls analyze_water and tests the two functions within that 
script to make sure they are working properly. 

## Running the Code

This code has two scripts that can be ran: analyze_water and test_analyze_water. 

To see the calculations: run analyze_water.

To run the unit test use pytest. 

### Output 

If anaylze_water runs correctly it should look like this if the water is under the turbidity threshold. 

![image](https://user-images.githubusercontent.com/122917623/218228397-b31aa81b-0235-46af-a8f4-c187ac1bcf09.png)

and like this if it is above the turbidity threshold. 

![image](https://user-images.githubusercontent.com/122917623/218230160-aa79d579-23c1-4b4e-bc31-f8c6ab8f2d79.png)

If the test_analyze_water runs correctly it should look like this. 

![image](https://user-images.githubusercontent.com/122917623/218228636-2cef434d-214c-411f-8d48-be68564a2aff.png)

### Interpretation 
To interpret this output from the images: the first line for the analyze_water script will
always tell you the turbidity of the water in NTU. The next line will tell you the if the water is safe or not to use. The final line will tell you the amount of time 
it will take to be safe to use. If the turbidity is already lower than the threshold it will tell you say 0 hours because it is already safe. The last image shows the
sanity tests and type tests I wrote passing meaning the functions are working correctly. 







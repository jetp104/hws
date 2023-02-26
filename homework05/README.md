# Flask Application that Takes the ISS Data Set and Finds the Instananeous Velocity
The purpose of this project was to read in the ISS data from an xml link. Using the link I
had to find the data associated with the epochs. Then using that data with the epochs I
created a path to a single epoch. Once the single epoch was returned I calculated the
instantaneous velocity using the x_dot, y_dot, and z_dot value in the data set.

## How to Access the Data Used for the Flask App 
To access the xml file used for the app visit this link that will take you to the NASA
website.
https://spotthestation.nasa.gov/trajectory_data.cfm
Once there scroll down and choose the xml link which will take you to the data set. The data 
set we use has the ids of the epochs, each epochs x, y, and z location, and it's speeds in the
x, y, and z direction. 

## Description of Flask App 
iss_tracker.py: This app has multiple paths included inside it that can be run.
<br> path (/): This path returns the entire data set
<br> path (/keys): returns the list of keys associated with another key. Used only to find the 
<br> epochs data. 
<br> path (/epochs): This path returns the list of all the epochs in the data set
<br> path (/epochs/"epoch_id"): This path returns a specific epoch using its assigned id 
<br> path (/epochs/"epoch_id"/speed: This path returns the insantaneous speed of the specified epoch

## Instructions to Run the App
To run the application use the 
  
``` 
  flask --app iss_tracker --debug run
```
In another terminal run the command <br> 
for the first path 
 ```
  curl localhost:5000/
 ```
  <br>for the second path  
  ```
  curl localhost:5000/epochs/
  ```
  for the third path  
  ```
  curl localhost:5000/epochs/"2023-048T18:40:00.000Z"
  ``` 
  for the fourth path 
  ```
  curl localhost:5000/epochs/"2023-048T18:40:00.000Z"/speed
  ``` 
  for the fifth path
  ```
  curl localhost:5000/keys
  ```
 ## Examples 
 The first path will return you the entire data set. It will be done running when the last
  thing appears as 
  ![image](https://user-images.githubusercontent.com/122917623/219977884-7fe8ffa2-4024-4768-98f0-d882e412ad01.png)

  The second path will give you a large dictionary of epochs and there z, y, z, x_dot, 
  y_dot, and z_dot values associated. 
  
  The third path if ran correctly should return the specific epoch that was searched for 
  including its data which looks like this 
  ![image](https://user-images.githubusercontent.com/122917623/219978073-ea4ed4cc-23a6-4215-ae2d-dab5467698ef.png)
  
  The fourth path will just return a string with the speed of the epoch calculated from the 
  equation speed = sqrt(x_dot^2 + y_dot^2 + z_dot^2) which looks like this 
  
  ![image](https://user-images.githubusercontent.com/122917623/219978156-d8bd369c-52c6-41d3-a335-20cc4414ff84.png)

  The fifth path with the final list should look like the second path
  
  ## Interpretation of results
  The first path just return a list of dictionaries and all the values included with each key. 
  The second path returns every epoch in the data set 
  The third path will return the epcific epoch id that was specified in the path 
  The fourth path will return the instantaneous speed calculated from the specific epoch indicated earlier in the path. 
  The fifth path depending on which list you return will give you the keys associated with that dictionary. 

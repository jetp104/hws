# Undone (The Sweater Container)
Scenario: The API you developed for the ISS positional and velocity data (in homework 04) is a great start! But, there are many improvements we could make in order to make the API more useful. And, we can use some smart software engineering & design strategies to make our app more portable.

The purpose of this project was to add onto homework04. In homework04 The purpose of the project was to read in the ISS data from an xml link. Using the link I had to find the data associated with the epochs. Then using that data with the epochs I created a path to a single epoch. Once the single epoch was returned I calculated the instantaneous velocity using the x_dot, y_dot, and z_dot value in the data set. In this homework there is 3 added routes with 2 of them using completley new methods "DELETE" and "POST." Within this project aswell I used defensive coding to bar the user from crashing the program using bad inputs. 

## How to Access the Data Used for the Flask App
To access the xml file used for the app visit this link that will take you to the NASA website. https://spotthestation.nasa.gov/trajectory_data.cfm Once there scroll down and choose the xml link which will take you to the data set. The data set we use has the ids of the epochs, each epochs x, y, and z location, and it's speeds in the x, y, and z direction.

## Scripts
iss_tracker.py: This app has multiple paths included inside it that can be run.
<br>
path (/): This path returns the entire data set
<br>
path (/keys): Turns the list of keys associated with another key. Used only to find the epochs data.
<br>
path (/epochs): This path returns the list of all the epochs in the data set
<br>
path (/epochs?limt=int&offset=int): This path returns modified list of Epochs given query parameters
<br>
path (/epochs/"epoch_id"): This path returns a specific epoch using its assigned id
<br>
path (/epochs/"epoch_id"/speed: This path returns the insantaneous speed of the specified epoch
<br>
path (/delete-data): This path deletes the entire data set
<br> 
path (/post-data): This path reloads the dictionary object with data from the web

Dockerfile: A text file the contains everything needed to run the iss_tracker Docker image from the container. 

## Instructions 
To use the existing docker image use the commands in this order: 
```
docker pull jetp104/iss_tracker:hw05
```
```
docker run -it --rm -p 5000:5000 jetp104/iss_tracker:hw05
```
Make sure you are in the same repository as the iss_tracker.py file when you pull from docker

To build a new image from the docker file use the command: 
```
docker build -t <your_username>/iss_tracker:hw05 .
```
You will know the docker image sucessfuly built if you use the command: 
```
docker images
```

and it shows this 

![image](https://user-images.githubusercontent.com/122917623/221445327-b1568523-fb31-4b27-a99a-3021088d1ba6.png)

## Running Flask 
If the image is built properly your terminal will end up looking like this once you do the docker run command: 

![image](https://user-images.githubusercontent.com/122917623/221445496-6b4d4ded-8c43-4e4e-81de-6d2f2b348baf.png)

To Curl these commands use: 
```
curl 172.17.0.2:5000
```
The routes can be run using these commands: 

 ```
  curl 172.17.0.2:5000/
 ```
 which will output like this: 
 ![image](https://user-images.githubusercontent.com/122917623/221445650-0affeeec-cc4b-45da-b0fd-a471022ffa03.png)
 
  Interpretation: The list of all the data inside the xml file. 
 
  ```
  curl 172.17.0.2:5000/epochs
  ```
 
  which will output like this: 
  
  ![image](https://user-images.githubusercontent.com/122917623/221445749-24dc1647-ec8b-4f38-be9c-d15df475154b.png)
  
  Interpretation: The list of all the epoch id's 
  ```
  curl 172.17.0.2:5000/epochs/"2023-048T18:40:00.000Z"
  ``` 
  
  which will output like this: 
  
  ![image](https://user-images.githubusercontent.com/122917623/221445811-be03421e-8b0f-4a5f-81c8-8618143759a5.png)


  Interpretation: The data associated with the specific epoch id
  ```
  curl 172.17.0.2:5000/epochs/"2023-048T18:40:00.000Z"/speed
  ``` 
  
  which will output like this: 
  
  ![image](https://user-images.githubusercontent.com/122917623/221445869-b92c1ca8-3d44-4592-974c-f9d3cc253a07.png)

  Interpretation: The speed of the specific epoch id 
  ```
  curl 172.17.0.2:5000/keys
  ```
  
  which will output like this: 
  
  ![image](https://user-images.githubusercontent.com/122917623/221445971-0c2ad98a-2531-44f3-8cc6-75cdf0e3ae53.png)
  
  Interpration: The keys and list associated with the xml file. 

  The command for the next two paths only return strings but influence the data: 
  
  the first command is for /delete-data which will produce a string that says "Deleted" 
  
  ```
   curl -X DELETE 172.17.0.2:5000/delete-data
  ```
  
  the next command is for /post-data which will produce a string that says "data posted" 
  ```
  curl -X POST 172.17.0.2:5000/post-data
  ```
  
  ### Query Paramaters 
  The /epochs route has 2 query paramaters associated with it. The offset parameter (chooses a starting point for the epochs) and the limit parameter (limits the        amount of epochs that show up in the list. An example of this command would be: 
  ```
  curl '172.17.0.2:5000/epochs?limit=10&offset=500'
  ```
  This command will display 10 epochs starting from epoch number 500. 
  

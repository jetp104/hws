# Creating plots and continuing Kubernetes (Holidapp / Homework08)
Scenario: Your app (Flask API + Redis DB) has been deployed in Kubernetes, and now we are going to continue to build out some more features. First, we will write some code to dynamically assign the Redis client host IP. Second, we will add some functionality to write images to a Redis database and read images back out.

The purpose of this project is to be able to run asteroid data within kubernetes clusters and docker by getting the current IP rather than hard coding it. In this homework we also use matlibplot to create a simple graph for our dataset.

## Data used for the App 
The data used for this application was found by a user on Kaggle named MIR SAKHAWAT HOSSAIN. The data used for this app is a modifed version of the data found using this link https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset. The modified data can be found here with this link https://github.com/TreyGower7/AsteroidDataProject/blob/main/ModifiedAsteroidData.csv.

## Important files

`asteroid_data.py`: This is the main script of this project. The asteroid_data script is a Flask app that has 8 routes that are described in the table below. This script puts the asteroid data into a Redis database so the user can interact with the data with the different routes and also uses defensive programming stratigies to make sure the script runs without breaking, giving an error message if something is amiss

`Dockerfile`: This file containerzies the `asteroid_data.py` script. The image created by the dockerfile contains the same version of python used to cretae the script and other dependencies such as versions of: `redis`, `requests`, `Flask` and `matplotlib`. 

`docker-compose.yml`: `docker-compose.yaml`: This file is a compose file to automate the devlopment of the app. It configures the build image with the specified tag and binds it to the appropriate ports from the container to the host. This file also launchs redis along with containerized flask app. This file now also binds the host. 

`asteroid-test-redis-pvc.yml` This file creates the depolyment of a persistent volume claim that's used by the upcoming redis pods. 

`asteroid-test-redis-deployment` The file deploys all the redis pods

`asteroid-test-redis-service` This file deploys both the kubernetes and redis services 

`asteroid-test-flask-deployment` This file deploys flask kubernetes pods (2 pods in our case)

`asteroid-test-flask-service` This file deploys ths flask and kubernetes service

## Instructions to run these files on kubernetes 

To start deploying the all software to make it work properly use these commands in this order

```
kubectl apply -f asteroid-test-pvc.yml
kubectl apply -f asteroid-test-redis-deployment.yml
kubectl apply -f asteroid-test-redis-service.yml
kubectl apply -f asteroid-test-flask-deployment
kubectl apply -f asteroid-test-flask-service
```
This will create the Persistant Volume claim, deploy the kubernetes pods, and will deploy both the redis and flask services. If ran corectly when you should see this 

```
kubectl apply -f asteroid-test-pvc.yml
```
Output: 
![image](https://user-images.githubusercontent.com/122917623/231303331-28502b1c-36fe-456d-a3d3-e99c6284a742.png)

```
kubectl apply -f asteroid-test-redis-deployment.yml
```
Output: 
![image](https://user-images.githubusercontent.com/122917623/231303536-fdaf2c0e-1dd1-4143-afaa-30bd790baf60.png)

```
kubectl apply -f asteroid-test-redis-service.yml
```
Output: 
![image](https://user-images.githubusercontent.com/122917623/231303790-cf75c361-87cd-4ffd-afc4-f893a200c19a.png)

```
kubectl apply -f asteroid-test-flask-deployment
```
Output: 
![image](https://user-images.githubusercontent.com/122917623/231304056-25a71f1d-08a5-4e16-9c3e-ac062f2be9ae.png)

```
kubectl apply -f asteroid-test-flask-service
```
Output: 
![image](https://user-images.githubusercontent.com/122917623/231304240-ffae2364-71d6-455d-be65-db164da1b74c.png)

Use the command `kubectl get pods` and `kubectl get service` to make sure everything deployed properly 

![image](https://user-images.githubusercontent.com/122917623/231304420-9d4e2006-62d6-444c-a54f-badd54fcb44c.png)

![image](https://user-images.githubusercontent.com/122917623/231304473-d6508234-8e4c-4548-a665-faaa9de7cd21.png)

### If you want to build your own docker image 
It is important to note that for the Flask container to get deployed to kuberenets, it must come from Docker Hub. In this case the default image used "jetp104/asteroid_data:hw08" is pulled from docker hub and can be found here - https://hub.docker.com/repository/docker/jetp104/asteroid_data/general
To build your own image and use it for the k8s you must use the command 

`docker build -t <dockerhubusername>/<code>:<version> .`

you must then push your image by using the command 

`docker push <dockerhubusername>/<code>:<version>`

and then once the image is pushed to docker hub go into the file `asteroid-test-flask-deployment.yml` and change line 23 for to the image that you would want to use. If you would like to use the exisiting image leave the files as is and go to the `Using k8s` section

### Using K8s 
To use the k8s use the command 

`kubectl get service`

This should look like this and copy the cluster IP of the `asteroid-test-flask-service`

![image](https://user-images.githubusercontent.com/122917623/231304974-bfca8fb2-e45d-4749-b1dc-2d466da68f84.png)

Then use the command 

`kubectl exec -it <dev-python-pod-name> -- /bin/bash`

this will lead you to a shell that looks like this 

![image](https://user-images.githubusercontent.com/122917623/230494158-b19b4fbf-3563-4851-8da4-8a169fb3c924.png)

To curl in this shell use the command 

`curl <Cluseter IP>:5000/<route>`

The routes can be found below as well as the commands. This should be all you need to run kuberenetes

## Instructions to run the app using the exisiting image on Docker Hub

### Important: Do Before Use
Before you do this method create an empty director named "data", so the user has the ability to interact with the flask application.

To make a director called data use this command

```
mkdir data
```

1. To pull and use the exisitng image from Docker Hub

```
docker pull jetp104/asteroid_data:hw08
```

This will pull the image from online from Docker Hub 
If ran correctly it will soemthing like this if you try to pull again. 

![image](https://user-images.githubusercontent.com/122917623/231307124-1fbaadc4-6b84-4d00-987f-edc86580d731.png)

2. Set up the redis data base with the command

```
docker run -d -p 6379:6379 -v </path/on/host>:/data redis:7 --save 1 1
```

An example of this command is 

```
docker run -d -p 6379:6379 -v $(pwd)/data:/data:rw redis:7 --save 1 1
```

if ran correctly it will look like this

![image](https://user-images.githubusercontent.com/122917623/228094553-f6bbc614-8963-49b4-b240-a7d83d91ae25.png)


This will create a redis image and map the ports of 6379 from the container to the port 6379 of the user's host. 

Once redis is up and running you can use the command 

```
docker run -it --rm -p 5000:5000 jetp104/asteroid_data:hw08
```

if ran correctly it will look like this 

![image](https://user-images.githubusercontent.com/122917623/228094690-cbb96faf-4a3e-4205-8f59-dee88f7b16f6.png)

This will open the flask app and redis database at the same time. 

## Instructions to run the app and redis using docker-compose 

### Important: Do Before Use
Before you do this method create an empty director named "data", so the user has the ability to interact with the flask application.

To make a director called data use this command

```
mkdir data
```

1. With all the files inside the same director use the command 

```
docker-compose up
```
if done correctly it will look like this 

![image](https://user-images.githubusercontent.com/122917623/228094789-feb16b10-6f2b-472e-9c81-23d845bd39ce.png)


This will create both the redis container and the flask app and launch both of them simaltaneously 

To close the cointainers use the command 

```
docker-compose down
```

if done correctly it will look like this 

![image](https://user-images.githubusercontent.com/122917623/228095019-5808bf0f-3c54-43c3-bd5f-d438ddc876d6.png)


## Instructions to build a new docker image  

### Important: Do Before Use
Before you do this method create an empty director named "data", so the user has the ability to interact with the flask application.

To make a director called data use this command

```
mkdir data
```

To build a new image from the exisiting docker image, use the command 

```
docker build -t <dockerhubusername>/<code>:<version> .
```

An example of this command is 

```
docker build -t jetp104/asteroid_data:hw08 .
```

if done correctly it will look something like this 

![image](https://user-images.githubusercontent.com/122917623/228095471-463eec50-8b43-4563-a1a8-e1d7d3fe48ee.png)

## Flask routes
|Route|Method|What they do| 
|-----|------|------------|
|/data|POST|Put data into Redis|
|/data|GET|Return all data from Redis|
|/data|DELETE|Delete data in Redis| 
|/asteroids|GET|Return a json-formatted list of all asteroids|
|/asteroids/<asteroid_name>|GET|Return all data associated with specifc asteroid name| 
|/image|GET|return the image to the user, if present in the database.
|/image|POST|read some portion of data out of the database (db=0), run some matplotlib code to create a simple plot of that data, then write the resulting plot back into the database (db=1).
|/image|DELETE|delete the image from the database.



## Running the app
To run the app you will use 1 of three commands that will all be outlined with example inputs here.

1. 
```
curl localhost:5000/ROUTE
```
2. 
```
curl -X POST localhost:5000/ROUTE
```
3.
```
curl -X DELETE localhost:5000/ROUTE
```

### Sample outputs of each route

```
curl -X POST localhost:5000/data
```
if done correctly the output will be

![image](https://user-images.githubusercontent.com/122917623/231546161-16149e5d-1d29-4daf-b69c-a4db4491af42.png)

Interpretation: The data has been posted to the redis database 

```
curl -X DELETE localhost:5000/data
```

![image](https://user-images.githubusercontent.com/122917623/231546312-1d66b2f1-4ae2-4894-8864-3135977f6690.png)

Interpretation: The data from the redis database was deleted. 

```
curl localhost:5000/data
```

![image](https://user-images.githubusercontent.com/122917623/231546524-d968b560-0f25-44bd-84a5-c3d3ca7d96cf.png)

Interpretation: The value of each key associated with the asteroid data (shows the entire dataset) 

```
curl localhost:5000/data
```

```
curl localhost:5000/asteroids
```

![image](https://user-images.githubusercontent.com/122917623/231546775-ecc28053-be63-4655-abd9-76c9925380d5.png)

Interpretation: Returns a list of the name of all the asteroids in the dataset

```
curl localhost:5000/asteroids/"<asteroid_name>"
```

![image](https://user-images.githubusercontent.com/122917623/231547101-88ce580a-a1ae-4e34-907b-de979715aceb.png)

Interpreation: Returns all values associated with a specific asteroid in the data set 

```
curl -X POST localhost:5000/image 
```

![image](https://user-images.githubusercontent.com/122917623/231547410-0336e32c-497a-4f5f-a894-7023dde2eadb.png)

Interpretation: An image was created a posted to a second redis database 

```
curl -X DELETE localhost:5000/image 
```

![image](https://user-images.githubusercontent.com/122917623/231547736-54b4e02b-e0cf-4c84-801f-9ffd3017b995.png)

Interpreation: The graph was deleted out of the 2nd redis database 

```
curl localhost:5000/image --output <filename> 
```

![image](https://user-images.githubusercontent.com/122917623/231548281-da3bb8ab-82de-467c-9ba7-e3e661a8251a.png)

Interpreatation: The image was outputted into bytes into the name of the file you gave it
















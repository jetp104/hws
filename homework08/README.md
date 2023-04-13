# Creating plots and continuing Kubernetes (Holidapp / Homework08)
Scenario: Your app (Flask API + Redis DB) has been deployed in Kubernetes, and now we are going to continue to build out some more features. First, we will write some code to dynamically assign the Redis client host IP. Second, we will add some functionality to write images to a Redis database and read images back out. 

The purpose of this project is to be able to run the hgnc data set in the last homework within a kubernetes cluster and in docker by creating yaml files for the kuberenetes and changing the host in the gene_api script. The host is changed to find the current host IP it is on rather than hard coding it in. We also want to create a plot with the hgnc data.  

## Data used for the App 
The data used for this application was supplied by The Hugo Gene Nomenclature Committee (HGNC) which is overseen by The Human Genome Organization (HUGO). The data can be found using this link https://www.genenames.org/download/archive/ to their website. Once at the website scroll down and choose the Current JSON format hgnc_complete_set file.  

## Important files

`gene_api.py`: This is the main script of this project. The gene_api script is a Flask app that has 8 routes that are described in the table below. This script puts the HGNC data into a Redis database so the user can interact with the data with the different routes and also uses defensive programming stratigies to make sure the script runs without breaking, giving an error message if something is amiss. 

`Dockerfile`: This file containerzies the `gene_api.py` script. The image created by the dockerfile contains the same version of python used to cretae the script and other dependencies such as versions of: `redis`, `requests`, and `Flask`

`docker-compose.yaml`: This file is a compose file to automate the devlopment of the app. It configures the build image with the specified tag and binds it to the appropriate ports from the container to the host. This file also launchs redis along with containerized flask app. 

`jetp104-test-redis-pvc.yml` This file creates the depolyment of a persistent volume claim that's used by the upcoming redis pods. 

`jetp104-test-redis-deployment` The file deploys all the redis pods

`jetp104-test-redis-service` This file deploys both the kubernetes and redis services 

`jetp104-test-flask-deployment` This file deploys flask kubernetes pods (2 pods in our case) 

`jetp104-test-flask-service` This file deploys ths flask and kubernetes service

## Instructions to run these files on kubernetes 

To start deploying the all software to make it work properly use these commands in this order

```
kubectl apply -f jetp104-test-pvc.yml
kubectl apply -f jetp104-test-redis-deployment.yml
kubectl apply -f jetp104-test-redis-service.yml
kubectl apply -f jetp104-test-flask-deployment
kubectl apply -f jetp104-test-flask-service
```
This will create the Persistant Volume claim, deploy the kubernetes pods, and will deploy both the redis and flask services. If ran corectly when you use the

`kubectl get pods` 

command this is what you should see

![image](https://user-images.githubusercontent.com/122917623/230490868-f19f9f0f-b025-4e69-89ab-21ffab9aa0e3.png)

`kubectl get service` 

command you should see this 

![image](https://user-images.githubusercontent.com/122917623/230490993-dcfbc653-c2a8-4ecd-8b4f-9121c32e3c0d.png)

 
### If you want to build your own docker image 
It is important to note that for the Flask container to get deployed to kuberenets, it must come from Docker Hub. In this case the default image used "jetp104/gene_api:hw07" is pulled from docker hub and can be found here -  https://hub.docker.com/repository/docker/jetp104/gene_api/general


To build your own image and use it for the k8s you must use the command 

`docker build -t <dockerhubusername>/<code>:<version> .`

you must then push your image by using the command 

`docker push <dockerhubusername>/<code>:<version>`

and then once the image is pushed to docker hub go into the file `jept104-test-flask-deployment.yml` and change line 24 for to the image that you would want to use. If you would like to use the exisiting image leave the files as is and go to the `Using k8s` section

### Using K8s 
To use the k8s use the command 

`kubectl get service` 

This should look like this and copy the cluster IP of the `jetp104-test-flask-service`

![image](https://user-images.githubusercontent.com/122917623/230490993-dcfbc653-c2a8-4ecd-8b4f-9121c32e3c0d.png)

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
docker pull jetp104/gene_api:hw06
```

This will pull the image from online from Docker Hub 
If ran correctly it will soemthing like this if you try to pull again. 

![image](https://user-images.githubusercontent.com/122917623/228094437-9683446f-ef14-4972-b57c-1175570a56d6.png)


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
docker run -it --rm -p 5000:5000 jetp104/gene_api:hw06
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
docker build -t jetp104/gene_api:hw06 .
```

if done correctly it will look something like this 

![image](https://user-images.githubusercontent.com/122917623/228095471-463eec50-8b43-4563-a1a8-e1d7d3fe48ee.png)

## Flask routes
|Route|Method|What they do| 
|-----|------|------------|
|/data|POST|Put data into Redis|
|/data|GET|Return all data from Redis|
|/data|DELETE|Delete data in Redis| 
|/genes|GET|Return json-formatted list of all hgnc_ids| 
|/genes/<hgnc_id>|GET|Return all data assocciated with specified id| 
|/image|GET|return the image to the user, if present in the database.|
|/image|POST|read some portion of data out of the database (db=0), run some matplotlib code to create a simple plot of that data, then write the resulting plot back into the database (db=1).|
|/image|DELETE|delete the image from the database.| 
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

![image](https://user-images.githubusercontent.com/122917623/228095814-49f4cebe-8417-4f5d-8406-dfdc440f76f4.png)

Interpreation: The data has succesfully been posted into a redis database

```
curl localhost:5000/data
```

if done correctly the output will be 

![image](https://user-images.githubusercontent.com/122917623/228096501-83a2284a-3a1f-47c9-acfb-62a24380499b.png)


Interpretation: This is all the data that was included within the HGNC data set

```
curl -X DELETE localhost:5000/data
```

if done correctly the output will be 

![image](https://user-images.githubusercontent.com/122917623/228096569-e46f1ab8-3b4b-46dc-b6fb-538135302696.png)


Interpretation: The data that was stored in the redis database was sucessfully deleted

```
curl localhost:5000/genes
```

if done correctky the output will be 

![image](https://user-images.githubusercontent.com/122917623/228096819-35cd69c5-8273-4ae3-9280-ace843cc97cd.png)

Interpretation: This is a Json list of all the HGNC ids associated inside the data set

```
curl localhost:5000/genes/"HGNC:24523"
```
If done correctly the output will be 

![image](https://user-images.githubusercontent.com/122917623/228096961-e98ba66c-8159-42ae-aad8-ef4ef7d0ef51.png)

Interpretation: This return a dictionary of all the values associated with the single HGNC id specified by the user

```
curl localhost:5000/image --output <filename> 
```
If done correctly the output will be

![image](https://user-images.githubusercontent.com/122917623/231886549-c70d7b64-6606-4588-93e9-c8560f796e6c.png)

Interpreation: This will create a file that has the png image from the data in bytes form

```
curl -X POST localhost:5000/data
```
If one correctly the output will be 

![image](https://user-images.githubusercontent.com/122917623/231886323-afb93f18-9dec-4ae1-a2ab-0ed9e7e8f326.png)

Interpretation: This will post the image into a seperate redis database

```
curl -X DELETE localhost:5000/data
```
If done correctly the output will be 

![image](https://user-images.githubusercontent.com/122917623/231886685-cfc7dac3-6391-4cd2-bc81-dbdcb3b2bf21.png)

Interpretation: The graph image was deleted from the redis database

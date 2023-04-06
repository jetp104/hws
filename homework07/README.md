# Containerizing Redis (Say It Ain’t Genes / Homework06)
Scenario: We are going to turn our attention to a brand new dataset. The Human Genome Organization (HUGO) is a non-profit which oversees the HUGO Gene Nomenclature Committee (HGNC). The HGNC “approves a unique and meaningful name for every gene”. For this homework, we will download the complete set of HGNC data and inject it into a Redis database through a Flask interface.

The purpose of this project is to get the HGNC dataset into a redis database and then launch both the containerized the flask application with the redis database by using a docker compose file. 

## Data used for the App 
The data used for this application was supplied by The Hugo Gene Nomenclature Committee (HGNC) which is overseen by The Human Genome Organization (HUGO). The data can be found using this link https://www.genenames.org/download/archive/ to their website. Once at the website scroll down and choose the Current JSON format hgnc_complete_set file.  

## Important files

`gene_api.py`: This is the main script of this project. The gene_api script is a Flask app that has 5 routes that are described in the table below. This script puts the HGNC data into a Redis database so the user can interact with the data with the different routes and also uses defensive programming stratigies to make sure the script runs without breaking, giving an error message if something is amiss. 

`Dockerfile`: This file containerzies the `gene_api.py` script. The image created by the dockerfile contains the same version of python used to cretae the script and other dependencies such as versions of: `redis`, `requests`, and `Flask`

`docker-compose.yaml`: This file is a compose file to automate the devlopment of the app. It configures the build image with the specified tag and binds it to the appropriate ports from the container to the host. This file also launchs redis along with containerized flask app. 

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


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









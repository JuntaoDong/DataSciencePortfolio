# Project1 - Docker and WebServices

### Image url: juntaodong/weatherapi
### local visit url: http://172.17.0.2:8081/

### Command: 
```
docker pull juntaodong/weathereapi
docker run -d -p 8081:80 juntaodong/weatherapi
```

### Workflow
* Edit Dockerfile: 

Pull base docker image "tiangolo/uwsgi-nginx-flask:python2.7" from docker hub. Make changes based on the base image including copying api file and its dependencies to docker image and installing the required packages in python via requirements.txt. Add commond lines.
* Edit requirements.txt:

Input the python packages that are needed for this api.
* Directory structure:
```
.
├── Dockerfile
├── requirements.txt
├── app
    ├── weather.py
    ├── daily.csv
    ├── daily.db
    ├── static
        ├── style.css
        ├── .js files
    ├── templates
        ├── index.html
```
* Build docker image:
```
docker build -t weatherapi .
```
* Push to docker hub:
```
docker commit <containerID> juntaodong/weatherapi
docker push juntaodong/weatherapi
```


# Deployment

### Prerequisite

1. OS:
Ubuntu 18.04

1. Install docker
```bash
sudo apt update
sudo apt install docker.io
```

### Get the docker image

```bash
sudo docker pull ouankou/rds:threadsanitizer
```
### Create a container

```bash
sudo docker run -it --name rds_tsan ouankou/rds:threadsanitizer bash
```

### Start a container

```bash
sudo docker start rds_tsan
```

### Enter a container

```bash
sudo docker exec -it rds_tsan bash
```

### ThreadSanitizer usage

Follow the official guide or other instructions.

https://clang.llvm.org/docs/ThreadSanitizer.html

https://github.com/passlab/RaceDetectionService/blob/master/tools_output/README.md

### Flask development

Flask framework under python3 has been installed in the docker image.
For now, we could mannually mount or download the source code of Flask server into the container and run it.


To deploy the Flask server, we also need to map the host port to the docker container port.
For example, assume we have an available Flask server running on the port 5000 in the container. The port 5001 on the host is assigned to the microservice. While creating the container, the port mapping is needed as follows.

```bash
# assume Flask source code is located in $HOME/flask
sudo docker run -it -p 5001:5000 --name rds_tsan -v $HOME/flask:/opt/flask ouankou/rds:threadsanitizer bash
```
Then inside the containe, start the Flask server.
```bash
cd /opt/flask
export FLASK_APP=Flask_TSan.py
flask run --host=0.0.0.0
```

Finally, on the host browser we can access the microservice at `127.0.0.1:5001`. For other external machine, it can be accessed at `<host_ip>:5001`.



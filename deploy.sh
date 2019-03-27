#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/commerce &&
git pull

#edit
source ~/.profile
echo "$DOCKERHUB_PASS" | sudo docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop commerce
sudo docker rm commerce
sudo docker rmi fsyahrulah/commerce
sudo docker run -d --name commerce -p 5000:5000 fsyahrulah/commerce:latests

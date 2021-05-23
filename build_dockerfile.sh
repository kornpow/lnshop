#!/bin/bash
# install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

docker volume create lnshop

sudo apt install awscli

# Use the credentials with profile
export AWS_PROFILE=skorn

# Build dockerfile on dev machine
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 190928636648.dkr.ecr.us-east-2.amazonaws.com


python3 manage.py createsuperuser



API_VERSION=0.0.5
docker build -t lnpyshop .

docker tag lnpyshop:latest 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION
docker push 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION


# Run docker image on server
docker pull 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION
docker pull 190928636648.dkr.ecr.us-east-2.amazonaws.com/frontend:$UI_VERSION

docker run -p 12345:8000 -v lnshop:/db -d 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION

docker run -p 12345:8000 --name "lnshop" -v lnshop:/db -d lnpyshop


docker run -d -p 80:80 --name web2 frontend


# Start nginx reverse proxy
docker run -d \
    --name nginx-proxy \
    --publish 80:80 \
    --publish 443:443 \
    --volume /etc/nginx/certs \
    --volume /etc/nginx/vhost.d \
    --volume /usr/share/nginx/html \
    --volume /var/run/docker.sock:/tmp/docker.sock:ro \
    mattjeanes/jwilder-nginx-proxy-arm64
    # jwilder/nginx-proxy \
    


# Start letsencrypt helper
docker run -d \
    --name nginx-proxy-letsencrypt \
    --volumes-from nginx-proxy \
    --volume /var/run/docker.sock:/var/run/docker.sock:ro \
    --env "DEFAULT_EMAIL=korn94sam@gmail.com" \
    jrcs/letsencrypt-nginx-proxy-companion


# Tear t
docker rm -f nginx-proxy nginx-proxy-letsencrypt

# Build and run API
docker build -t lnpyshop .

docker run -d --name lnshop -v lnshop:/db \
    --env "VIRTUAL_HOST=api.btcmemes.com" \
    --env "VIRTUAL_PORT=8000" \
    --env "LETSENCRYPT_HOST=api.btcmemes.com" \
    --env "LETSENCRYPT_EMAIL=korn94sam@gmail.com" \
    lnpyshop:$API_VERSION

# Tear down API
docker rm -f lnshop

# Build and run Frontend
npm run build
docker build . -t frontend

docker run -d --name web3  \
    --env "VIRTUAL_HOST=chaosn.coffee" \
    --env "LETSENCRYPT_HOST=chaosn.coffee"  \
    --env "LETSENCRYPT_EMAIL=korn94sam@gmail.com" \
    190928636648.dkr.ecr.us-east-2.amazonaws.com/frontend:$UI_VERSION

# Tear down Frontend
docker rm -f web3



API_VERSION=0.0.6
docker tag lnpyshop:latest 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION
docker push 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION


UI_VERSION=0.0.6
docker tag frontend:latest 190928636648.dkr.ecr.us-east-2.amazonaws.com/frontend:$UI_VERSION
docker push 190928636648.dkr.ecr.us-east-2.amazonaws.com/frontend:$UI_VERSION


### ***** SERVER SIDE ***** ###
UI_VERSION=0.0.6
API_VERSION=0.0.6


# Run docker image on server
docker pull 190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$UI_VERSION
docker pull 190928636648.dkr.ecr.us-east-2.amazonaws.com/frontend:$API_VERSION


docker run -d --name lnshop -v lnshop:/db \
    --env "VIRTUAL_HOST=api.btcmemes.com" \
    --env "VIRTUAL_PORT=8000" \
    --env "LETSENCRYPT_HOST=api.btcmemes.com" \
    --env "LETSENCRYPT_EMAIL=korn94sam@gmail.com" \
    190928636648.dkr.ecr.us-east-2.amazonaws.com/lnpyshop:$API_VERSION



docker run -d --name web3  \
    --env "VIRTUAL_HOST=chaosn.coffee" \
    --env "LETSENCRYPT_HOST=chaosn.coffee"  \
    --env "LETSENCRYPT_EMAIL=korn94sam@gmail.com" \
    190928636648.dkr.ecr.us-east-2.amazonaws.com/frontend:$UI_VERSION

    
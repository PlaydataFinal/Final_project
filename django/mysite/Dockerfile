# pull official base image
FROM tensorflow/tensorflow:2.16.0rc0 
COPY . /usr/src/app/
WORKDIR /usr/src/app/

# Update and install system packages
RUN apt update
RUN apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config libgl1-mesa-glx

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



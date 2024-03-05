# pull official base image
FROM tensorflow/tensorflow:2.16.0rc0 
COPY . /usr/src/app/
WORKDIR /usr/src/app/
RUN apt update
RUN apt install python3-dev default-libmysqlclient-dev build-essential pkg-config -y
#RUN apt add python3-dev musl-dev zlib-dev jpeg-dev  #--(5.2)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


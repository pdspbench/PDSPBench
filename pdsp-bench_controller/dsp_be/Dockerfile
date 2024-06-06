# base image  
FROM python:3.10   
# setup environment variable  
ENV DockerHOME=/home/PDSPBench 
# creating a directory
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# Install JAVA
RUN apt-get update 
RUN apt-get install -y software-properties-common
RUN apt-get install -y --no-install-recommends apt-transport-https
RUN apt-get clean

#RUN add-apt-repository -y ppa:openjdk-r/ppa
#RUN apt-get update
RUN  apt-get install -y --no-install-recommends default-jdk
RUN  apt-get install -y docker.io
#RUN apt-get install -y ansible

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r dsp_be/requirements.txt  

RUN mkdir -p /home/legion/.ssh
#RUN mkdir -p /etc/ansible
COPY ./id_rsa /home/legion/.ssh/id_rsa
COPY ./id_rsa.pub /home/legion/.ssh/id_rsa.pub
#COPY ./ansible.cfg /etc/ansible/ansible.cfg
WORKDIR /home/PDSPBench/dsp_be
RUN python manage.py makemigrations
RUN python manage.py migrate
# port where the Django app runs  
EXPOSE 8000

# start server  
#ENTRYPOINT ["/bin/bash"]
CMD python manage.py runserver 0.0.0.0:8000
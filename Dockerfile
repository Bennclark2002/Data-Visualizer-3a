# syntax=docker/dockerfile:1


FROM python:3.10.11
#setup working directory

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

USER root

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


# WORKDIR /work

# FROM python:3.10.11

# # copy requirements
# COPY requirements.txt ./

# RUN pip3 install -r requirements.txt
# RUN pip3 install flask
# #set user to non root
# USER root
# #copy the python files over
# COPY / /work/


# EXPOSE 5000

# CMD [ "python3","server.py" ]


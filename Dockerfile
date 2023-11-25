# syntax=docker/dockerfile:1


FROM python:3.10.11
#setup working directory

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install flask

USER root

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]



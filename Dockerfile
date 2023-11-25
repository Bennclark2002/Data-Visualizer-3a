FROM python:3.10.11
#setup working directory


WORKDIR /work
# copy requirements
COPY requirements.txt ./

RUN pip3 install -r requirements.txt
RUN pip3 install flask
#set user to non root
USER root
#copy the python files over
COPY / /work/


EXPOSE 5000
ENV FLASK_APP=server.py
CMD [ "python3","-m","flask", "run","--host=0.0.0.0"]

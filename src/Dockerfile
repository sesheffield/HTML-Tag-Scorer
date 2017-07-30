 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN pip3 install mysqlclient
 RUN pip3 install HTMLParser
 RUN pip3 install Flask
 RUN pip3 install watchdog 
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/

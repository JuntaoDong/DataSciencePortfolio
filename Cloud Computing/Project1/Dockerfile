FROM tiangolo/uwsgi-nginx-flask:python2.7
MAINTAINER Juntao Dong

EXPOSE 8081
COPY ./app /app
COPY requirements.txt ./
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["weather.py"]


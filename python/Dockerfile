FROM python:3.9

RUN pip install mysql-connector-python pandas flask pyyaml

WORKDIR /usr/app/src

EXPOSE 7007

COPY api.py ./

COPY data_to_load/ ./
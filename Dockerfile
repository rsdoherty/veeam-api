# Python runtime with pyodbc to connect to SQL Server
FROM ubuntu:16.04

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https software-properties-common python3-pip build-essential libssl-dev libffi-dev python3-dev\
    && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install python3.7 -y

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql unixodbc-dev

# install necessary locales
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

COPY requirements.txt ./app/requirements.txt
RUN pip3 install -r ./app/requirements.txt
COPY app.py ./app/app.py

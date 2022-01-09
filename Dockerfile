FROM ubuntu
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y curl git vim python3 python3-pip

WORKDIR /workdir
COPY /workdir/requirements.txt /workdir
COPY /workdir/main.py /workdir

RUN pip install -r /workdir/requirements.txt

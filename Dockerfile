FROM python:2.7
ADD . /app
WORKDIR /app
RUN apt-get update && apt-get -y install sudo libmysqlclient-dev
RUN groupadd -r user && useradd -r -g user user | chpasswd && adduser user sudo
RUN pip install -r requirements.txt
RUN sudo chown -R user ./
USER user

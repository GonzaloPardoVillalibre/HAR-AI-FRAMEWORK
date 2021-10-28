FROM python:3

RUN pip install toolz \
    pip install numpy \
    pip install pandas \
    pip install progressbar

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install sudo

ARG USER=docker
ARG UID=1000
ARG GID=1000
ARG PW=123400

RUN useradd -m ${USER} --uid=${UID} && echo "${USER}:${PW}" | \
      chpasswd
RUN usermod -aG sudo docker

USER docker

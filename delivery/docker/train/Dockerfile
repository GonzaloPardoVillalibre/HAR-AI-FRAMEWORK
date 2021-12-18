FROM nvcr.io/nvidia/tensorflow:21.11-tf2-py3

COPY requirements.txt /src/
RUN pip install -r /src/requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install sudo bash-completion

ARG USER=docker
ARG UID=1000
ARG GID=1000
ARG PW=123400

RUN useradd -m ${USER} --uid=${UID} && echo "${USER}:${PW}" | \
      chpasswd
RUN usermod -aG sudo docker

USER docker

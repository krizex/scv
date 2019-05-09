FROM ubuntu:18.04
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt update
# install Python3
RUN apt install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN apt install -y build-essential
RUN apt install -y python-dev
RUN apt install -y libjpeg8-dev zlib1g-dev
RUN apt install -y vim iputils-ping


RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

RUN apt install -y node-less

COPY src/ /app/
WORKDIR /app
EXPOSE 8000

CMD ./server.sh start

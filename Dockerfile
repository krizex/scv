FROM ubuntu:18.04 as builder
RUN apt update \
    && apt install -y wget \
    && apt install -y build-essential


# install ta-lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar xzvf ta-lib-0.4.0-src.tar.gz && cd ta-lib && mkdir /usr-tmp && ./configure --prefix=/usr-tmp && make && make install

# --------------------
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

# install ta-lib
COPY --from=builder /usr-tmp /usr
ENV LD_LIBRARY_PATH /usr/lib

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN apt install -y libjpeg8-dev zlib1g-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

RUN apt install -y vim

COPY src/ /app/
WORKDIR /app
EXPOSE 8000

CMD ./run-server.sh

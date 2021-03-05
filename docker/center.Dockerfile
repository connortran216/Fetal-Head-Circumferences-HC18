FROM python:3.6.8


ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y tzdata tk-dev apt-utils locales

RUN locale-gen en_US.UTF-8

# set locale
ENV LANG C.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=Asia/Ho_Chi_Minh


RUN apt-get update && apt-get install -y --no-install-recommends

RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "LANG=en_US.UTF-8" >> /etc/locale.conf

RUN locale-gen en_US.UTF-8
RUN apt-get install -y build-essential software-properties-common gcc g++ musl-dev

RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi
RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install gunicorn
RUN pip install uvicorn
RUN pip install python-multipart
RUN pip install Cython
# RUN pip install json
RUN pip install requests

ENV PYTHONPATH=/app

EXPOSE 8008
# command to run on container start
# CMD [ "python", "center_processing.py" ]

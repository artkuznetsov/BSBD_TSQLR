FROM python:latest

ENV PYTHONUNBUFFERED 1

#####################################################################################################################
################################################# INSTALLING FFMPEG ##################################################
RUN apt-get update ; apt-get install -y git build-essential gcc make yasm autoconf automake cmake libtool checkinstall libmp3lame-dev pkg-config libunwind-dev zlib1g-dev libssl-dev

RUN apt-get update \
    && apt-get clean \
    && apt-get install -y --no-install-recommends libc6-dev libgdiplus wget software-properties-common

RUN apt-get install -y python-setuptools unixodbc-dev graphviz libgraphviz-dev pkg-config python-dev
RUN apt-get install -y libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get install -y mysql-client unixodbc-bin

RUN curl -SL https://dev.mysql.com/get/Downloads/Connector-ODBC/5.3/mysql-connector-odbc-5.3.9-linux-ubuntu17.04-x86-64bit.tar.gz | tar -zxC /opt
RUN cp /opt/mysql-connector-odbc-5.3.9-linux-ubuntu17.04-x86-64bit/lib/libmyodbc5* /usr/lib/x86_64-linux-gnu/odbc/
RUN /opt/mysql-connector-odbc-5.3.9-linux-ubuntu17.04-x86-64bit/bin/myodbc-installer -d -a -n "MySQL ODBC 5.3 ANSI Driver" -t "DRIVER=/usr/lib/x86_64-linux-gnu/odbc/libmyodbc5a.so;"
RUN /opt/mysql-connector-odbc-5.3.9-linux-ubuntu17.04-x86-64bit/bin/myodbc-installer -d -a -n "MySQL ODBC 5.3 Unicode Driver" -t "DRIVER=/usr/lib/x86_64-linux-gnu/odbc/libmyodbc5w.so;"
######################################################################################################################

# Requirements are installed here to ensure they will be cached.
COPY ./config /config
RUN pip install --no-cache-dir -r /config/requirements_dev.txt
RUN pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"


COPY ./compose/dev/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


COPY . /src



WORKDIR /src
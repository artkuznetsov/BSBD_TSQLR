# Testing of the SQL Requests

Required - >=Python3.4
sudo su
sudo apt-get update
sudo apt-get install git
git clone https://github.com/artkuznetsov/BSBD_TSQLR.git
sudo apt-get install mysql-server

Create Database for Application (see configuration TestApp/settings.py). Default: testbsbd

mysql -u root -p
mysql>create database testbsbd charset=utf8;
mysql>exit;

sudo apt-get install python3-setuptools
sudo apt-get install python3-pip
sudo pip3 install pymysql
sudo apt-get install unixodbc-dev
sudo pip3 install pyodbc
sudo pip3 install pytz
sudo pip3 install sqlalchemy
sudo apt-get install graphviz libgraphviz-dev pkg-config
sudo pip3 install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"
sudo pip3 install eralchemy
sudo pip3 install django-tinymce

Install libraries for working with images:

sudo apt-get install python3-dev
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk
sudo apt-get install pillow



All required libraries has been installed and now we can to migrate
project's database; For this run following command:

python3 manage.py migrate


Now we need to create a superuser:

python3 manage.py createsuperuser


Install MySQL ODBC Driver:

sudo apt-get install mysql-client
sudo apt-get install libmyodbc unixodbc-bin

find / -name 'lib*odbc*.so'

OUTPUT (EXAMPLE):
/usr/lib/x86_64-linux-gnu/odbc/liboplodbcS.so
/usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
/usr/lib/x86_64-linux-gnu/odbc/libodbcmyS.so
/usr/lib/x86_64-linux-gnu/odbc/libodbcminiS.so
/usr/lib/x86_64-linux-gnu/odbc/libmyodbc.so
/usr/lib/x86_64-linux-gnu/odbc/libodbctxtS.so
/usr/lib/x86_64-linux-gnu/odbc/liboraodbcS.so
/usr/lib/x86_64-linux-gnu/odbc/libodbcdrvcfg2S.so
/usr/lib/x86_64-linux-gnu/odbc/libodbcdrvcfg1S.so
/usr/lib/x86_64-linux-gnu/odbc/libodbcnnS.so
/usr/lib/x86_64-linux-gnu/libodbcinst.so
/usr/lib/x86_64-linux-gnu/libodbccr.so
/usr/lib/x86_64-linux-gnu/libodbc.so

nano /etc/odbcinst.ini

[MySQL]
Description     = ODBC for MySQL
Driver          = /usr/lib/x86_64-linux-gnu/odbc/libmyodbc.so
Setup           = /usr/lib/x86_64-linux-gnu/odbc/libodbcmyS.so
UsageCount      = 1

nano /etc/odbc.ini

[MySQL]                                    # this is your system D$
Description = description of your DSN
Driver      = MySQL                        # custom driver name
Server      = localhost                    # or external IP if nee$
Port        = 3306                         # or custom port if nee$
Socket      = /var/run/mysqld/mysqld.sock  # socket, see above
Database    = testbsbd                     # MySQL DB name or empty
Option      = 3
ReadOnly    = No

Install the ODBC driver:

odbcinst -i -d -f /etc/odbcinst.ini

Install your system DSN:

odbcinst -i -s -l -f /etc/odbc.ini

Test if your system DSN was installed successfully: 

odbcinst -s -q

OUTPUT (EXAMPLE):
[MySQL]

Currently we should to create white mysql database which can see an users and shadow database for check SQL requests.

mysql -u root -p
mysql> create database whitedb;
mysql> create database shadowdb;
mysql> exit

Example for connection string to whitedb and shadowdb:

DRIVER={MySQL}; DATABASE=whitedb; SERVER=localhost; UID=root; PWD=12345;
DRIVER={MySQL}; DATABASE=shadowdb; SERVER=localhost; UID=root; PWD=12345;


Setting Up App in Docker
^^^^^^^^^^^^^^^^^^^^^

* Build Docker

    $ sudo docker-compose build
    $ sudo docker-compose up

* To create an **superuser account**, use this command::

    $ sudo docker-compose run --rm web python manage.py createsuperuser

* Create Test database in docker for test

    $ sudo docker exec -it Postgres-BSBD bash
    $ psql -h db1 postgres debug
    $ CREATE DATABASE test owner debug;

* Connection string for test database

    dbname=test host=db1 user=debug password=debug

At the moment app with Docker support only postgres


# BSBD_TSQLR
Web application for check of knowledges at testing SQL requests

Setting Up App in Docker


* Build Docker
    ```
    $ sudo docker-compose build
    $ sudo docker-compose up
    ```

* To create an **superuser account**, use this command::
    ```
    $ sudo docker-compose run --rm web python manage.py createsuperuser
    ```

* Create Test database in docker for test

    ```
    $ sudo docker exec -it Postgres-BSBD bash
    $ psql -h db1 postgres debug
    $ CREATE DATABASE test owner debug;
    ```

* Connection string for test database

    ```
    dbname=test host=db1 user=debug password=debug
    ```

At the moment app with Docker support only postgres

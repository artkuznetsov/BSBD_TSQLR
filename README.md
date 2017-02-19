# BSBD_TSQLR
Web application for check of knowledges at testing SQL requests

Instruction for installation BSBD_TSQLR project:
1) Install python
2) Install mysql
3) install pymysql driver
4) install pytz
5) install django
6) You need to create MySQL database. In the peoject using a default database name as testbsbd.
  1.1) If you work with linux - follow this script for create database testbsbd:
  >mysql -u root -p
  Enter password:
  mysql> create database testbsbd;
  mysql> GRANT ALL PRIVILEGES ON testbsbd.* TO root@localhost IDENTIFIED BY '12345';
  mysql>exit
  PS:password 12345 as default password in TestApp/settings.py file. You can to change this password if you need.
7) In the project directory enter this:
  7.1) python manage.py migrate jet
  7.2) python manage.py collectstatic
  7.3) python manage.py migrate dashboard
  7.4) python manage.py collectstatic
  7/5) python manage.py migrate
  
  If you got a various error messages during installation BSBD_TSQLR - please contact kuznets.a.g@gmail.com or zeden@gmail.com

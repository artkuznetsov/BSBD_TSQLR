from django.utils.safestring import mark_safe
from django.contrib.auth.models import *

from PIL import Image
from wsgiref.util import FileWrapper
from TestApp import settings
from .forms import *
from .models import models
from django.http import *
from django.shortcuts import *
from django.http import FileResponse
# from django.contrib.auth.models import User, Group
import random, json
from django.contrib.auth.decorators import login_required
import re
import pyodbc
from datetime import *
from pytz import timezone
import eralchemy
from eralchemy import render_er
import base64
import hashlib
from django.db.models import Q
import psycopg2


def CreateShema (database_type_Name, connectStr):
      print('popal')      
      if database_type_Name != 'PostgreSQL':
            host = re.search(r'\w*SERVER=\w*', connectStr).group(0)[7:]
            user = re.search(r'\w*UID=\w*', connectStr).group(0)[4:]
            password = re.search(r'\w*PWD=\w*', connectStr).group(0)[4:]
            database = re.search(r'\w*DATABASE=\w*', connectStr).group(0)[9:]
            render_er('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + database + '','' + host + '->' + database + '.png')
            response = base64.b64encode(open(host + '->' + database + '.png',"rb").read())
            return response
      else:
            #lines = [line.rstrip('\n') for line in open('/etc/odbc.ini')]
            #dsn_name = re.search(r'\w*DSN=\w*', connectStr).group(0)[4:]
            #print('DSN_NAME IS ' + dsn_name)
            Connect = psycopg2.connect(connectStr)
            
            host = re.search(r'\w*host=\w*',connectStr).group(0)[5:]
            
            user = re.search(r'\w*user=\w*',connectStr).group(0)[5:]
            
            database = re.search(r'\w*dbname=\w*',connectStr).group(0)[7:]
            
            password = re.search(r'\w*password=\w*',connectStr).group(0)[9:]
           
            render_er('postgresql+psycopg2://' + str(user) + ':' + str(password) + '@' + str(host) + '/' + str(database) + '','' + str(host) + '->' + str(database) + '.png')    
            response = base64.b64encode(open(host + '->' + database + '.png', "rb").read())
            return response
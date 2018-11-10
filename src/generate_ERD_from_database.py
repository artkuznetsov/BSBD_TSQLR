import eralchemy
from eralchemy import render_er
import sqlalchemy
from sqlalchemy import create_engine

host = 'localhost'
user = 'root'
password = 'P@$$word'
database = 'testbsbd'

render_er('mysql+pymysql://'+user+':'+password+'@'+host+'/'+database+'',''+host+'\\'+database+'.jpg')


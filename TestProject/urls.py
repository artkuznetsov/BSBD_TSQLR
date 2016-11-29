from django.conf.urls import url, include

import TestApp
import TestProject
from . import views

urlpatterns = [
  url(r'^$', TestProject.views.home),
  #url(r'^users/(?P<LoginUser>[^/]+)/profile$', views.TestsUser, name='TestUser'),
  url(r'^tests/$', views.AddUsers, name='AddUsers'),
  url(r'create_test/$', views.CreateTest, name = 'create_test'),
  url(r'^generate_users/$', views.AddUsers,name='AddUsers'),
  url(r'404/$', TestProject.views.error404),
  url(r'add_subscribe/$', views.Add_TestPerson, name='Add_TestPerson'),
  url(r'testid=(?P<testid>[0-9]+)/$', views.GoTest, name='GoTest')
]
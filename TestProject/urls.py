from django.conf.urls import url, include

import TestApp
import TestProject
from . import views

urlpatterns = [
  url(r'^$', TestProject.views.home),
  #url(r'^users/(?P<LoginUser>[^/]+)/profile$', views.TestsUser, name='TestUser'),
  url(r'^tests/$', views.AddUsers, name='AddUsers'),
  url(r'create_test/$', views.CreateTest, name = 'create_test'),
  url(r'^generate_users/$',views.AddUsers,name='AddUsers'),
]
from django.conf.urls import url, include

import TestApp
import TestProject
from . import views

urlpatterns = [
  url(r'^$', TestProject.views.tests),
  #url(r'^users/(?P<LoginUser>[^/]+)/profile$', views.TestsUser, name='TestUser'),
  # url(r'^tests/$', views.tests),
  url(r'^tinymce/', include('tinymce.urls')),
  url(r'create_test/$', views.CreateTest, name = 'create_test'),
  url(r'^generate_users/$', views.AddUsers,name='AddUsers'),
  url(r'404/$', TestProject.views.error404),
  url(r'add_subscribe/$', views.Add_TestPerson, name='Add_TestPerson'),
  url(r'testid=(?P<testid>[0-9]+)&var=(?P<var>[0-9]+)/$', views.some_test, name='SomeTest'),
  url(r'answer_user/$', views.TakeAnswer, name='TakeAnswer'),
  url(r'delete_subscribe/$', views.DeleteSubscribe, name='DeleteSubscribe'),
  url(r'trainer/$', views.Trainer, name='Trainer'),
  url(r'show_users/$', views.ShowUsers, name='ShowUsers'),
  url(r'some_test/$', views.some_test, name='SomeTest'),
  url(r'newid=(?P<newid>[0-9]+)/$', views.News, name='News')
]
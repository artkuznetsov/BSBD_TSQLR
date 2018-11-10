from django.conf.urls import url, include

from .views import MainPage

urlpatterns = [
  url(r'^$', MainPage.as_view()),
  
]
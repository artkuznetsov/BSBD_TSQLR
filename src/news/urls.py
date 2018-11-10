from django.conf.urls import url, include
from .views import NewDetailView

urlpatterns = [
    url(r'newid=(?P<slug>[0-9]+)/$', NewDetailView.as_view(), name='New-detail')
]
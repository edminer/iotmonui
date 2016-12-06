from django.conf.urls import url

from . import views

app_name = 'iotmonui'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^log$', views.log, name='log'),
]

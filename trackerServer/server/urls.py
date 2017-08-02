from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^insert_data/$', views.insertData, name='insertData'),
    url(r'^datafilter/$', views.dataFilter, name='dataFilter'),
    url(r'^folios/$', views.getFolioOfST, name='getFolioOfST'),
    url(r'^getSTFolios/$', views.getSTFolios, name='getSTFolios'),
    url(r'^datatable/$', views.dataTable, name='dataTable'),
]

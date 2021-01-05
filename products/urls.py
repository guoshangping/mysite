from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index/', views.ProdExportIndex),
    path('testindex/', views.ExportIndexTest),
    path('casetest/',views.ProdExportCase),
    url(r'^choose/location/$', views.choose_location),
    url(r'^choose/type/$', views.choose_prodtypes),
]
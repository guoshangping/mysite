from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('score_tools/', views.score_tools, name='score_tools'),
    path('test_zhibiao/', views.test_zhibiao, name='test_zhibiao'),
    path('test_show/', views.test_show, name='test_show'),
    path('test_clear/', views.test_clear, name='test_clear'),
    path('test_export/', views.test_export, name='test_export'),
    path('test_save/', views.test_save, name='test_save'),
    path('vend_rank/', views.vend_rank, name='vend_rank'),
    path('muban_download/', views.muban_download, name='muban_download'),
    url(r'report/word_down/(?P<id>\w+)', views.Export_Report, name='report_word'),
    url(r'report/zip_down/(?P<id>\w+)', views.report_downzip, name='report_zip'),

]

from django.urls import path
from . import views
app_name = 'app'
urlpatterns = [
    path('index/',views.index,name='index'),
    path('select_to_index2/',views.select_to_index2,name='select_to_index2'),
    path('input/',views.select_to_index2 ,name='input'),
    path('select/',views.select,name='select'),
    path('select2/',views.select2,name='select2'),
    path('pro_chaxun_bycretime/',views.pro_chaxun_bycretime,name='pro_chaxun_bycretime'),
    path('pro_chaxun_bycretuser/',views.pro_chaxun_bycretuser,name='pro_chaxun_bycretuser'),
    path('pro_chaxun_byxmjd/',views.pro_chaxun_byxmjd,name='pro_chaxun_byxmjd'),
    path('pro_chaxun_bychargeperson/',views.pro_chaxun_bychargeperson,name='pro_chaxun_bychargeperson'),
    path('pro_chaxun_byparticipant/',views.pro_chaxun_byparticipant,name='pro_chaxun_byparticipant'),
    path('pro_chaxun_byproname/',views.pro_chaxun_byproname,name='pro_chaxun_byproname'),
    path('pro_chaxun_mohu/',views.pro_chaxun_mohu,name='pro_chaxun_mohu'),
    path('pro_check/',views.pro_check,name='pro_check'),
    path('pros/',views.pro,name='pros'),
    path('create_pro_page/',views.create_pro_page,name='create_pro_page'),
    path('create_pro/',views.create_pro,name='create_pro'),
    path('configpro/',views.configpro,name='configpro'),
    path('superconfigpro/',views.superconfigpro,name='superconfigpro'),
    path('superudate/',views.superudate,name='superudate'),
    path('updateproname/',views.updateproname,name='updateproname'),
    path('updateprotime/',views.updateprotime,name='updateprotime'),
    path('updatechar/',views.updatechar,name='updatechar'),
    path('updatepar/',views.updatepar,name='updatepar'),
    path('delpro/',views.delpro,name='delpro'),
    path('delete_all/',views.delete_all,name='delete_all'),
    path('save_config/',views.save_config,name='save_config'),
    path('query_pro/',views.query_pro,name='query_pro'),
    path('query_all_users/',views.query_all_users,name='query_all_users'),
    path('update_pro_page/',views.update_pro_page,name='update_pro_page'),
    path('update_pro/',views.update_pro,name='update_pro'),
    path('query_protime/',views.query_protime,name='query_protime'),
    path('query_protime_yue/',views.query_protime_yue,name='query_protime_yue'),
    path('query_properson/',views.query_properson,name='query_properson'),
    path('query_proxmjd/',views.query_proxmjd,name='query_proxmjd'),
    path('query_charperson/',views.query_charperson,name='query_charperson'),
    path('query_participant/',views.query_participant,name='query_participant'),
    path('query_proname/',views.query_proname,name='query_proname'),
    path('pro_page/',views.pro_page,name='pro_page'),
    path('lianhe_query/',views.lianhe_query,name='lianhe_query'),
]
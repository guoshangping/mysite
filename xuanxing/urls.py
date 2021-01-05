from django.urls import path
from django.conf.urls import url
from . import task_manage_views
from . import user_views
from . import project_views
from . import test_views
from . import options_views
from . import product_views
from . import role_views
from . import log_views
from . import document
from . import document_check
from . import score_views
from . import all_test

from tools import tools

urlpatterns = [
    # 项目相关
    path('login/', task_manage_views.login, name="login"),
    path('logout/', task_manage_views.logout, name="logout"),
    path('homepage/', task_manage_views.homepage, name="homepage"),
    path('task_manage/', task_manage_views.task_manage, name="task_manage"),
    path('product_manage/', task_manage_views.product_manage, name="product_manage"),

    # 用户相关
    path('user_manage/', user_views.user_manage, name="user_manage"),
    path('user_upload/', user_views.user_upload, name="user_upload"),
    path('user_add/', user_views.user_add, name="user_add"),
    path('user_del/', user_views.user_del, name="user_del"),
    path('user_edit/', user_views.user_edit, name="user_edit"),
    path('user_status_change/', user_views.user_status_change, name="user_status_change"),

    # 测试案例相关
    path('test_anli_list/', test_views.test_anli_list, name="test_anli_list"),
    path('test_anli/', test_views.test_anli, name="test_anli"),
    path('test_fangan/', test_views.test_fangan, name="test_fangan"),
    path('test_report/', test_views.test_report, name="test_report"),
    path('anli_view/', test_views.anli_view, name="anli_view"),
    path('anli_del/', test_views.anli_del, name="anli_del"),
    path('daochu_anli_word/', test_views.daochu_anli_word, name="daochu_anli_word"),
    path('anli_map/', test_views.anli_map, name="anli_map"),
    path('anli_map_init/', test_views.anli_map_init, name="anli_map_init"),
    path('anli_map_query/', test_views.anli_map_query, name="anli_map_query"),
    path('anli_map_opt/', test_views.anli_map_opt, name="anli_map_opt"),

    # 产品相关
    path('up_prod_content/', product_views.up_prod_content, name="up_prod_content"),
    path('prod_show/', product_views.prod_show, name="prod_show"),
    path('prod_info/', product_views.prod_info, name="prod_info"),
    path('prod_list/', product_views.prod_list, name="prod_list"),
    path('prod_list_db/', product_views.prod_list_db, name="prod_list_db"),
    path('prod_type_modify/', product_views.prod_type_modify, name="prod_type_modify"),
    path('prod_add/', product_views.prod_add, name="prod_add"),
    path('prod_save/', product_views.prod_save, name="prod_save"),
    path('prod_type_add/', product_views.prod_type_add, name="prod_type_add"),
    path('prod_export/', product_views.prod_export, name="prod_export"),
    path('prod_change/', product_views.prod_change, name="prod_change"),
    path('vend_prod_add_html/', product_views.vend_prod_add_html, name="vend_prod_add_html"),
    path('prod_type_change/', product_views.prod_type_change, name="prod_type_change"),
    path('prod_del/', product_views.prod_del, name="prod_del"),
    path('product_a_list/', product_views.product_a_list, name="product_a_list"),

    # 指标相关
    path('index_list/', product_views.index_list, name="index_list"),
    path('index_a_list/', product_views.index_a_list, name="index_a_list"),
    path('up_index_content/', product_views.up_index_content, name="up_index_content"),
    path('index_show/', product_views.index_show_db, name="index_show"),
    path('index_info/', product_views.index_info, name="index_info"),
    path('index_detail/', product_views.index_detail, name="index_detail"),
    path('index_save/', product_views.index_save, name="index_save"),
    path('index_type_modify/', product_views.index_type_modify, name="index_type_modify"),
    path('index_save_db/', product_views.index_save_db, name="index_save_db"),
    path('index_add/', product_views.index_add, name="index_add"),
    path('index_export/', product_views.index_export, name="index_export"),
    path('index_query/', product_views.index_query, name="index_query"),
    path('index_del/', product_views.index_del, name="index_del"),

    # 项目相关
    path('project_tongji/', test_views.project_tongji, name="project_tongji"),
    path('index_tongji/', test_views.index_tongji, name="index_tongji"),
    path('anli_upload/', test_views.anli_upload, name="anli_upload"),
    path('show_doc_data/', test_views.show_doc_data, name="show_doc_data"),
    path('project_dongtai/', project_views.project_dongtai, name="project_dongtai"),
    path('project_export/', project_views.project_export, name="project_export"),
    path('project_daily/', project_views.project_daily, name="project_daily"),
    path('project_daily_upload/', project_views.project_daily_upload, name="project_daily_upload"),
    path('project_daily_edit/', project_views.project_daily_edit, name="project_daily_edit"),
    path('project_daily_del/', project_views.project_daily_del, name="project_daily_del"),

    # 权限相关
    path('option_list/', user_views.option_list, name="option_list"),
    path('op_add/', options_views.op_add, name="op_add"),
    path('op_type_add/', options_views.op_type_add, name="op_type_add"),
    path('role_op_add/', options_views.role_op_add, name="role_op_add"),  # 角色权限添加
    path('role_op_query/', options_views.role_op_query, name="role_op_query"),
    path('optype_edit/', options_views.optype_edit, name="optype_edit"),
    path('op_del/', options_views.op_del, name="op_del"),
    path('op_add_html/', options_views.op_add_html, name="op_add_html"),
    path('op_edit_html/', options_views.op_edit_html, name="op_edit_html"),
    path('op_query/', options_views.op_query, name="op_query"),
    path('op_edit/', options_views.op_edit, name="op_edit"),

    # 角色相关
    path('admin_role/', role_views.admin_role, name="admin_role"),
    path('role_del/', role_views.role_del, name="role_del"),
    path('role_edit/', role_views.role_edit, name="role_edit"),
    path('role_add_html/', role_views.role_add_html, name="role_add_html"),
    path('role_set/', role_views.role_set, name="role_set"),
    path('role_query/', role_views.role_query, name="role_query"),
    path('role_cancel/', role_views.role_cancel, name="role_cancel"),
    path('user_role_change/', role_views.user_role_change, name="user_role_change"),

    # 项目相关
    path('project_add_html/', task_manage_views.project_add_html, name="project_add"),
    path('project_del/', task_manage_views.project_del, name="project_del"),
    path('pro_delete_all/', task_manage_views.pro_delete_all, name="pro_delete_all"),
    path('pro_edit/', task_manage_views.pro_edit, name="pro_edit"),
    path('sp_time/', task_manage_views.sp_time, name="sp_time"),
    path('prod_type_query/', task_manage_views.prod_type_query, name="prod_type_query"),

    # 日志相关
    path('log/', log_views.log, name="log"),

    # 个人信息
    path('my_info/', task_manage_views.my_info, name='my_info'),
    path('my_info_edit/', task_manage_views.my_info_edit, name='my_info_edit'),
    path('project_dongtai/', project_views.project_dongtai, name='project_dongtai'),
    path('dt_search/', project_views.dt_search, name='dt_search'),

    # 文档相关
    path('document/', document.document, name='document'),
    path('document_check/', document_check.document_check, name='document_check'),
    path('doc_log/', document.doc_log, name='doc_log'),
    path('doc_add/', document.doc_add, name='doc_add'),
    # path('get_doc_add/',document.get_doc_add,name='get_doc_add'),
    path('upload_file/', document.upload_file, name='upload_file'),
    path('download_file/', document.download_file, name='download_file'),
    path('down_load/', document.down_load, name='down_load'),
    path('get_ven/', document.get_ven, name='get_ven'),
    path('get_ven_c/', document_check.get_ven_c, name='get_ven_c'),
    path('get_ven_other/', document.get_ven_other, name='get_ven_other_c'),
    path('get_ven_other_c/', document_check.get_ven_other_c, name='get_ven_other_c'),
    path('get_pub/', document.get_pub, name='get_pub'),
    path('change_name/', document.change_name, name='change_name'),
    path('stat_change/', document.stat_change, name='stat_change'),

    path('add_mark/', document.add_mark, name='add_mark'),
    path('check_add_mark/', document_check.check_add_mark, name='check_add_mark'),
    path('jy_add_mark/', document_check.jy_add_mark, name='jy_add_mark'),

    path('check_pass/', document.check_pass, name='check_pass'),
    path('no_check_pass/', document.no_check_pass, name='no_check_pass'),

    # path('score/', score.score, name='score'),

    path('download_file_jy/', document.download_file_jy, name='download_file_jy'),  # 纪要
    path('down_load_jy/', document.down_load_jy, name='down_load_jy'), #纪要

    path('shape_show/', document.shape_show, name='shape_show'),

    # 考核打分
    path('item_input/', score_views.items_input, name='items_input'),
    path('huping/', score_views.huping, name='huping'),
    path('lingdao/', score_views.lingdao, name='lingdao'),
    path('item_submit/', score_views.item_submit, name='submit'),  # 事项提交
    path('item_check/', score_views.item_check, name='item_check'),  # 事项审核
    path('shenhe_change/', score_views.shenhe_change, name='shenhe_change'),  # 事项审核
    path('huping_submit/', score_views.huping_submit, name='huping_submit'),  # 事项审核
    path('lingdao_submit/', score_views.lingdao_submit, name='lingdao_submit'),  # 事项审核
    path('save_final/', score_views.save_final, name='save_final'),  # 事项审核
    path('clear_final/', score_views.clear_final, name='clear_final'),  # 事项审核
    path('shenhe_list/', score_views.shenhe_list, name='shenhe_list'),  # 个人查看页面
    path('kaohe_jili/', score_views.kaohe_jili, name='kaohe_jili'),  # 激励与档次

    # test
    # path('test_pdf/', all_test.get_files, name='get_files'),
    path('score_excel/', score_views.score_excel, name='score_excel'),

]

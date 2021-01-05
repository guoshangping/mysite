# from django.contrib import admin
# # from testm.admin import ExportExcelMixin
# from products.models import *
# from django.contrib.admin import ListFilter
# from django.core.exceptions import ImproperlyConfigured
# from django.utils.translation import gettext as _
#
# # Register your models here
#
# class ProductAdmin(admin.ModelAdmin,ExportExcelMixin):
#     list_max_show_all = 20
#     list_per_page = 20
#     list_display = ['id', 'prod_class','prod_name', 'vend_name']
#     # 搜索字段
#     #search_fields = ['vend_name', 'prod_name','prod_relation_id__location_type_name','prod_relation_id__prod_type_name','prod_relation_id__prod_subclass']
#     actions = ["export_as_excel"]
#     list_display_links = ('id', 'prod_name','vend_name',)
#     #list_filter = (VendProdNameListFilter,'prod_relation_id__location_type_name','prod_relation_id__prod_type_name', 'prod_relation_id__prod_subclass',)
#     #list_filter = (VendProdNameListFilter,'prod_class','prod_class__location_type')
#     #list_filter = (VendProdNameListFilter, 'prod_class')
#     list_filter = (VendProdNameListFilter, 'prod_class__location_type','prod_class__prod_type',
#                    'prod_class__prod_subclass','prod_class__performance_classification')
# # Register your models here.
# admin.site.register([ProductsLocation,Statistics])
# class ProductsClassAdmin(admin.ModelAdmin,ExportExcelMixin):
#     list_max_show_all = 20
#     list_per_page = 20
#     search_fields = ['location_type__location_type_name','prod_type__prod_type_name','prod_subclass',
#                      'performance_classification','main_specifications','vend_strategy','deployment_scope'
#                      , 'application_scenario']
#     list_display = ['id','location_type', 'prod_type', 'prod_subclass', 'performance_classification']
#     list_filter = ('location_type','prod_type','prod_subclass','performance_classification')
#     change_form_template = 'admin/prodclass.html'
#
# class ProductsTypesAdmin(admin.ModelAdmin,ExportExcelMixin):
#     list_max_show_all = 20
#     list_per_page = 20
#     fields = ('location_type','prod_type_name',)
#     list_display = ['id', 'location_type','prod_type_name']
#     #search_fields = ['location_type','prod_type_name']
#     list_filter = ('location_type','prod_type_name',)
#     list_display_links = ['id', 'location_type','prod_type_name']
#     actions = ['delete_selected']
#     '''
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(for_group_id=2)
#
#
#
#     def delete_selected(self, request, obj):
#         for o in obj.all():
#             # 这里除了删除选择的对象之外，我还更新了其它对象
#             #Article.objects.filter(id=o.id).update(is_ad=1)
#             if not request.user.is_superuser:
#                 if 'for_group' in dir(o):
#                     o.for_group_id = 1
#                     o.save()
#             else:
#                 o.delete()
#
#     delete_selected.short_description = '删除所选选项'
#     '''
#
#
#
# admin.site.register(ProductsTypes,ProductsTypesAdmin)
# admin.site.register(ProductsClass,ProductsClassAdmin)
# admin.site.register(Products, ProductAdmin)
# admin.site.site_header = '后台管理系统'
# admin.site.index_title = '选型产品管理'
#
#

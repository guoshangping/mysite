# from django.contrib import admin
# from testm.models import *
#
# from django.http import HttpResponse
# from openpyxl import Workbook
# #from products.models import VendProdNameListFilter
# from django import forms
# from import_export import resources
# from import_export.formats import base_formats
# #from import_export.admin import ImportExportModelAdmin
# from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
# import tablib
# import collections
# from docxtpl import DocxTemplate
# import re
# from django.utils.safestring import mark_safe
#
# from django.shortcuts import get_object_or_404
#
# from django.urls import reverse
#
# from django.http import HttpResponseRedirect
#
# import json
# from django.contrib.auth.models import User
#
#
# class ExportExcelMixin(object):
# 	def export_as_excel(self,request, queryset):
# 		meta = self.model._meta
# 		field_names = [field.name for field in meta.fields]
# 		response = HttpResponse(content_type='application/msexcel')
# 		response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
# 		wb = Workbook()
# 		ws = wb.active
# 		ws.append(field_names)
# 		for obj in queryset:
# 			data = [f'{getattr(obj, field)}' for field in field_names]
# 			ws.append(data)
# 		wb.save(response)
# 		return response
# 	export_as_excel.short_description = '导出Excel'
#
# class CaseResource(resources.ModelResource):
#
# 	def __init__(self):
# 		super(CaseResource, self).__init__()
#
# 		field_list = TestCase._meta.fields
# 		self.vname_dict = {}
# 		self.fkey = []
# 		for i in field_list:
# 			self.vname_dict[i.name] = i.verbose_name
#
# 			if (isinstance(i, models.ForeignKey)):
# 				self.fkey.append(i.verbose_name)  # 获取所有ForeignKey字段的name存放在列表
# 		#print(self.vname_dict)
#
#
# 	def get_export_fields(self):
# 		fields = self.get_fields()
# 		for i, field in enumerate(fields):
# 			field_name = self.get_field_name(field)
# 			if field_name in self.vname_dict.keys():
# 				# print(self.vname_dict[field_name])
# 				field.column_name = self.vname_dict[field_name]
# 		return fields
#
# 	def export(self, queryset=None, *args, **kwargs):
# 		self.before_export(queryset, *args, **kwargs)
#
# 		if queryset is None:
# 			queryset = self.get_queryset()
#
# 		headers = self.get_export_headers()
# 		data = tablib.Dataset(headers=headers)
# 		#print(data)
# 		# 获取所有外键名称在headers中的位置
# 		fk_index = {}
# 		for fk in self.fkey:
# 			fk_index[fk] = headers.index(fk)
# 		iterable = queryset
# 		for obj in iterable:
# 			# 获取将要导出的源数据，这里export_resource返回的是列表，便于更改。替换到外键的值
# 			res = self.export_resource(obj)
# 			if res[fk_index['案例(三级指标)名称']] != '':
# 				res[fk_index['案例(三级指标)名称']] = Index.objects.get(id=res[fk_index['案例(三级指标)名称']]).index_name
# 			if res[fk_index['测试项目名称']] != '':
# 				res[fk_index['测试项目名称']] = Projects.objects.get(id=res[fk_index['测试项目名称']]).project_name
# 			data.append(res)
# 		self.after_export(queryset, data, *args, **kwargs)
# 		return data
#
# 	def before_import(self, dataset, using_transactions, dry_run, **kwargs):
# 		dict = []
# 		#print(dataset)
# 		for row in dataset.dict:
# 			tmp = collections.OrderedDict()
# 			#cases = TestCase.objects.all()
# 			for item in row:
# 				if item == '案例(三级指标)名称':
# 					"""
# 					这里是关键，通过可读名称到User表中找到对应id，并加到导入的数据中去
# 					"""
# 					print(row[item])
# 					if row[item] in ['', None]:
# 						tmp[item] = ''
# 					else:
# 						tmp[item] = Index.objects.get(index_name=row[item]).id
# 				elif item == '测试项目名称':
# 					if row[item] in ['', None]:
# 						tmp[item] = ''
# 					else:
# 						tmp[item] = Projects.objects.get(project_name=row[item]).id
# 				else:
# 					tmp[item] = row[item]
# 			"""
# 			这里是关键，将数据进行比对，如果数据相同，就把原先在Book表中的id加到需要导入的数据中去，
# 			这样就不会新增和原先一模一样的数据，类似于create_or_update方法
# 						for case in cases:
# 				if row['name'] == case.case_name:
# 					tmp['id'] = case.id
# 			"""
#
# 			dict.append(tmp)
# 		dataset.dict = dict
# 		#print(dataset)
# 		return dataset
#
# 	class Meta:
# 		#fields = ("id","case_name", "test_date","test_location","prod_name","vend_name","test_purpose","test_design","test_conditions","test_procedure","expected_results","test_result","sign","remark",)
# 		#export_order = ("id","case_name", "test_date","test_location","prod_name","vend_name","test_purpose","test_design","test_conditions","test_procedure","expected_results","test_result","sign","remark",)
# 		model = TestCase
#
#
# # 模块
# class TestCaseAdmin(ImportExportModelAdmin,ImportExportActionModelAdmin):
# 	list_max_show_all = 10
# 	list_per_page = 10
# 	list_display = ["id",'case_name','test_purpose','project_name']
# 	search_fields = ('case_name__index_name','project_name__project_name')
# 	list_display_links = ('id','case_name','test_purpose','project_name',)
# 	list_filter = ('project_name__project_name',)
# 	#ordering = ('-id',)
# 	readonly_fields = ('prod_name', 'vend_name','test_date', 'sign', 'test_result')
# 	#actions = ["export_as_excel"]
# 	#export_as_excel.short_description = '导出Excel'
# 	resource_class = CaseResource
#
# 	def get_export_formats(self):  # 该方法是限制格式
# 		formats = (
# 			base_formats.XLS,
# 			base_formats.XLSX,
# 		)
# 		return [f for f in formats if f().can_export()]
#
# 	def get_import_formats(self):  # 该方法是限制格式
# 		formats = (
# 			base_formats.XLS,
# 			base_formats.XLSX,
# 		)
# 		return [f for f in formats if f().can_import()]
#
#
# admin.site.register(TestCase,TestCaseAdmin)
#
# '''
# class ProjectsForm(forms.ModelForm):
# 	checkbox = forms.ModelMultipleChoiceField(label=u'参与人',queryset=User.objects.all(),widget=forms.CheckboxSelectMultiple())
#
# 	class Meta:
# 		model = Projects
# 		fields = "__all__"
#
#
# class ProjectsAdmin(admin.ModelAdmin):
# 	form = ProjectsForm
# '''
# # class ProjectsAdmin(admin.ModelAdmin):
# #
# # 	list_max_show_all = 20
# # 	list_per_page = 20
# # 	#fieldsets = ( ['主要信息', {   'classes': ('collapse', 'wide', 'extrapretty'),'fields':('project_name','project_speed','create_user',), }],)
# # 	search_fields = ('project_name',)
# # 	list_display = ["id",'project_name','项目进度','create_user','负责人','参与人']
# # 	list_display_links = ("id",'project_name','项目进度','create_user','负责人','参与人',)
# # 	list_filter = ['project_speed','create_user','deal_user','members','vend_prod']
# # 	filter_horizontal = ('deal_user', 'members', 'vend_prod')
# # 	#raw_id_fields = ('create_user',)
# # 	radio_fields = {"project_speed": admin.HORIZONTAL}
# # 	exclude = ('create_user',)
# # 	'''	def queryset(self, request):
# # 		print('test')
# #
# # 		if request.user.is_superuser:
# # 			return Projects.objects.all()
# # 		return Projects.objects.filter(create_user=request.user)'''
# #
# #
# # 	def save_model(self, request, obj, form, change):
# # 		obj.create_user = request.user
# # 		obj.save()
# # 		#super().save_model(request, obj, form, change)
# #
# # 	def 负责人(self,obj):
# # 		return [bt.username for bt in obj.deal_user.all()]
# # 	def 参与人(self,obj):
# # 		return [bt.username for bt in obj.members.all()]
#
# 	#filter_horizontal = ('deal_user',)
# # admin.site.register(Projects,ProjectsAdmin)
#
# '''
# class ReportsAdmin(admin.ModelAdmin):
#
# 	list_max_show_all = 20
# 	list_per_page = 20
# 	filter_horizontal = ('prod_vend','group_part','test_conclusion','test_time',)
# 	#filter_horizontal = ('prod_vend', 'group_part', 'test_conclusion',)
# 	fieldsets = (
# 		(None, {'fields': ['report_name']}),
# 		['需求概述', {'fields': ('test_background', 'test_object', 'test_demand',)}],
# 		['测试方法', {'fields': ('pass_index', 'evaluate_index', 'test_case',)}],
# 		['选型组织', {'fields': ('organization_framework','group_part',)}],
# 		['候选选型产品供应商', {'fields': ['prod_vend']}],
# 		['测试计划', {'fields': ['test_time','test_location', 'test_flow']}],
# 		['测试环境', {'fields': ['test_environment']}],
# 		['测试情况', {'fields': ['test_records', 'test_results']}],
# 		['测试结论', {'fields': ['test_conclusion']}]
# 	)
#
# 	change_form_template = 'admin/test_report.html'
# '''
#
# class ReportsAdmin(admin.ModelAdmin):
# 	search_fields = ('report_name','project_name__project_name',)
#
# 	list_max_show_all = 20
# 	list_per_page = 20
# 	filter_horizontal = ['test_conclusion','prod_vend']
# 	#list_filter = ['project_name']
# 	# 自定义一个字段
#
# 	def save_model(self, request, obj, form, change):
#
# 		#if form.cleaned_data['organization_framework'].split
# 		#obj.organization_framework = 'aaa'
# 		obj.organization_framework = form.data['organization_framework']
# 		obj.test_flow = form.data['test_flow']
# 		super().save_model(request, obj, form, change)
# 	def down_paper(self, obj):
# 		"""自定义一个a标签，跳转到实现下载功能的url"""
# 		dest = '{}export/'.format(obj.pk)
# 		title = '下载'
# 		return mark_safe('<a href="{}">{}</a>'.format(dest, title))
#
# 	down_paper.short_description = 'zip/word 下载'
# 	down_paper.allow_tags = True
#
# 	def get_urls(self):
# 		"""添加一个url，指向实现下载功能的函数make_docx"""
# 		from django.conf.urls import url
# 		urls = [
# 			url('^(?P<pk>\d+)export/?$',
# 				self.admin_site.admin_view(self.make_docx),
# 				name='export_data'),
# 		]
# 		#print(urls)
# 		#print(self.get_urls())
# 		return urls + super(ReportsAdmin, self).get_urls()
#
# 	def make_docx(self, request,  *args, **kwargs,):
# 		# 重定向
# 		new_path = reverse('report_zip', args=(kwargs['pk'],))
# 		#print(new_path)
# 		return HttpResponseRedirect(new_path)
#
# 	'''
# 	def make_docx(self, request, *args, **kwargs):
#
#
# 		file_path = "D:\\GIT-Project\\TestPM\\mysite\\media\\output\\"
# 		# file_path = '/webserver/hys_cmdb/static/download/'
# 		obj = get_object_or_404(Reports, pk=kwargs['pk'])
# 		#list_nums = re.findall("\d+", obj.id)  # 获取字符串中的所有数字
# 		list_nums = [obj.id]
# 		print(list_nums)
#
# 		#nums = ''.join(list_nums)
# 		nums = list_nums[0]
# 		print(nums)
# 		doc = DocxTemplate("{}export.docx".format(file_path))
# 		print(doc)
# 		context = {}
# 		doc.render(context)
# 		doc.save("{}{}.docx".format(file_path, nums))
# 		new_path = reverse('download', args=(nums,))
# 		print(new_path)
# 		return HttpResponseRedirect(new_path)
# 	'''
# 	def flow(self,obj):
# 		test_flows = obj.test_flow
# 		#print(test_flows)
# 		html = "<a href = '#'> 测试流程 </a>"
# 		#html = "<p>" + str(test_flows) + "</p>"
#
# 		return mark_safe(html)  # 取消转义
#
# 	# 允许HTML标签
# 	flow.allow_tags = True
# 	# HTML展示时的字段名
# 	flow.short_description = '流程'
#
#
# 	list_display = ["id", 'report_name', 'project_name', 'test_background', 'test_object','down_paper',]
# 	list_display_links = ("id", 'report_name', 'project_name','test_background', 'test_object')
# 	#radio_fields = {"project_name": admin.HORIZONTAL}
# 	fields_plan = ('test_time', 'test_location', 'test_flow')
# 	list_filter = ('project_name',)
# 	fieldsets = (
# 		(None, {'fields': ['project_name']}),
# 		(None, {'fields': ['report_name']}),
# 		['需求概述', {'fields': ('test_background', 'test_object', 'test_demand',)}],
# 		['测试方法', {'fields': ('pass_index', 'evaluate_index', 'test_case',)}],
# 		['选型组织', {'fields': ('organization_framework', 'group_part',)}],
# 		['候选选型产品供应商', {'fields': ['prod_vend'],'classes': ('collapse', 'wide', 'extrapretty'),}],
# 		['测试计划', {'fields': fields_plan}],
# 		['测试环境', {'fields': ['test_environment']}],
# 		['测试情况', {'fields': ['test_records', 'test_results']}],
# 		['测试结论', {'fields': ['test_conclusion']}]
# 	)
#
# 	change_form_template = 'admin/test_report.html'
#
#
#
# admin.site.register(Reports,ReportsAdmin)
# class Reports_groupsAdmin(admin.ModelAdmin):
#
# 	list_max_show_all = 20
# 	list_per_page = 20
# 	list_display = ['name','department','contacts','group_flag']
#
#
# admin.site.register(Reports_groups,Reports_groupsAdmin)
# admin.site.register(Conclusion)
# admin.site.register(Executes)
# admin.site.register(Score)
#
#
#
#
#
#
#

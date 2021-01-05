from django.shortcuts import render
from .models import *
from norm.models import *
from case.models import TestCase
from django.http import HttpResponse
from openpyxl import Workbook
import re
from io import BytesIO,StringIO

import simplejson
from case.admin import ExportExcelMixin

# Create your views here.
def ProductsIndex(params):
	records_list = []
	#print(params)
	if (type(params).__name__=='dict'):
		if params['vend_name'] is None and params['prod_name'] is None :
			list1 = Products.objects.all()
		elif params['vend_name'] == '' and params['prod_name'] != '' :
			list1 = Products.objects.filter(prod_name=params['prod_name'])
		elif params['vend_name'] != '' and params['prod_name'] == '' :
			list1 = Products.objects.filter(vend_name=params['vend_name'])
		elif params['vend_name'] != '' and params['prod_name'] != '':
			list1 = Products.objects.filter(vend_name=params['vend_name'], prod_name=params['prod_name'])
	elif (type(params).__name__)=='list':
		list1 = Products.objects.all()
	i = 0
	sum = 0
	for var in list1:
		#print(var.prod_relation_id_id)
		list2=ProductsRelation.objects.filter(id=var.prod_relation_id_id)
		#print(list2)
		for var1 in list2:
			list3 = IndexRelation.objects.filter(prod_class_id_id=var1.prod_class_id_id)
			for var2 in list3:
				list4 = Index.objects.filter(index_relation_id_id=var2.id)
				for var3 in list4:
					record_dic = dict()
					i = i + 1
					record_dic['id'] = i
					record_dic['prod_name'] = var.prod_name
					record_dic['vend_name'] = var.vend_name
					record_dic['test_type_name'] = str(var2.test_type_id)
					record_dic['location_type_name'] = var1.location_type_name
					record_dic['prod_type_name'] = var1.prod_type_name
					record_dic['prod_subclass'] = var1.prod_subclass
					record_dic['first_index'] = var2.first_index
					record_dic['two_index'] = var2.two_index
					record_dic['index_explanation'] = var2.index_explanation
					record_dic['three_index'] = var3.index_name
					record_dic['index_description'] = var3.index_description
					record_dic['test_tools'] = var3.tool
					record_dic['test_steps'] = var3.test_steps
					record_dic['remarks'] = var3.remark

					records_list.append(record_dic)
	#print(record_dic)

	if (type(params).__name__) == 'list':
		#print(records_list)
		records_list1 = []
		for record in records_list:
			if str(record['id'])  in params:
				records_list1.append(record)
		records_list=records_list1
	#print(len(records_list),records_list)
	records_num = len(records_list)
	response1 = ({'total_num': records_num}, records_list)
	return response1
	# return render(request,'index.html',"<p>" + response + "</p>")


def ExportExcelORM(res):
	meta = "产品指标"
	field_names =['id', 'prod_name', 'vend_name', 'test_type_name', 'location_type_name', 'prod_type_name', 'prod_subclass', 'first_index', 'two_index', 'index_explanation', 'three_index', 'index_description', 'test_tools', 'test_steps', 'remarks']

	wb = Workbook()
	ws = wb.active
	ws.append(field_names)
	for i in range(0, len(res[1])):
		data = [res[1][i][field] for field in field_names]
		ws.append(data)
		#print(data)
	#print(response)
	response = HttpResponse(content_type='application/msexcel')
	response['Content-Disposition'] = 'attachment; filename=prodindex.xlsx'
	wb.save(response)
	'''	x_io = BytesIO()
	wb.save(x_io)
	x_io.seek(0)
	response = HttpResponse(x_io.getvalue(), content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=prodindex.xls'
	response.write(x_io.getvalue())'''


	'''	print(type(response))
	response.write(x_io.getvalue())
	print(response)'''
	#print(response['Content-Disposition'])
	return response



def ExportProdIndex(request):
	try:
		#print('grf')
		#print(request.method)
		if request.method == "POST":
			data = re.findall(r"\d+\.?\d*", request.body.decode())
			res = ProductsIndex(data)
			res1 = ExportExcelORM(res)
			return res1
	except Exception as e:
		print(e)

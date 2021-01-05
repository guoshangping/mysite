# -*- coding:utf-8 -*-
import openpyxl
import os
import json
from django.shortcuts import render
from testm.models import Projects
from django.contrib.auth.models import User
from products.models import ProductsClass, Products
from django.db import transaction
from django.http import JsonResponse
from openpyxl import Workbook
from xuanxing.models import ManageUser
from xuanxing.models import Options
from xuanxing.models import OptionsType
from xuanxing.models import Role


def op_add(request):
    op_name = request.POST.get("op_name", "")  # 权限名称
    optp_name = request.POST.get("optp_name", "")  # 权限类型名称
    if op_name and optp_name:
        op_obj = Options.objects.filter(option_name=op_name).first()
        if op_obj:
            return JsonResponse({"code": "0004"})  # 同名权限存在
        op_obj = Options()
        op_obj.option_name = op_name
        optp_obj = OptionsType.objects.filter(type_name=optp_name).first()
        if optp_obj:
            op_obj.option_type = optp_obj
        op_obj.save()
        return JsonResponse({"code": "0000"})


def op_type_add(request):
    recv_dic = request.POST.dict()
    op_type_name = recv_dic.get("op_type_name", "")
    op_type_obj = OptionsType()
    op_type_obj.type_name = op_type_name
    op_type_obj.save()
    return JsonResponse({"code": "0000"})


def role_op_add(request):
    recv_data = request.POST.dict()
    role_name = recv_data.get("role_name", "")  # 角色
    option_list = recv_data.get("option_list", "")  # 权限

    if role_name and option_list:
        option_list = json.loads(option_list)
        role_obj = Role.objects.filter(rolename=role_name).first()
        if not role_obj:
            return JsonResponse({"code": "0000"})
        else:
            role_obj.option.clear()  # 清除已有的权限
        # 权限入库
        for opt in option_list:
            opt_obj = Options.objects.filter(option_name=opt).first()
            if opt_obj:
                role_obj.option.add(opt_obj)
        # 保存，角色入库
        role_obj.save()
        return JsonResponse({"code": "0000"})
    else:
        return JsonResponse({"code": "0002"})


def role_op_query(request):
    recv_data = request.POST.dict()
    role_name = recv_data.get("role_name", "")  # 角色
    role_obj = Role.objects.filter(rolename=role_name).first()
    if role_obj:
        op_list = [op_obj.option_name for op_obj in role_obj.option.all()]
        return JsonResponse({"code": "0000", "op_list": op_list})
    else:
        return JsonResponse({"code": "0002"})


# 修改权限类型的名称
def optype_edit(request):
    recv_data = request.POST.dict()
    try:
        old_name = recv_data.get("old_name", "")
        new_name = recv_data.get("new_name", "")
        optype_obj = OptionsType.objects.filter(type_name=old_name).first()
        if optype_obj:
            optype_obj.type_name = new_name
            optype_obj.save()
            return JsonResponse({"code": "0000"})
        else:
            return JsonResponse({"code": "0004"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0003"})


# 删除权限
def op_del(request):
    recv_data = request.POST.dict()
    print(recv_data)
    try:
        opname = recv_data.get("opname", "")
        print("=============")
        print(opname)
        if opname:
            opname = json.loads(opname)
            print(type(opname))
            for op_name in opname:
                Options.objects.filter(option_name=op_name).delete()
            return JsonResponse({"code": "0000"})
        else:
            return JsonResponse({"code": "0002"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0003"})


# 增加权限的页面
def op_add_html(request):
    recv_data = request.GET.dict()
    resp_dic = {"optype": recv_data.get("optype", "")}
    return render(request, "xuanxing_html/option_add.html", resp_dic)


def op_edit_html(request):
    op_type_name = request.GET.get("op_type", "")
    print(op_type_name)
    resp_dic = dict()
    optype_obj = OptionsType.objects.filter(type_name=op_type_name).first()
    op_list = []
    if optype_obj:
        print("进来的")
        op_list = [op_obj.option_name for op_obj in Options.objects.filter(option_type=optype_obj)]
    resp_dic["op_list"] = op_list
    return render(request, "xuanxing_html/option_edit.html", resp_dic)


def op_query(request):
    resp_dic = dict()
    recv_data = request.POST.dict()
    op_type = recv_data.get("op_type", "")
    optype_obj = OptionsType.objects.filter(type_name=op_type)[0]
    op_list = [op_obj.option_name for op_obj in Options.objects.filter(option_type=optype_obj)]

    resp_dic["code"] = "0000"
    resp_dic["op_list"] = op_list
    return JsonResponse(resp_dic)


def op_edit(request):
    recv_data = request.POST.dict()
    old_name = recv_data.get("opt_name", "")
    new_name = recv_data.get("opt_name_new", "")
    opt_obj = Options.objects.filter(option_name=old_name).first()
    if opt_obj:
        opt_obj.option_name = new_name
        opt_obj.save()
        return JsonResponse({"code": "0000"})
    return JsonResponse({"code": "0002"})

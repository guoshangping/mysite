# -*- coding:utf-8 -*-
import openpyxl
import os
import json
import collections
from django.shortcuts import HttpResponse
from django.shortcuts import render
from testm.models import Projects
from tools.tools import format_string
from xuanxing.models import Options
from django.contrib.auth.models import User
from products.models import ProductsClass, Products
from django.db import transaction
from django.http import JsonResponse
from openpyxl import Workbook
from xuanxing.models import ManageUser
from xuanxing.models import Role
from xuanxing.models import OptionsType
from xuanxing.models import Role
from xuanxing.models import ManageUser
from hashlib import md5

# 角色主页面
def admin_role(request):
    all_role_list = [{"role_id": role_obj.id, "role_name": role_obj.rolename, "desc": role_obj.desc, } for role_obj in
                     Role.objects.all()]
    usr_list = [[usr_obj.username, usr_obj.id] for usr_obj in ManageUser.objects.all()]
    rolename_list = [role_obj.rolename for role_obj in Role.objects.all()]

    #用户拥有角色展示
    li = {user_obj.username:[u_role.id for u_role in user_obj.user_role.all()] for user_obj in ManageUser.objects.all()}
    role_dic={u_role.rolename:u_role.id for u_role in Role.objects.all()}
    user_role_dic ={"all_user":li,"all_role":role_dic}
    print(user_role_dic)
    # print(li)
    # print(role_dic)

    # {'all_user': {'管理员': [3, 4, 6], '李大釗': [3, 4, 6], '王刚1': [4], '王刚2': [5], '王刚3': [6], 'test': [4, 6], '张勇': [3],
    #               '王超': [3], '戴路': [3], '倪海波': [3, 5], '姜炜': [3, 5], '杨博': [3]},
    #  'all_role': {'超级管理员': 3, '测试经理': 4, 'reporter': 5, '测试操作员': 6, '考核员': 11, '文档审核员': 13}}

    return render(request, "xuanxing_html/admin-role.html", {"role_list": all_role_list,
                                                             "usr_list": usr_list,
                                                             "rolename_list":rolename_list,
                                                             "user_role_dic":user_role_dic
                                                             })


# 增加角色
def role_add_html(request):
    if request.method == "GET":
        return render(request, "xuanxing_html/roles_add.html")

    try:
        recv_data = request.POST.dict()
        role_name = recv_data.get("role_name", "")
        role_desc = recv_data.get("role_desc", "")
        role_obj = Role.objects.filter(rolename=role_name).first()
        if role_obj:
            return JsonResponse({"code": "0004"})
        role_obj = Role()
        role_obj.rolename = role_name
        role_obj.desc = role_desc
        role_obj.save()
        return JsonResponse({"code": "0000"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0002"})


# 删除角色
def role_del(request):
    recv_data = request.POST.dict()
    role_id = recv_data.get("role_id", "")
    try:
        if role_id:
            role_id = int(role_id)
            Role.objects.filter(id=role_id).delete()
            return JsonResponse({"code": "0000"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0002"})


def role_edit(request):
    resp_dic = dict()
    try:
        if request.method == "GET":
            recv_data = request.GET.dict()
        else:
            recv_data = request.POST.dict() # Post方式
        role_id = recv_data.get("role_id", "")
        if role_id:
            role_id = int(role_id)
            role_obj = Role.objects.filter(id=role_id).first()
            if request.method == "GET":
                resp_dic["role_msg"] = {"role_name": role_obj.rolename, "desc": role_obj.desc, "role_id": role_obj.id}
                return render(request, "xuanxing_html/roles_edit.html", resp_dic)
            else:
                role_name_new = format_string(recv_data.get("rolename", ""))
                if not role_name_new:
                    return JsonResponse({"code": "0006"})
                role_name_org = role_obj.rolename
                if role_name_org != role_name_new:
                    role_old = Role.objects.filter(rolename=role_name_new).first()
                    if role_old:
                        return JsonResponse({"code": "0004"})
                role_obj.rolename = role_name_new
                role_obj.desc = recv_data.get("desc", "")
                role_obj.save()
                return JsonResponse({"code": "0000"})
        else:
            if request.method == "GET":
                return HttpResponse("角色不存在")
            else:
                return JsonResponse({"code": "0007"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0002"})


def role_set(request):
    user_id = request.POST.get("user_id", "")
    role_name = request.POST.get("role_name", "")
    usr_obj = ManageUser.objects.filter(id=int(user_id)).first()
    if usr_obj:
        role_obj = Role.objects.filter(rolename=role_name).first()
        if role_obj:
            usr_obj.user_role.add(role_obj)
            usr_obj.save()
            return JsonResponse({"code": "0000"})
    return JsonResponse({"code": "0001"})


def role_query(request):
    user_id = request.POST.get("user_id", "")
    usr_obj = ManageUser.objects.filter(id=int(user_id)).first()
    if usr_obj:
        role_list = [u_role.rolename for u_role in usr_obj.user_role.all()]
        return JsonResponse({"code": "0000", "role_list": role_list})
    return JsonResponse({"code": "0001"})


def role_cancel(request):
    user_id = request.POST.get("user_id", "")
    role_name = request.POST.get("role_name", "")
    usr_obj = ManageUser.objects.filter(id=int(user_id)).first()
    if usr_obj:
        del_role = [u_role for u_role in usr_obj.user_role.all() if u_role.rolename == role_name]
        if del_role:
            usr_obj.user_role.remove(del_role[0])
            usr_obj.save()
            return JsonResponse({"code": "0000"})
    return JsonResponse({"code": "0001"})

def user_role_change(request):
    recv_data = request.POST.dict()
    user = recv_data.get("user", "")  # 用户
    print(user)
    role_list = recv_data.get("role", "")  # 角色
    print(role_list)

    if user and role_list:
        role_list = json.loads(role_list)
        user_obj = ManageUser.objects.filter(username=user).first()

        # 创建角色
        if not user_obj:
            return JsonResponse({"code": "0000"})
        else:
            user_obj.user_role.clear()  # 清除已有的角色

        for role in role_list:
            role_obj = Role.objects.filter(rolename=role).first()
            if role_obj:
                user_obj.user_role.add(role_obj)

        # 保存，角色入库
        user_obj.save()
        return JsonResponse({"code": "0000"})
    else:
        return JsonResponse({"code": "0002"})
# -*- coding:utf-8 -*-
import openpyxl
import os
import json
import collections

from django.shortcuts import render
from django.shortcuts import HttpResponse
from testm.models import Projects
from xuanxing.models import Options
from django.contrib.auth.models import User
from products.models import ProductsClass, Products
from django.db import transaction
from django.http import JsonResponse
from openpyxl import Workbook
from xuanxing.models import ManageUser
from xuanxing.models import Role
from xuanxing.models import OptionsType
from xuanxing.models import Log
from hashlib import md5
from tools.pm_utils_page import PagePaging
from tools.tools import format_string


def user_manage(request):
    if request.method == "GET":
        page_num_list = list(range(3, 12))
        return render(request, "xuanxing_html/user_list.html", {"page_num_list": page_num_list})
    else:
        recv_data = request.POST.dict()
        print(recv_data)
        user_name = recv_data.get("username", "")
        curr_page = int(recv_data.get("current_page", 1))
        if user_name:  # 搜索框里的值
            print("usernmae :%s" % user_name)
            all_user_list = [m_usr for m_usr in ManageUser.objects.all() if user_name in m_usr.username]
        else:
            all_user_list = ManageUser.objects.all()
        # 分页开始
        page_msg_num = int(request.POST.get("msg_num", 8))
        pp_obj = PagePaging(len(all_user_list), page_msg_num)
        totalpage_num = pp_obj.judge()  # 总页数
        page_obj = pp_obj.re_page(curr_page)  # 返回当前页的分页对象 包含start 和 end
        page_jizhun = 1 if curr_page == 1 else (curr_page -1) * page_msg_num + 1

        data = [{"uid": usr.id, "username": usr.username, "user_mobile": usr.user_mobile, "user_email": usr.user_email,
                      "user_workid": usr.user_workid,
                      "user_role": usr.user_role.all()[0].rolename if usr.user_role.all() else "", "rz_time": usr.rz_time,
                      "user_status": str(usr.user_status)} for usr in all_user_list[page_obj.start:page_obj.end]]
        return JsonResponse({"code": "0000", "data": data, "total_page": totalpage_num, "curr_page": curr_page, "page_jizhun": page_jizhun, "url": "user_manage"})


def option_list(request):
    resp_dic = dict()
    op_type_lsit = OptionsType.objects.all()
    optp_list = [optype.type_name for optype in op_type_lsit]  # 所有权限类型的名称
    resp_dic["optype_list"] = optp_list

    opt_dic = collections.OrderedDict()
    for optp in optp_list:
        optype_obj = OptionsType.objects.filter(type_name=optp)[0]
        opt_dic[optp] = [op_obj.option_name for op_obj in Options.objects.filter(option_type=optype_obj)]
    print("+++++++=============")
    print(opt_dic)
    resp_dic["optp"] = opt_dic
    resp_dic["roles"] = [role_obj.rolename for role_obj in Role.objects.all()]
    return render(request, "xuanxing_html/option-list.html", resp_dic)


def user_upload(request):
    try:
        print('-- user file upload---')
        resp_file = request.FILES.get('file', "")
        # 项目id
        csrf_token = request.POST.get("csrfmiddlewaretoken", "")
        # 读取前端上传来的文件，并写入服务器目录下
        with open('static/user_files/' + str(csrf_token) + "_" + resp_file.name, 'wb') as f:
            for line in resp_file.chunks():
                f.write(line)
        print("----over---")
        file_name = os.getcwd() + "/static/user_files/" + str(csrf_token) + "_" + resp_file.name
        data = openpyxl.load_workbook(file_name)
        # 读取excel里的 职员 页签里的数据
        user_table = data["职员"]
        nrows = list(user_table.rows)
        del nrows[0]
        all_list = [[i.value if i.value else "" for i in r] for r in nrows]
        all_user_list = [user_obj.username for user_obj in ManageUser.objects.all()]
        # 获取user信息
        daoru_flag = 0
        for userinfo_list in all_list:
            u_name = userinfo_list[0]
            if u_name in all_user_list:
                daoru_flag = 1
                break
            u_mobile = userinfo_list[1]
            u_email = userinfo_list[2]
            u_workid = userinfo_list[3]
            u_rz_time = userinfo_list[4]
            u_rz_status = userinfo_list[5]
            if not u_rz_status:
                u_rz_status = 0
            # 存入数据库
            user_obj = ManageUser()
            user_obj.username = u_name
            user_obj.user_mobile = u_mobile
            user_obj.user_email = u_email
            user_obj.user_workid = u_workid
            user_obj.rz_time = u_rz_time.strftime("%Y-%m-%d")
            user_obj.user_status = u_rz_status
            user_obj.save()
        if daoru_flag:
            return JsonResponse({"code": "0002"})
        else:
            return JsonResponse({"code": "0000"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0001"})


def user_add(request):
    if request.method == "GET":
        try:
            resp_json = {"pj_list": [pj.project_name for pj in Projects.objects.all()]}
            resp_json["roles"] = [role_obj.rolename for role_obj in Role.objects.all()]
            return render(request, "xuanxing_html/user_add.html", resp_json)
        except Exception as e:
            print("get 方式有异常")
            print(e)
    else:
        try:
            print("-------post-----")
            recv_data = request.POST.dict()
            username = recv_data.get("username", "")
            pwd = recv_data.get("pwd", "")
            phone_num = recv_data.get("phone_num", "")
            eamil = recv_data.get("email", "")
            work_id = recv_data.get("work_id", "")
            join_time = recv_data.get("join_time", "")
            all_user_list = [user_obj.username for user_obj in ManageUser.objects.all()]
            if username in all_user_list:
                return JsonResponse({"code": "0001"})

            user_obj = ManageUser()
            user_obj.username = username
            user_obj.user_mobile = phone_num
            user_obj.user_email = eamil
            user_obj.user_workid = work_id
            user_obj.user_pwd = md5(pwd.encode("utf-8")).hexdigest()
            user_obj.rz_time = join_time
            user_obj.save()
            return JsonResponse({"code": "0000"})
        except Exception as e:
            print(e)
            print("有异常")
            return JsonResponse({"code": "0002"})


def user_del(request):
    recv_data = request.POST.dict()
    user_id = recv_data.get("uid", "")
    print(user_id)
    try:
        user_id = json.loads(user_id)
    except Exception as e:
        print(e)
        user_id = str(user_id).split(",")
    if isinstance(user_id, str) or isinstance(user_id, int):
        user_id = str(user_id).split(",")
    if user_id:
        print(user_id)
        try:
            for uid in user_id:
                ManageUser.objects.filter(id=int(uid)).delete()
        except Exception as e:
            print("delete exception :%s" % e)
            return JsonResponse({"code": "0002"})
        return JsonResponse({"code": "0000"})


def user_edit(request):
    try:
        if request.method == "GET":
            resp_dic = dict()
            recv_data = request.GET.dict()
            user_id = str(recv_data.get("uid", ""))
            if user_id.isalnum():
                usr_obj = ManageUser.objects.filter(id=int(user_id)).first()
                if not usr_obj:
                    return HttpResponse("用户不存在")
            else:
                return HttpResponse("请求参数错误")
            resp_dic["user_msg"] = {"username": usr_obj.username, "user_mobile": usr_obj.user_mobile,
                                    "user_email": usr_obj.user_email, "user_workid": usr_obj.user_workid,
                                    "rz_time": usr_obj.rz_time, "user_pwd": usr_obj.user_pwd, "uid": usr_obj.id}
            print(resp_dic)
            return render(request, "xuanxing_html/user-edit.html", resp_dic)
        else:
            recv_data = request.POST.dict()
            user_id = str(recv_data.get("uid", ""))
            if user_id.isalnum():
                usr_obj = ManageUser.objects.filter(id=int(user_id)).first()
                if not usr_obj:
                    return JsonResponse({"code": "0002"})
            else:
                return JsonResponse({"code": "0003"})
            print("post modify")
            name_new = format_string(recv_data.get("username", ""))
            pwd_new = format_string(recv_data.get("pwd", ""))
            if not name_new or not pwd_new:
                return JsonResponse({"code": "0001"})
            if name_new != usr_obj.username:
                if ManageUser.objects.filter(username=name_new).first():
                    return JsonResponse({"code": "0004"})  # 用户名已存在

            usr_obj.username = name_new
            usr_obj.user_pwd = md5(pwd_new.encode("utf-8")).hexdigest() if pwd_new != usr_obj.user_pwd else usr_obj.user_pwd
            usr_obj.user_mobile = recv_data.get("phone_num", "")
            usr_obj.user_email = recv_data.get("email", "")
            usr_obj.user_workid = recv_data.get("work_id", "")
            usr_obj.rz_time = recv_data.get("join_time", "")
            usr_obj.save()
            return JsonResponse({"code": "0000"})

    except Exception as e:
        print(e)


def user_status_change(request):
    recv_data = request.POST.dict()
    user_id = recv_data.get("uid", "")
    user_opt = recv_data.get("option", "")
    if user_id:
        print(user_id)
        user_id = int(user_id)
        usr_obj = ManageUser.objects.filter(id=int(user_id)).first()
        print(usr_obj)
        if usr_obj:
            status_old = usr_obj.user_status
            if user_opt == "1":
                usr_obj.user_status = "1"  # 启用
            elif user_opt == "0":
                usr_obj.user_status = "0"
            usr_obj.save()
            c_str = "用户%s的停启用状态由%s 变更为 %s" % (
            usr_obj.username, "停用" if str(status_old) == "0" else "启用", "停用" if str(user_opt) == "0" else "启用")
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            Log.objects.create(operation=c_str, user_id=opt_usr)

            return JsonResponse({"code": "0000"})
        else:
            return JsonResponse({"code": "0002"})

    else:
        print("no user")
        return JsonResponse({"code": "0003"})

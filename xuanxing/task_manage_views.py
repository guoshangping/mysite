# -*- coding:utf-8 -*-
import json
import datetime

from xuanxing.models import Options
from xuanxing.models import Role
from xuanxing.models import ProductStructure
from xuanxing.models import Index

from django.shortcuts import render, redirect
from testm.models import Projects, Pro_speed, Sp_time
from testm import models
from django.http import JsonResponse
from xuanxing.models import ManageUser, ProductsDetail, ProductsType
import django.utils.timezone as timezone
from django.utils.safestring import mark_safe
from django.db.models import Q
from tools.tools import juge_user_pj
from xuanxing.models import Log
from testm.models import Dongtai
from tools.pm_utils_page import PagePaging


# 登录
def login(request):
    if request.method == "GET":
        return render(request, "xuanxing_html/login.html", )
    elif request.method == "POST":
        usr_name = request.POST.get("username", "")
        pwd = request.POST.get("pwd", "")
        print("--------pwd %s" % pwd)
        login_user = ManageUser.objects.filter(username=usr_name).first()
        if login_user:
            if login_user.user_pwd == pwd:
                if str(login_user.user_status) == "0":  # 未启用
                    return JsonResponse({"code": "0001"})
                opt_type_list = []  # 左侧菜单列表
                user_role_list = login_user.user_role.all()  # 登陆者的角色列表
                role_name_list = [role.rolename for role in user_role_list]
                pj_only_mem = []  # 操作员参与的项目名称列表
                mem_opt_list = []  # 操作员权限列表
                opt_list = []  # 权限名称列表

                if "测试经理" in role_name_list or "测试操作员" in role_name_list:
                    # 判断用户身份是否为项目负责人或参与人  负责人权限>参与人权限
                    print("---------pj_only_mem-----------")
                    deal_user_opt = Role.objects.filter(rolename="测试经理").first()  # 测试经理角色
                    mem_user_opt = Role.objects.filter(rolename="测试操作员").first()  # 测试操作员角色
                    # 操作员权限名称列表
                    mem_opt_list = [opt_obj.option_name for opt_obj in mem_user_opt.option.all()]
                    # 负责人负责的项目名称列表
                    deal_pj_list = [pj_obj.project_name for pj_obj in Projects.objects.all() if
                                    login_user in pj_obj.deal_user.all()]
                    # 测试经理权限名称列表
                    opt_list = [opt_obj.option_name for opt_obj in deal_user_opt.option.all()] if deal_pj_list else []
                    # 参与人参与的项目名称列表
                    mem_pj_list = [pj_obj.project_name for pj_obj in Projects.objects.all() if
                                   login_user in pj_obj.members.all()]
                    # 只参与没负责 & 负责 两种情况下得到的权限名称表
                    opt_list = mem_opt_list if mem_pj_list and not opt_list else opt_list
                    print(opt_list)
                    pj_only_mem = list(set(mem_pj_list).difference(set(deal_pj_list)))  # 只参与且没负责的项目名称列表

                # 除了测试经理和测试操作员以外的其他权限
                user_role_list = [role for role in login_user.user_role.all() if role.rolename not in ["测试经理", "测试操作员"]]
                opt_other_list = list(
                    set([op_obj.option_name for user_role in user_role_list for op_obj in user_role.option.all()]))
                opt_list = list(set(opt_list + opt_other_list))
                if "超级管理员" in role_name_list:
                    pj_only_mem = []

                for op_name in opt_list:
                    opt_obj = Options.objects.filter(option_name=op_name).first()
                    if opt_obj:
                        opt_type_name = opt_obj.option_type.type_name
                        if opt_type_name not in opt_type_list:
                            opt_type_list.append(opt_type_name)
                opt_type_list = opt_type_list + opt_list
                opt_type_list = list(set(opt_type_list))
                request.session["opt_list"] = ";".join(opt_list)
                request.session["opt_type_list"] = ";".join(opt_type_list)
                request.session["user_id"] = login_user.id
                request.session["username"] = login_user.username
                request.session["pj_only_mem"] = ";".join(pj_only_mem)
                request.session["mem_opt_list"] = ";".join(mem_opt_list)
                res = JsonResponse({"code": "0000"})
                res.set_cookie("is_login", "1")
                return res
            else:
                return JsonResponse({"code": "0002"})
        else:
            return JsonResponse({"code": "0003"})


def logout(request):
    response = redirect("/xuanxing/login/")
    response.delete_cookie("is_login")
    return response


# 首页
def homepage(request):
    user = request.session.get('username', "")
    is_login = request.COOKIES.get("is_login", "")
    print(is_login)
    print(user)
    user_obj = ManageUser.objects.filter(username=user).first()
    if not user_obj:
        return redirect("/xuanxing/login/")
    elif is_login != "1":
        return redirect("/xuanxing/login/")
    else:
        return render(request, "xuanxing_html/index.html", {"user_obj": user_obj})


def my_info(request):
    user = request.session.get('username')
    user_obj = ManageUser.objects.filter(username=user)

    return render(request, "xuanxing_html/my_info.html", {"user_obj": user_obj})


def my_info_edit(request):
    user = request.session.get('username')
    user_obj = ManageUser.objects.get(username=user)
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        print(mobile)
        email = request.POST.get("email")
        print(email)
        pwd = request.POST.get("pwd")
        print(pwd)
        if mobile and email and pwd:
            obj = ManageUser.objects.filter(username=user)
            print(obj)
            obj.update(user_mobile=mobile, user_email=email, user_pwd=pwd)
            return redirect("/xuanxing/my_info/")

    return render(request, "xuanxing_html/my_info_edit.html", {"user_obj": user_obj})


# 任务管理
def task_manage(request):
    if request.method == "GET":
        page_num_list = list(range(3, 12))
        return render(request, "xuanxing_html/project_list.html", {"page_num_list": page_num_list})
    else:
        curr_page, pro_speed, deal_user, members, start, pro_name = int(
            request.POST.get("current_page", 1)), request.POST.get('pj_speed', ""), request.POST.get(
            'deal_user', ""), request.POST.get('members', ""), request.POST.get('start', ""), request.POST.get(
            'pj_name', "")
        pj_list = [pj_obj for pj_obj in Projects.objects.all()]
        pj_list = [pj for pj in pj_list if pro_name in pj.project_name] if pro_name else pj_list
        pj_list = [pj for pj in pj_list if
                   int(pro_speed) == pj.project_speed.all().first().id] if pro_speed else pj_list
        pj_list = [pj for pj in pj_list if start == pj.creation_time.strftime("%Y-%m-%d")] if start else pj_list
        pj_list = [pj for pj in pj_list if
                   ManageUser.objects.filter(id=int(members)).first() in pj.members.all()] if members else pj_list
        pj_list = [pj for pj in pj_list if
                   ManageUser.objects.filter(id=int(deal_user)).first() in pj.deal_user.all()] if deal_user else pj_list
        sp_obj = [{"id": pro.id, "speed_name": pro.speed_name} for pro in Pro_speed.objects.all()]
        # 搜索框，获取负责人和参与者的显示
        user_list = [{"id": usr.id, "username": usr.username} for usr in ManageUser.objects.all()]
        # 获取项目对象
        pjname_list = juge_user_pj(request.session.get("user_id"))
        all_pj_list = [pj_obj for pj_obj in pj_list if pj_obj.project_name in pjname_list]
        meet_status = {"0": "未知", "1": "选型测试(上会)", "2": "选型测试(不上会)", "3": "选型评估"}
        # 分页

        page_msg_num = int(request.POST.get("msg_num", 8))
        pp_obj = PagePaging(len(all_pj_list), page_msg_num)
        totalpage_num = pp_obj.judge()  # 总页数
        page_obj = pp_obj.re_page(curr_page)  # 返回当前页的分页对象 包含start 和 end
        pj_data_list = [{
            "id": pj.id,
            "pj_name": pj.project_name,
            "deal_user": " ".join([d_user.username for d_user in pj.deal_user.all()]),
            "members": " ".join([m_user.username for m_user in pj.members.all()]),
            "project_speed": " ".join([pro_sp.speed_name for pro_sp in pj.project_speed.all()]),
            "creation_time": pj.creation_time.strftime("%Y-%m-%d"),
            "product_subclass": " ".join([sub_class.child_type for sub_class in pj.product_subclass.all()]),
            "vend_prods": "\n".join([vd.vend_name + "|" + vd.product_name for vd in pj.vend_prod.all()]),
            "meet_status": meet_status[pj.meeting_status]} for pj in
            all_pj_list[page_obj.start:page_obj.end]]
        page_jizhun = 1 if curr_page == 1 else (curr_page - 1) * page_msg_num + 1
        js_res = {"code": "0000", "data": pj_data_list, "user_list": user_list, "sp_obj": sp_obj,
                  "value1": int(pro_speed) if pro_speed else "", "value2": int(deal_user) if deal_user else "",
                  "value3": int(members) if members else "", "total_page": totalpage_num, "curr_page": curr_page,
                  "page_jizhun": page_jizhun, "url": "task_manage"}
        return JsonResponse(js_res)


# 返回添加项目的页面
def project_add_html(request):
    msg = ""
    if request.method == "POST":
        recv_data = request.POST.dict()
        pj_name = recv_data.get("pj_name", "")
        deal_user = recv_data.get("deal_user", "")
        members = recv_data.get("member_list", "")
        project_speed = recv_data.get("pj_speed", "")
        small_class = recv_data.get("small_class", "")
        start_time = request.POST.get("s_time", "")
        end_time = request.POST.get("e_time", "")
        sh_type = request.POST.get("sh_type", "")
        print(pj_name, deal_user, members, project_speed, small_class, sh_type)
        if all([pj_name, deal_user, members, project_speed, small_class]):
            print("-----start-------")
            title_obj = models.Projects.objects.filter(project_name=pj_name).first()
            if not title_obj:
                sub_obj = ProductsType.objects.filter(id=int(small_class)).first()
                exist_pj_list = ["1" if sub_obj in pj_obj.product_subclass.all() else "" for pj_obj in
                                 Projects.objects.all()]
                if "1" in exist_pj_list:
                    return JsonResponse({"code": "0003"})

                obj = models.Projects.objects.create(project_name=pj_name)
                # 选型类型
                if sh_type:
                    obj.meeting_status = str(sh_type)
                # 负责人
                user_obj = ManageUser.objects.filter(id=int(deal_user)).first()
                if user_obj:
                    user_obj.user_role.add(Role.objects.filter(rolename="测试经理").first())
                    user_obj.save()
                obj.deal_user.add(user_obj)

                # 日志
                c_str = "创建了项目" + obj.project_name
                opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
                Log.objects.create(operation=c_str, user_id=opt_usr)
                # 动态
                dt_str = obj.project_name + " ：" + Pro_speed.objects.filter(id=int(project_speed)).first().speed_name
                pj_time = start_time if start_time else datetime.datetime.now().strftime("%Y-%m-%d")
                Dongtai.objects.create(s_time=pj_time, project_id=obj, operation=dt_str)

                # 参与者
                members = json.loads(members)
                for m in members:
                    mem_obj = ManageUser.objects.filter(id=int(m)).first()
                    if mem_obj:
                        mem_obj.user_role.add(Role.objects.filter(rolename="测试操作员").first())
                        mem_obj.save()
                    obj.members.add(mem_obj)

                # 产品类型入库

                # 项目A的产品类型对象
                sub_obj_a = ProductsType.objects.filter(
                    Q(project_name="A") & Q(prod_type=sub_obj.prod_type) & Q(child_type=sub_obj.child_type) & Q(
                        struct_name=sub_obj.struct_name)).first()

                # 指标入库
                if sub_obj:
                    obj.product_subclass.add(sub_obj)
                    # 指标入库
                    for idx_obj in Index.objects.filter(Q(prod_class=sub_obj_a) & Q(project_name="项目A")):
                        print("--==========-------")
                        idx_new = Index()
                        idx_new.project_name = pj_name
                        idx_new.prod_class = sub_obj
                        idx_new.first_index = idx_obj.first_index
                        idx_new.two_index = idx_obj.two_index
                        idx_new.index_explain = idx_obj.index_explain
                        idx_new.index_name = idx_obj.index_name
                        idx_new.index_description = idx_obj.index_description
                        idx_new.index_id = idx_obj.index_id
                        idx_new.anli_id = idx_obj.anli_id
                        idx_new.test_type = idx_obj.test_type
                        idx_new.tool = idx_obj.tool
                        idx_new.remark = idx_obj.remark
                        idx_new.save()
                # 项目进度
                sp_obj = Pro_speed.objects.filter(id=int(project_speed)).first()
                obj.project_speed.add(sp_obj)
                p1 = Projects.objects.filter(project_name=pj_name).first()
                # 进度变更表
                sp_time_obj = Sp_time.objects.create(status=sp_obj.speed_name, name=obj.project_name, pid_id=p1.id)
                if start_time:
                    sp_time_obj.s_time = start_time
                if end_time:
                    sp_time_obj.e_time = end_time
                sp_time_obj.save()
                obj.save()

                print("-----------end --------")
                return JsonResponse({"code": "0000"})
            else:
                return JsonResponse({"code": "0001"})
        return JsonResponse({"code": "0002"})
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({"code": "0002"})

    # 项目进度
    sp_list = [s for s in Pro_speed.objects.all()]
    # 用户列表
    user_list = [u_obj for u_obj in ManageUser.objects.all()]
    # 获取厂商名字
    vend_list = [pd_obj for pd_obj in ProductsDetail.objects.all()]
    # 获取产品类型--三级
    pro_list = [ps_obj.product_structure_name for ps_obj in ProductStructure.objects.all()]

    return render(request, "xuanxing_html/create-obj.html", {"list": user_list,
                                                             "pro_list": pro_list,
                                                             "sp_list": sp_list,
                                                             "msg": msg,
                                                             })


# 单条删除
def project_del(request):
    # 删除项目
    pj_name = request.GET.get("pj_name")
    # print(id)
    obj = models.Projects.objects.get(project_name=pj_name)
    if obj:
        obj.delete()
        # 日志
        d_str = "删除了项目" + obj.project_name
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        Log.objects.create(operation=d_str, user_id=opt_usr)

        return redirect("/xuanxing/task_manage/")


# 批量删除
def pro_delete_all(request):
    recv_data = request.POST.dict()
    select_flag = recv_data.get("select_flag", "")
    box_style = recv_data.get("box_style", "")
    print(box_style)
    if not box_style:
        return JsonResponse({"code": "0004"})
    box_style = json.loads(box_style)
    del_list = []
    for del_id, del_flag in box_style.items():
        if del_flag == "1":
            pj_obj = Projects.objects.filter(id=int(del_id)).first()
            del_list.append(pj_obj.project_name)
            pj_obj.delete()
    # 对全选的进行处理
    if select_flag == "1":
        del_all_pj = [del_pj for del_pj in Projects.objects.all() if str(del_pj.id) not in box_style]
        for pj in del_all_pj:
            del_list.append(pj.project_name)
            pj.delete()
    d_str = "删除了项目" + ",".join(del_list)
    opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
    Log.objects.create(operation=d_str, user_id=opt_usr)
    # 删除成功返回显示页
    return JsonResponse({"code": "0000"})


# 编辑
def pro_edit(request):
    msg = ""
    id = request.GET.get("id")
    project_obj = Projects.objects.get(id=int(id))
    # 负责人和参与者
    u_name_list = [[u_obj.username, u_obj.id] for u_obj in ManageUser.objects.all()]
    pj_u_name_list = [[m_obj.username, m_obj.id] for m_obj in project_obj.members.all()]
    # 负责人
    pj_deal_usr = project_obj.deal_user.all().first()
    pj_deal_user = [pj_deal_usr.username if pj_deal_usr else "", pj_deal_usr.id if pj_deal_usr else ""]
    # 选型类型
    meet_status = {"1": "选型测试(上会)", "2": "选型测试(不上会)", "3": "选型评估"}

    if request.method == "POST":
        title = request.POST.get("title")
        deal_user = request.POST.get("deal_user")
        members = request.POST.getlist("members")
        meet_type = request.POST.get("meet_type", "0")

        if title and deal_user and members:
            get_obj = models.Projects.objects.get(id=id)
            # 进度时间
            user_objs = ManageUser.objects.filter(id=int(deal_user))
            members_objs = ManageUser.objects.filter(id__in=members)
            # 多对多字段
            get_obj.deal_user.set(user_objs)
            get_obj.members.set(members_objs)

            for usr_obj in user_objs:
                if usr_obj:
                    usr_obj.user_role.add(Role.objects.filter(rolename="测试经理").first())
                    usr_obj.save()

            for mem_obj in members_objs:
                if mem_obj:
                    mem_obj.user_role.add(Role.objects.filter(rolename="测试操作员").first())
                    mem_obj.save()

            # get_obj.product_subclass.set(class3_objs)
            get_obj.meeting_status = str(meet_type)
            get_obj.save()

            # 日志写入记录
            u_obj = user_objs[0]
            if pj_deal_user[0] != u_obj.username:
                u_str = "更改" + project_obj.project_name + "负责人: " + pj_deal_user[0] + "---->" + u_obj.username
                opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
                Log.objects.create(operation=u_str, user_id=opt_usr)

            # 日志写入记录
            m = ",".join([m.username for m in members_objs])
            mo1 = ",".join([ul_obj[0] for ul_obj in pj_u_name_list])
            if mo1 != m:
                m_str = "更改" + project_obj.project_name + "参与者: " + mo1 + "---->" + m
                opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
                Log.objects.create(operation=m_str, user_id=opt_usr)

            # 更新项目名称
            get_obj.project_name = title
            get_obj.save()
            # 更新项目进度的时间
            # 项目进度关联表，改变进度获取对应开始时间，结束时间

        return redirect("/xuanxing/task_manage/")

    return render(request, "xuanxing_html/pro_edit.html", {"msg": msg,
                                                           "project_obj": project_obj,
                                                           "pj_deal_user": pj_deal_user,
                                                           "u_name_list": u_name_list,
                                                           "pj_u_name_list": pj_u_name_list,
                                                           "meet_status": meet_status
                                                           })


def sp_time(request):
    if request.method == "GET":
        pro_id = request.GET.get("id")
        t_list = []
        p = Sp_time.objects.filter(pid_id=pro_id)

        for j in p:
            p_obj = mark_safe(
                '<td>' + j.status + '</td><td>' + str((j.s_time).strftime("%Y-%m-%d")) + '</td><td>' + str(
                    (j.e_time).strftime("%Y-%m-%d")) + '</td><td>' + str(j.pid.project_name) + '</td>')
            t_list.append(p_obj)

        project_obj = Projects.objects.get(id=int(pro_id))
        print("--------======")
        print(project_obj)
        # 取进度时间
        time_obj = Sp_time.objects.filter(pid=project_obj).last()
        pj_start_time = time_obj.s_time.strftime("%Y-%m-%d") if time_obj else ""
        pj_end_time = time_obj.e_time.strftime("%Y-%m-%d") if time_obj else ""

        # 项目进度
        speed_list = [[ps_obj.speed_name, ps_obj.id] for ps_obj in Pro_speed.objects.all()]
        pj_speed = project_obj.project_speed.all().first()
        pj_speed = pj_speed.speed_name if pj_speed else ""

        return render(request, "xuanxing_html/sp_time.html",
                      {"t_list": t_list, "speed_list": speed_list, "pj_speed": pj_speed, "pj_start_time": pj_start_time,
                       "pj_end_time": pj_end_time, "pj_id": pro_id})

    else:
        print(request.POST.dict())
        project_speed = request.POST.get("project_speed", "")
        pj_id = request.POST.get("pj_id", "")  # 项目ID
        project_obj = Projects.objects.filter(id=int(pj_id)).first()
        # 项目时间
        s_time = request.POST.get('start_time', '')
        e_time = request.POST.get('end_time', '')

        sp_objs = Pro_speed.objects.filter(id=int(project_speed))
        sp_orgin = project_obj.project_speed.all().first().speed_name
        project_obj.project_speed.set(sp_objs)
        project_obj.save()

        # 日志写入记录
        s_obj = sp_objs[0]
        s_str = "更改" + project_obj.project_name + "项目进度: " + sp_orgin + "---->" + s_obj.speed_name
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        Log.objects.create(operation=s_str, user_id=opt_usr)
        # 动态写入
        dt_str = project_obj.project_name + " ：" + sp_orgin + "--->" + s_obj.speed_name
        Dongtai.objects.create(s_time=s_time, project_id=project_obj, operation=dt_str)

        # 进度表更新
        pj_sp = Pro_speed.objects.filter(id__in=project_speed).first()
        if sp_objs and pj_sp:
            Sp_time.objects.create(s_time=s_time,
                                   name=project_obj.project_name,
                                   pid_id=int(pj_id),
                                   status=pj_sp.speed_name,
                                   e_time=e_time
                                   )
            sp_list = [spts_obj for spts_obj in Sp_time.objects.filter(pid_id=int(pj_id))]
            if len(sp_list) > 1:
                sp_list[-2].e_time = s_time
                sp_list[-2].save()
        return JsonResponse({"code": "0000"})


def product_manage(request):
    uid = request.session.get("user_id")
    pj_list = juge_user_pj(uid)
    return render(request, "xuanxing_html/tree.html", {"pjname_list": pj_list})


def prod_type_query(request):
    recv_data = request.POST.dict()
    big_cls = recv_data.get("big_cls_name", "")
    mid_cls = recv_data.get("mid_cls_name", "")
    sml_cls = recv_data.get("sml_cls_name", "")
    pj_name = recv_data.get("pj_name", "B")
    print("------start------")
    print(recv_data)
    child_type_list = []
    vend_list = []
    if big_cls:
        big_cls_obj = ProductStructure.objects.filter(product_structure_name=big_cls).first()
        if big_cls_obj:
            pdt_list = list(set([pdt_obj.prod_type for pdt_obj in
                                 ProductsType.objects.filter(Q(project_name=pj_name) & Q(struct_name=big_cls_obj))]))
            if mid_cls:
                child_type_list = list(
                    set([(pdt_obj.child_type, pdt_obj.id) for pdt_obj in ProductsType.objects.filter(
                        Q(project_name=pj_name) & Q(struct_name=big_cls_obj) & Q(prod_type=mid_cls))]))
                if sml_cls:
                    sml_cls = sml_cls.split("-")[0]
                    pdt_obj = ProductsType.objects.filter(
                        Q(project_name=pj_name) & Q(struct_name=big_cls_obj) & Q(prod_type=mid_cls) & Q(
                            child_type=sml_cls)).first()
                    if pdt_obj:
                        vend_list = ["%s|%s|%s" % (pd_obj.vend_name, pd_obj.product_name, pd_obj.id) for pd_obj in
                                     ProductsDetail.objects.filter(Q(product_type=pdt_obj) & Q(project_name=pj_name))]
            print(vend_list)
            return JsonResponse(
                {"code": "0000", "pdt_list": pdt_list, "child_type_list": child_type_list, "vend_list": vend_list})
    return JsonResponse({"code": "0001"})

# 日志先关代码

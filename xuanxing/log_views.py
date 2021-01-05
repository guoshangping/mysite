# -*- coding:utf-8 -*-
from django.shortcuts import render
from xuanxing.models import Log
from xuanxing.models import ManageUser
from django.http import JsonResponse
from tools.pm_utils_page import PagePaging


def log(request):
    # 时间和操作对象
    if request.method == "GET":
        user_list = Log.objects.values("user_id").distinct()
        print(user_list)
        user_list = [usr["user_id"] for usr in user_list]
        user_dic = {user_id: ManageUser.objects.filter(id=int(user_id)).first().username for user_id in user_list}
        page_list = list(range(4, 10))
        return render(request, "xuanxing_html/log.html", {"user_all": user_dic, "page_list": page_list})
    else:
        recv_data = request.POST.dict()
        op_user = recv_data.get("op_user", "")
        op_content = recv_data.get("op_content", "")
        curr_page = int(recv_data.get("current_page", 1))
        user = ManageUser.objects.filter(id=int(request.session.get("user_id", ""))).first()
        if user:
            log_all = Log.objects.all()[::-1]
            if op_user:
                log_all = [log_obj for log_obj in log_all if log_obj.user_id == int(op_user)]
            if op_content:
                log_all = [log_obj for log_obj in log_all if op_content in log_obj.operation]
            # 分页开始
            page_msg_num = int(recv_data.get("msg_num", 8))
            pp_obj = PagePaging(len(log_all), page_msg_num)
            totalpage_num = pp_obj.judge()  # 总页数
            page_obj = pp_obj.re_page(curr_page)  # 返回当前页的分页对象 包含start 和 end
            page_jizhun = 1 if curr_page == 1 else (curr_page - 1) * page_msg_num + 1

            role_list = [u_obj.rolename for u_obj in user.user_role.all()]
            if "reporter" in role_list or "超级管理员" in role_list:
                log_list = [[log_obj.s_time, log_obj.user_id.user_role.all().first().rolename, log_obj.user_id.username, log_obj.operation] for log_obj in log_all[page_obj.start:page_obj.end]]
            else:
                log_list = [[log_obj.s_time, log_obj.user_id.user_role.all().first().rolename, log_obj.user_id.username, log_obj.operation] for log_obj in log_all[page_obj.start:page_obj.end] if log_obj.user_id == user]
            return JsonResponse({"code": "0000", "data": log_list, "total_page": totalpage_num, "curr_page": curr_page, "page_jizhun": page_jizhun, "url": "log"})
        return JsonResponse({"code": "0000"})

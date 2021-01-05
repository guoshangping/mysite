# -*- coding:utf-8 -*-
import os
import collections

from django.core import serializers
from django.shortcuts import render
from django.db.models import Q
import docx
import re
import json
from docxtpl import DocxTemplate
from docxtpl import RichText
from testm.models import Projects
from xuanxing.models import CaseDocx
from xuanxing.models import CaseMiddleType
from xuanxing.models import CaseSamllType
from xuanxing.models import AnliDoc
from django.http import HttpResponse, JsonResponse
from tools.tools import title_deal
from tools.tools import juge_user_pj
from django.utils.encoding import escape_uri_path
from xuanxing.models import Log
from xuanxing.models import ManageUser
from xuanxing.models import AnliMap
from tools.pm_utils_page import PagePaging
from django.db import transaction
from itertools import product


def test_anli_list(request):
    anli_dic = dict()
    pj_list = juge_user_pj(request.session.get("user_id", ""))
    search_pjname = request.GET.get("pj_name", "")
    if search_pjname:
        pj_list = [pjname for pjname in pj_list if search_pjname in pjname]
    anli_dic["search_pjname"] = search_pjname
    anli_dic["anli_list"] = [{"pj_name": pj.project_name,
                              "pj_deal": " ".join([d_user.username for d_user in pj.deal_user.all()]),
                              "pj_members": " ".join([m_user.username for m_user in pj.members.all()]), }
                             for pj in Projects.objects.filter(project_name__in=pj_list)]
    print("-----------")

    return render(request, "xuanxing_html/anli_list.html", anli_dic)


def test_anli(request):
    if request.method == "GET":
        pj_name = request.GET.get("pj_name", "")
        project_obj = Projects.objects.filter(project_name=pj_name).first()
        doc_name_list = [doc_obj.doc_name for doc_obj in AnliDoc.objects.filter(project_id=project_obj)]
        page_num_list = list(range(4, 11))
        resp_dic = {"pj_id": project_obj.id if project_obj else "", "pj_name": pj_name, "doclist": doc_name_list, "page_num_list": page_num_list}
        return render(request, "xuanxing_html/anli_info.html", resp_dic)
    else:
        recv_data = request.POST.dict()
        rsp_doc_name = recv_data.get("doc_name", "")
        pj_name = recv_data.get("pj_name", "")
        curr_page = int(recv_data.get("current_page", 1))
        project_obj = Projects.objects.filter(project_name=pj_name).first()

        if rsp_doc_name not in ["", "无"]:
            anli_doc_obj = AnliDoc.objects.filter(doc_name=rsp_doc_name, project_id=project_obj).first()
            case_type_list = [sm_obj.id for sm_obj in
                              CaseSamllType.objects.filter(doc_name=anli_doc_obj, project=project_obj)]
        else:
            anli_doc_obj = AnliDoc.objects.filter(project_id=project_obj).last()
            case_type_list = [sm_obj.id for sm_obj in
                              CaseSamllType.objects.filter(doc_name=anli_doc_obj, project=project_obj)]
        if case_type_list:
            # 文档名为rsp_doc_name的文档下的 所有案例
            all_case_list = [case_obj for case_obj in CaseDocx.objects.filter(case_type__in=case_type_list)]
            # 分页开始
            page_msg_num = int(recv_data.get("msg_num", 8))
            pp_obj = PagePaging(len(all_case_list), page_msg_num)
            totalpage_num = pp_obj.judge()  # 总页数
            page_obj = pp_obj.re_page(curr_page)  # 返回当前页的分页对象 包含start 和 end
            page_jizhun = 1 if curr_page == 1 else (curr_page - 1) * page_msg_num + 1
            data_list = [{"id": cs_obj.id, "s_type_name": cs_obj.case_type.s_type_name, "test_goal": cs_obj.test_goal,
                          "pre_condition": cs_obj.pre_condition, "test_steps": cs_obj.test_steps,
                          "expect_result": cs_obj.expect_result, "test_result": cs_obj.test_result,
                          "test_conclusion": cs_obj.test_conclusion, "remark": cs_obj.remark,
                          "check_person": cs_obj.check_person} for cs_obj in
                         all_case_list[page_obj.start:page_obj.end]]
            return JsonResponse({"code": "0000", "data": data_list, "curr_page": curr_page,
                                 "page_jizhun": page_jizhun, "url": "anli", "total_page": totalpage_num,})


# 导入并接收文件
def anli_upload(request):
    try:
        print('--file upload---')
        resp_file = request.FILES.get('file', "")  # 文件体
        pj_name = request.POST.get("pj_name", "")  # 项目名
        rsp_doc_name = resp_file.name  # 文档名
        pj_obj = Projects.objects.filter(project_name=pj_name).first()
        print(rsp_doc_name)
        if rsp_doc_name.split(".")[-1] != "docx":
            return JsonResponse({"code": "0005"})
        files_mulu = os.getcwd() + "/static/anli_docs"
        if not all([pj_name, rsp_doc_name, pj_obj]):
            return JsonResponse({"code": "0010"})
        anlidoc_list = [al_doc_obj.doc_name for al_doc_obj in AnliDoc.objects.filter(project_id=pj_obj)]
        cover_flag = 0
        if rsp_doc_name in anlidoc_list:
            cover_flag = 1
        # 读取前端上传来的文件，并写入服务器目录下
        if cover_flag:
            os.remove(files_mulu + "/" + "hassaved" + str(pj_name) + "$" + resp_file.name)
            print('已刪除的案例doc' + str(resp_file.name))

        with open('static/anli_docs/' + str(pj_name) + "$" + resp_file.name, 'wb') as f:
            for line in resp_file.chunks():
                f.write(line)
        # 文档名入库
        if cover_flag:
            AnliDoc.objects.filter(doc_name=rsp_doc_name, project_id=pj_obj).delete()
        anli_doc_obj = AnliDoc()
        anli_doc_obj.doc_name = rsp_doc_name
        anli_doc_obj.project_id = pj_obj
        anli_doc_obj.save()

        # 案例信息入库
        code_str = save_db(str(pj_name) + "$" + resp_file.name)
        if code_str == "0000":
            print("----over---")
            # 日志
            c_str = "为项目%s上传了案例文档%s" % (pj_name, rsp_doc_name)
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            Log.objects.create(operation=c_str, user_id=opt_usr)
            return JsonResponse({"code": "0000"})
        else:
            return JsonResponse({"code": code_str})
    except Exception as e:
        print("-------------file upload exception----------")
        print(e)
        return JsonResponse({"code": "0004"})


# 把上传的案例文档存入数据库
@transaction.atomic
def save_db(file_name):
    files_mulu = os.getcwd() + "/static/anli_docs"
    file_list = os.listdir(files_mulu)
    print("------000000")
    print(file_list)
    save_flag = 0
    try:
        if not file_name.startswith("hassaved"):
            pj_name = file_name.split("$")[0]  # 项目名称
            fn = files_mulu + "/" + file_name
            # 读取word文件,必须为docx格式`
            doc_obj = docx.Document(fn)
            title_all = title_deal(fn)
            te_list = [dc for dc in title_all if re.match(r"^\d{1}\.\d{1}\.\d{1}.*\D+$", dc)]  # 二级标题(闭口用来防止拿到文档名字或者目录)
            te_three_list = [dc for dc in title_all if re.match(r"^\d{1}\.\d{1}\.\d{1}\.\d{1}.*\D+$", dc)]  # 三级标题
            te_all_list = [dc for dc in title_all if re.match(r"^\d{1}\.\d{1}.*\D+$", dc)]  # 所有标题
            te_cha_list = sorted(list(set(te_all_list).difference(set(te_list))))  # 一级标题  通过取差集得到
            # 取得真正的二级标题 摈弃三级标题
            print("------2222222222")
            print(te_cha_list)

            new_three_list = []
            remove_list = []
            nw_te_list = []
            # 文档的数据库对象
            al_doc_obj = AnliDoc.objects.filter(doc_name=file_name.split("$")[-1], project_id=Projects.objects.filter(
                project_name=pj_name).first()).first()

            if te_three_list:
                te_three_cha_list = sorted(list(set(te_list).difference(set(te_three_list))))  # ["1.1.1", "1.1.2"]

                for te_title in te_three_cha_list:  # 遍历["1.1.1", "1.1.2"]
                    for te_three_title in te_three_list:  # 遍历["1.1.1.1", "1.1.1.2"]
                        if te_three_title.startswith(te_title[0:5]):  # 1.1.1.1是以 1.1.1开头
                            te_three_title = te_title + "【" + te_three_title[7:] + "】"  # 1.1.1 【1.1.1.1后面的内容】
                            new_three_list.append(te_three_title)  # 放入新列表存放 1.1.1 【1.1.1.1后面的内容】
                            remove_list.append(te_title)  # 把循环过的1.1.1放入 删除名单列表 里
                print(new_three_list)
                remove_list = list(set(remove_list))
                for t in remove_list:
                    te_list.remove(t)

                for te_x in te_list:  # 循环 ["1.1.1","1.1.2"]
                    for te_y in new_three_list:  # 循环 ["1.1.1 【1.1.1.1后面的内容】" , "1.1.2 【1.1.1.2后面的内容】"]
                        if re.match(r"^\d{1}\.\d{1}\.\d{1}\.\d{1}.*\D+$", te_x) and te_x[
                                                                                    7:] in te_y:  # 把二级标题列表里的 1.1.1.1 替换成 1.1.1 【1.1.1.1后面的内容】
                            te_x = te_y
                    nw_te_list.append(te_x)  # ["1.1.1", "1.1.1 【1.1.1.1后面的内容】", "1.1.2...", "1.1.2 【1.1.1.2后面的内容】"]

                nw_i = 0  # 计算循环数
                p1 = re.compile(r'\d.*\d', re.S)
                new_t_list = []
                for nw_title in nw_te_list:  # 遍历["1.1.1", "1.1.1 【1.1.1.1后面的内容】", "1.1.2...", "1.1.2 【1.1.1.2后面的内容】"]  之前排好序的
                    if nw_i != 0:
                        nw_1 = re.findall(p1, nw_title)[0].split(".")  # [1.1.1]
                        nw_2 = re.findall(p1, new_t_list[nw_i - 1])[0].split(".")  #
                        if nw_1[0:2] == nw_2[0:2]:
                            # 把重复的1.1.1 1.1.1 重新编号 1.1.1 , 1.1.2
                            nw_title = ".".join(nw_2[0:2] + [str(int(nw_2[2]) + 1)]) + \
                                       nw_title.split(re.findall(p1, nw_title)[0])[-1]
                    nw_i += 1
                    new_t_list.append(nw_title)
                print(new_t_list)
                nw_te_list = new_t_list  # 处理好的标题

            tb_all_list = []

            if nw_te_list:
                te_list = nw_te_list
            project_obj = Projects.objects.filter(project_name=pj_name).first()
            for p_num, paragraph in enumerate(te_list):
                print(paragraph)
                tb_dic = {}
                # {  for an in AnliMap.objects.all()}
                tb_field_map = {an.anli_name: an.anli_key for an in AnliMap.objects.all()}

                for tb_num, table in enumerate(doc_obj.tables):
                    # 一个标题对应一个表格
                    if p_num == tb_num:
                        tb_dic["case_type"] = paragraph  # 二级标题 1.1.1
                        # 取二级标题
                        p_list = [para for para in te_cha_list if para[0:3] == paragraph[0:3]]
                        tb_dic["case_middle_type"] = p_list[0]
                        tb_dic["case_big_type"] = "数据库"  # todo 無用

                        for row in table.rows:
                            rw_list = [rw.text for rw in row.cells]
                            rw_list.pop(0)  # 去除第一个
                            new_list = []
                            for rl in rw_list:
                                if rl in ["测试日期", "供应商"]:
                                    rl = ""
                                # 合并单元格后 第一个格的内容会重复两次以上，所以要进行下面的操作
                                if rl not in new_list:
                                    new_list.append(rl)
                                else:
                                    new_list.append("")
                            # new_list = [nw.replace("\n", "") for nw in new_list]

                            rw_list = "           ".join(new_list)
                            rw_list = rw_list.replace("\n", "<br/>")
                            if "操作员" in row.cells[0].text or "复核员" in row.cells[0].text:
                                tb_dic["check_person"] = rw_list
                            else:
                                if row.cells[0].text in tb_field_map:
                                    if tb_field_map[row.cells[0].text] not in tb_dic:
                                        tb_dic[tb_field_map[row.cells[0].text]] = rw_list
                                    else:
                                        tb_dic[tb_field_map[row.cells[0].text]] = tb_dic[tb_field_map[
                                            row.cells[0].text]] + "<br/>" + rw_list
                        break
                tb_all_list.append(tb_dic)

            # 遍历所有的表格 tbs代表一个表格，格式是json

            for tbs in tb_all_list:
                # 中类的创建
                case_middle_type_obj = CaseMiddleType.objects.filter(m_type_name=tbs.get("case_middle_type", ""),
                                                                     md_project=project_obj).first()
                if not case_middle_type_obj:
                    if tbs.get("case_middle_type", ""):
                        md_type_obj = CaseMiddleType()
                        md_type_obj.m_type_name = tbs.get("case_middle_type")
                        md_type_obj.md_project = project_obj
                        if al_doc_obj:
                            md_type_obj.doc_name = al_doc_obj
                        md_type_obj.save()
                        case_middle_type_obj = md_type_obj
                # 小类的创建
                case_type_obj = CaseSamllType.objects.filter(s_type_name=tbs.get("case_type", ""),
                                                             project=project_obj).first()
                if not case_type_obj:
                    if tbs.get("case_type", ""):
                        sm_type_obj = CaseSamllType()
                        sm_type_obj.s_type_name = tbs.get("case_type")
                        sm_type_obj.m_type = case_middle_type_obj
                        if al_doc_obj:
                            sm_type_obj.doc_name = al_doc_obj
                            sm_type_obj.project = project_obj
                        sm_type_obj.save()
                        case_type_obj = sm_type_obj
                # 案例文档数据库对象的创建
                cs_obj = CaseDocx()
                cs_obj.case_type = case_type_obj  # 案例的小类
                cs_obj.case_id = tbs.get("case_id", "")
                cs_obj.test_goal = tbs.get("test_goal", "")
                cs_obj.pre_condition = tbs.get("pre_condition", "")
                cs_obj.test_steps = tbs.get("test_steps", "")
                cs_obj.expect_result = tbs.get("expect_result", "")
                cs_obj.test_result = tbs.get("test_result", "")
                cs_obj.test_conclusion = tbs.get("test_conclusion", "")
                cs_obj.remark = tbs.get("remark", "")
                cs_obj.check_person = tbs.get("check_person", "")
                cs_obj.save()
            save_flag = 1  # 走到这步，代表入库成功
            # 把此次处理完的word文件命名修改,以防下次重复读取
            if f"hassaved{file_name}" in file_list:
                os.remove(files_mulu + "/" + f"hassaved{file_name}")
            os.rename(files_mulu + f"/{file_name}", files_mulu + "/" + f"hassaved{file_name}")
            if save_flag:
                return "0000"
            else:
                print("0001")
                return "0001"
        return "0002"
    except Exception as e:
        print("------exception----------")
        print(e)
        return "0003"


def show_doc_data(request):
    project_id = request.GET.get("pj_id", "")
    small_type_list = [sm_obj.id for sm_obj in
                       CaseSamllType.objects.filter(project=Projects.objects.filter(id=int(project_id)).first())]
    print("--------------1")
    print(small_type_list)
    all_doc_list = CaseDocx.objects.filter(case_type__in=small_type_list)
    show_list = json.loads(serializers.serialize("json", all_doc_list))
    all_show_list = [s.get("fields", {}) for s in show_list]
    resp_dic = dict()
    resp_dic["resp"] = all_show_list

    key_map = {
        "case_id": "案例编号",
        "test_goal": "测试目的",
        "pre_condition": "预置条件",
        "test_steps": "测试步骤",
        "expect_result": "预期结果",
        "test_result": "实测结果",
        "test_conclusion": "测试结论",
        "remark": "备注",
        "check_person": "操作员 复核员",
    }

    new_resp = []
    for rsp in resp_dic["resp"]:
        new_rsp = dict()
        g_rsp = dict()
        g_rsp["case_type"] = CaseSamllType.objects.filter(id=int(rsp["case_type"]))[0].s_type_name
        new_rsp["g_rsp"] = g_rsp
        del rsp["creation_time"]
        del rsp["case_type"]

        for rp in rsp:
            rsp[rp] = str(rsp[rp]).replace(r'\n', '<br/>')
        new_rsp_dic = {}
        for rp in rsp:
            if rp in key_map:
                new_rsp_dic[key_map[rp]] = rsp[rp]
        new_rsp["y_rsp"] = new_rsp_dic
        new_resp.append(new_rsp)
    return render(request, "xuanxing_html/show_doc.html", {"resp": new_resp})


def anli_view(request):
    if request.method == "GET":
        anli_id = request.GET.get("anli_id", "")
        case_obj = CaseDocx.objects.filter(id=int(anli_id)).first()
        return render(request, "xuanxing_html/anli_view.html", {"case_obj": case_obj})
    else:
        pass


def anli_del(request):
    try:
        anli_id = request.POST.get("anli_id", "")
        CaseDocx.objects.filter(id=int(anli_id)).delete()
        return JsonResponse({"code": "0000"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": "0001"})


def daochu_anli_word(request):
    if request.method == "POST":
        recv_data = request.POST.dict()
        select_flag = recv_data.get("select_flag", "")
        box_style = recv_data.get("box_style", "")
        if not box_style:
            return JsonResponse({"code": "0004"})
        box_style = json.loads(box_style)
        daochu_list = [daochu_id for daochu_id, daochu_flag in box_style.items() if daochu_flag == "1"]
        # 对全选的进行处理
        if select_flag == "1":
            for daochu_pj in CaseDocx.objects.all():
                if str(daochu_pj.id) not in box_style:
                    daochu_list.append(str(daochu_pj.id))
        d_str = "导出了案例"
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        Log.objects.create(operation=d_str, user_id=opt_usr)
        # 删除成功返回显示页

        return JsonResponse({"code": "0000", "check_str": json.dumps(daochu_list)})

    if request.method == "GET":
        anli_ids = request.GET.get("anli_ids", "")
        pj_id = request.GET.get("pj_id", "")
        pj_id = int(pj_id)
        if anli_ids:
            anli_ids = eval(anli_ids)
            if isinstance(anli_ids, int):
                anli_ids = [anli_ids]
            project_name = Projects.objects.filter(id=int(pj_id)).first().project_name
            fl_name = "%s测试案例" % project_name
            print(fl_name)
            anli_ids = [int(anli) for anli in anli_ids]
            # 获取当前传来的案例id，并读出数据库里的案例对象
            case_test_obj = CaseDocx.objects.filter(id=anli_ids[0]).first()
            rsp_doc_id = 0
            if case_test_obj:
                rsp_doc_name = case_test_obj.case_type.doc_name.doc_name
                rsp_doc_id = AnliDoc.objects.filter(doc_name=rsp_doc_name, project_id=pj_id)[0].id
            case_obj_list = CaseDocx.objects.filter(id__in=anli_ids)

            show_list = json.loads(serializers.serialize("json", case_obj_list))
            all_show_list = [anli_obj.get("fields", {}) for anli_obj in show_list]
            # all_show_list = [cs_obj for cs_obj in case_obj_list]
            anli_dic = {}
            for anl in all_show_list:
                case_id = anl["case_type"]
                anl["case_type"] = CaseSamllType.objects.filter(id=int(case_id))[0].s_type_name
                anl["case_middle_type"] = CaseSamllType.objects.filter(id=int(case_id)).first().m_type.m_type_name
                if anl["case_middle_type"] not in anli_dic:
                    anli_dic[anl["case_middle_type"]] = [anl]
                else:
                    anli_dic[anl["case_middle_type"]].append(anl)
            middle_obj_list = CaseMiddleType.objects.filter(Q(md_project=pj_id) & Q(doc_name=rsp_doc_id))
            md_list = [md_obj.m_type_name for md_obj in middle_obj_list]

            for al in anli_dic:
                i = 1
                for ali in anli_dic[al]:
                    ali_bt = ali["case_type"]

                    ali_list = re.findall(r"\d.*\.\d{0,8}", ali_bt)[0].split(".")
                    ali_list[-1] = str(i)
                    ali_new_str = re.sub(r"\d.*\.\d{0,8}", ".".join(ali_list), ali_bt)
                    rt = RichText()
                    if i != 1:
                        ali_new_str = "\f" + ali_new_str
                    rt.add(ali_new_str, size=30, font="Times New Roman")
                    ali["case_type"] = rt
                    i += 1

            sorted_dic = collections.OrderedDict()
            for md_title in md_list:
                if md_title in anli_dic:
                    sorted_dic[md_title] = anli_dic[md_title]
                else:
                    sorted_dic[md_title] = {}

            anli_new_dic = collections.OrderedDict()
            h1_flag = 0
            for anli_k, anli_v in sorted_dic.items():
                rt_md = RichText()
                if h1_flag:
                    anli_k = "\f" + anli_k
                else:
                    h1_flag = 1
                rt_md.add(anli_k, size=40, font="Times New Roman")

                for a_dic in anli_v:
                    for a_k in a_dic:
                        if r"<br/>" in str(a_dic[a_k]):
                            br_rt = RichText()
                            new_ak = a_dic[a_k].replace(r"<br/>", "\n")
                            br_rt.add(new_ak)
                            a_dic[a_k] = br_rt
                anli_new_dic[rt_md] = anli_v

            context = {"all_anli": anli_new_dic, "pj_name": project_name}
            template_docx = DocxTemplate(os.getcwd() + "/static/anli/anli_muban/anli_muban.docx")
            template_docx.render(context)
            template_docx.save(os.getcwd() + f"/static/anli/anli_daochu/anli_{fl_name}.docx")
            response = HttpResponse(content_type='application/msword')

            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
                escape_uri_path(f"{fl_name}.docx"))
            template_docx.save(response)
            return response


def anli_map(request):
    return render(request, "xuanxing_html/anli_map.html")


def anli_map_init(request):
    anli_dic = {}
    with open('static/anli/anli_map/' + "anli_map.json", 'rb') as f:
        # 定义为只读模型，并定义名称为f
        anli_dic = json.load(f)
    print(anli_dic)
    anli_name_list = [a_obj.anli_name for a_obj in AnliMap.objects.all()]
    for k in anli_dic:
        if k not in anli_name_list:
            AnliMap.objects.create(anli_key=anli_dic[k], anli_name=k)
    # map(lambda k: AnliMap.objects.create(anli_key=k[1], anli_name=k[0]) if k[0] not in anli_name_list else "",anli_dic.items())
    return JsonResponse({"code": "0000"})


def anli_map_query(request):
    query_field = request.POST.get("anli_key", "")
    if query_field == "请选择字段":
        an_list = AnliMap.objects.all().order_by("anli_key")
    else:
        an_list = AnliMap.objects.filter(anli_key=query_field)
    an_list = [{"id": an.id, "anli_key": an.anli_key, "anli_name": an.anli_name} for an in an_list]
    an_key_list = list(set([an.anli_key for an in AnliMap.objects.all()]))
    return JsonResponse({"code": "0000", "anli_fields": an_key_list, "anli_maps": an_list})


def anli_map_opt(request):
    opt = request.POST.get("opt", "")
    if opt == "add":
        anli_key = request.POST.get("anli_key", "")
        anli_name = request.POST.get("anli_name", "")
        if anli_name and anli_key:
            AnliMap.objects.create(anli_key=anli_key, anli_name=anli_name)
            return JsonResponse({"code": "0000"})
        else:
            return JsonResponse({"code": "0001"})
    elif opt == "del":
        del_id = request.POST.get("del_id", "")
        if del_id:
            AnliMap.objects.filter(id=int(del_id)).first().delete()
            return JsonResponse({"code": "0000"})
        else:
            return JsonResponse({"code": "0001"})


def project_tongji(request):
    return render(request, "xuanxing_html/objbg.html")


def product_tongji(request):
    return render(request, "xuanxing_html/objbg.html")


def index_tongji(request):
    return render(request, "xuanxing_html/objbg.html")


def test_fangan(request):
    anli_dic = dict()
    anli_dic["proj"] = [{"pj_name": pj.project_name,
                         "pj_deal": " ".join([d_user.username for d_user in pj.deal_user.all()]),
                         "pj_members": " ".join([m_user.username for m_user in pj.members.all()]), }
                        for pj in Projects.objects.all()]

    return render(request, "xuanxing_html/obj2.html", anli_dic)


def test_report(request):
    return render(request, "xuanxing_html/objbg.html")

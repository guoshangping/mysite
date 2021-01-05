# -*- coding:utf-8 -*-
import re
import docx
from xuanxing.models import ManageUser
from testm.models import Projects
from django.shortcuts import render, redirect
from xuanxing.models import Log
from xuanxing.models import ManageUser
from xuanxing.models import Role
from xuanxing.models import XuanXingRank
from xuanxing.models import ZhuangXiangRank
from xuanxing.models import ChushiRank



def save_files(mulu, file_name, resp_file):
    with open(mulu + file_name, 'wb') as f:
        for line in resp_file.chunks():
            f.write(line)


def juge_user_pj(uid):
    pj_list = []
    if uid:
        login_user = ManageUser.objects.filter(id=int(uid)).first()
        admin_role = Role.objects.filter(rolename="超级管理员").first()
        reporter_role = Role.objects.filter(rolename="reporter").first()
        if admin_role in login_user.user_role.all() or reporter_role in login_user.user_role.all():
            pj_list = [pj_obj.project_name for pj_obj in Projects.objects.all()]
        else:
            mem_user_list = [[pj_obj.members.all(), pj_obj.project_name] for pj_obj in Projects.objects.all()]
            pj_list_m = [pj_name for m_user, pj_name in mem_user_list if login_user in m_user]

            deal_user_list = [[pj_obj.deal_user.all(), pj_obj.project_name] for pj_obj in Projects.objects.all()]
            pj_list_d = [pjname for d_user, pjname in deal_user_list if login_user in d_user]

            pj_list = list(set(pj_list_m + pj_list_d))
    return pj_list


def format_string(init_str):
    if init_str:
        return str(init_str).strip().replace("\n", "").replace(" ", "")
    else:
        return init_str


def iter_headings(paragraphs):
    for paragraph in paragraphs:
        if paragraph.style.name.startswith('Heading'):
            yield paragraph


def title_deal(file_mulu):
    doc = docx.Document(file_mulu)
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    p1 = re.compile(r'\d.*\.\d+', re.S)  # 替换该正则匹配到的字符串
    title_list = []
    for heading in iter_headings(doc.paragraphs):
        if heading.style.name == "Heading 1":
            t1 += 1
            t2 = 0
            t3 = 0
            t4 = 0
            biaoti = str(t1)
        elif heading.style.name == 'Heading 2':
            t2 = t2 + 1
            biaoti = str(t1) + "." + str(t2)
            t3 = 0
        elif heading.style.name == 'Heading 3':
            t3 = t3 + 1
            biaoti = str(t1) + "." + str(t2) + "." + str(t3)
            t4 = 0
        elif heading.style.name == 'Heading 4':
            t4 = t4 + 1
            biaoti = str(t1) + "." + str(t2) + "." + str(t3) + "." + str(t4)
        else:
            continue
        if not re.findall(p1, heading.text):
            heading.text = biaoti + heading.text
        else:
            heading.text = re.sub(p1, biaoti, heading.text)
        title_list.append(heading.text)
    title_list = [tt.strip().replace("\n", "") for tt in title_list]
    return title_list


def quarter_judge(date_str):
    quarter_dic_new = {"01,02,03": "第四季度", "04,05,06": "第一季度", "07,08,09": "第二季度", "1,2,3": "第四季度", "4,5,6": "第一季度",
                       "7,8,9": "第二季度"}
    date_list = date_str.split("-")
    quarter_final = "第三季度"
    for k in quarter_dic_new:
        if str(date_list[1]) in k:
            quarter_final = quarter_dic_new[k]
            break
    return str(date_list[0]) + "年" + quarter_final


def xuanxing_date_all():
    xx_date_list = list(XuanXingRank.objects.values_list('date', flat=True))
    zx_date_list = list(ZhuangXiangRank.objects.values_list('date', flat=True))
    cs_date_list = list(ChushiRank.objects.values_list('date', flat=True))
    date_all = list(set(xx_date_list + zx_date_list + cs_date_list))
    quarter_all = [quarter_judge(dt) for dt in date_all if dt]
    return quarter_all

# Title.objects.filter(id__startswith='12345')


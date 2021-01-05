# -*- coding:utf-8 -*-
from django.utils.encoding import escape_uri_path
from django.shortcuts import render, HttpResponse, redirect
from document.models import Doc
from testm.models import Projects
from xuanxing.models import ProductsDetail
import os
from django.http import JsonResponse
from django.http import FileResponse
from document.models import Doc
from document.models import Doc_log
from xuanxing.models import ManageUser
from xuanxing.models import ProjectDaily
# from document.models import ProjectDaily

import os
import json
import datetime
import time


def document_check(request):
    pro_obj = Projects.objects.all()
    venv_obj = ProductsDetail.objects.all()

    pro_name = request.GET.get("pro_name")
    vend_name = request.GET.get("vend_name")
    flag = request.GET.get("flag")
    print(pro_name, vend_name, flag, "--c--doc长")
    if pro_name and vend_name:
        return render(request, "doc_t/document_check.html", {
            "pro_name": pro_name,
            "vend_name": vend_name,
            "flag": flag,
            "pro_obj": pro_obj,
            # "pj_list":pj_list,
            "venv_obj": venv_obj,
            "stat": Doc.stat,
        })

    return render(request, "doc_t/document_check.html", {
        "pro_obj": pro_obj,
        "venv_obj": venv_obj,
        "stat": Doc.stat
    })


def get_ven_c(request):
    recv_data = request.POST.dict()
    pro_name = recv_data.get("pro_name", "")
    print(pro_name, "pro_name+++++++")
    vend_name = recv_data.get("vend_name", "")
    print(vend_name,"vend_name++++++++")
    flag = recv_data.get("flag", "")
    print(flag,type(flag),"=======flag=======")

    # 建立上传文件的文件夹----分类存储文件
    # def make_dir():
    #     p = os.getcwd()+"/"+"doc"
    #     dirs = os.listdir(p)
    #     if pro_name in dirs:
    #         print(pro_name)
    #         vs = os.listdir( p + "/" + pro_name )
    #         print(vs, 89)
    #         if vend_name in vs:
    #             print(vend_name)
    #         else:
    #             os.makedirs(p + "/" + pro_name + "/" + vend_name)
    #     else:
    #         os.makedirs(p + "/" + pro_name + "/" + vend_name)


    ess_list = ["公司营业执照", "法人代表授权书", "公司承诺与声明", "参测产品承诺书", "中国建设银行产品选型测评纪律", "公司承诺书", "测试案例", "软件著作权证书"]

    if flag == "1" and pro_name:
        pro_obj = Projects.objects.filter(project_name=pro_name).first()
        p_id = pro_obj.id
        v_obj = Doc.objects.filter(vend_name=vend_name,pro_name=pro_name)
        v_name_list = [v.vend_name for v in v_obj]

        doc_obj_all=""
        vend_list = [v.vend_name for v in pro_obj.vend_prod.all()]
        if pro_obj:

            if vend_name and vend_name not in  v_name_list and vend_name in vend_list:

                print("前")
                for ess in ess_list:
                    upname=vend_name+"_"+ess+'.pdf'
                    print(upname)
                    Doc.objects.create(file_name=ess,upload_filename=upname,flag=1,pro_id_id=p_id,pro_name=pro_name,vend_name=vend_name)
                doc_obj_all=[{"file_name":d.file_name,"upload_filename":d.upload_filename,"filesize":d.filesize,"status":d.get_status_display(),"id":d.id,"remark":d.remark,"check_remark": d.check_remark,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in Doc.objects.filter(vend_name=vend_name,pro_name=pro_name,flag=1)]
                # make_dir()

            # 存储了之后再次选择时显示数据库中内容

            elif vend_name and vend_name in v_name_list and vend_name in vend_list:
                print("后")
                doc_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,"status":d.get_status_display(),"id":d.id,"remark":d.remark,"check_remark": d.check_remark,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time }
                               for d in Doc.objects.filter(vend_name=vend_name,pro_name=pro_name,flag=1)]
                # make_dir()

            return JsonResponse({"code": "0000",
                                 "vend_list": vend_list,
                                 "doc_obj_all": doc_obj_all,
                                 })

    return JsonResponse({"code": "0000"})


#厂商其他文件上传
file_path_other = ""
def get_ven_other_c(request):
    recv_data = request.POST.dict()
    pro_name = recv_data.get("pro_name", "")
    print(pro_name, " pro_name3+++++++")
    vend_name = recv_data.get("vend_name", "")
    print(vend_name, " vend_name3++++++++")
    flag = recv_data.get("flag", "")
    print(flag, type(flag), "=======flag3=======")

    other_list = ["其他文件"]

    if flag == "3" and pro_name:
        pro_obj = Projects.objects.filter(project_name=pro_name).first()
        p_id = pro_obj.id
        v_obj = Doc.objects.filter(vend_name=vend_name, pro_name=pro_name)
        v_name_list = [v.vend_name for v in v_obj]


        if pro_obj:
            vend_list = [v.vend_name for v in pro_obj.vend_prod.all()]
            other_obj_all = ""

            if vend_name and vend_name not in v_name_list and vend_name in vend_list:
                for other in other_list:
                    # upname="pdf格式文件"
                    Doc.objects.create(file_name=other,flag=3, pro_id_id=p_id, pro_name=pro_name,
                                       vend_name=vend_name)
                    other_obj_all = [
                        {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,
                         "status": d.get_status_display(), "id": d.id, "remark": d.remark,"vend_name":d.vend_name,"pro_name":pro_name,"check_remark": d.check_remark,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in
                        Doc.objects.filter(vend_name=vend_name, pro_name=pro_name,flag=3)]
                #make_dir()


            # 存储了之后再次选择时显示数据库中内容
            elif vend_name and vend_name in v_name_list and vend_name in vend_list:
                print("再次显示其他内容===333=========")
                other_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,
                                "status": d.get_status_display(), "id": d.id, "remark": d.remark,"vend_name":d.vend_name,"pro_name":pro_name,"check_remark": d.check_remark,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time}
                               for d in Doc.objects.filter(vend_name=vend_name, pro_name=pro_name,flag=3)]

            return JsonResponse({"code": "0000",
                                 "vend_list": vend_list,
                                 "other_obj_all":other_obj_all,
                                 })

    return JsonResponse({"code": "0000"})

# 审核人添加备注页面
def check_add_mark(request):
    if request.method == "GET":
        m_id = request.GET.get("m_id")
        obj = Doc.objects.filter(id=m_id).first()
        pro_name = obj.pro_name
        vend_name = obj.vend_name
        flag = obj.flag
        check_remark=obj.check_remark
        print(pro_name, vend_name, flag,"==c==")
        return render(request, "doc_t/check_add_mark.html", {"m_id": m_id,"pro_name":pro_name,"vend_name":vend_name,"flag":flag,"check_remark":check_remark})

    if request.method == "POST":
        myadd = request.POST.get("myadd")
        print(myadd)
        m_id = request.POST.get("m_id")
        print(m_id)
        pro_name = request.POST.get("pro_name")
        print(pro_name,66)
        vend_name = request.POST.get("vend_name")
        print(vend_name,77)
        flag = request.POST.get("flag")
        print(flag)
        id_obj = Doc.objects.filter(id=int(m_id))
        print(myadd, m_id, 888)
        id_obj.update(check_remark=myadd)
        return JsonResponse({"code": "0000","pro_name":pro_name,"vend_name":vend_name,"flag":flag})


#纪要备注
def jy_add_mark(request):
    if request.method == "GET":
        m_id = request.GET.get("m_id")
        print(m_id,"mmm--------")
        obj = ProjectDaily.objects.filter(id=m_id).first()
        pro_id = obj.pj_id_id
        check_mark = obj.check_mark
        print(pro_id ,678)
        p_obj = Projects.objects.filter(id = pro_id).first()
        pro_name=p_obj.project_name
        print(pro_name)
        return render(request, "doc_t/jy_mark.html", {"m_id": m_id,"pro_name":pro_name,"check_mark":check_mark})

    if request.method == "POST":
        myadd = request.POST.get("myadd")
        print(myadd)
        m_id = request.POST.get("m_id")
        print(m_id)
        pro_name = request.POST.get("pro_name")
        print(pro_name,"jy")
        id_obj = ProjectDaily.objects.filter(id=int(m_id))
        print(myadd, m_id, "888jy-------")
        id_obj.update(check_mark=myadd)
        return JsonResponse({"code": "0000","pro_name":pro_name})

# def get_ven_c(request):
#     recv_data = request.POST.dict()
#     pro_name = recv_data.get("pro_name", "")
#     print(pro_name, " pro_name+++++++")
#     vend_name = recv_data.get("vend_name", "")
#     print(vend_name, " vend_name++++++++")
#     flag = recv_data.get("flag", "")
#     print(flag, type(flag), "=======flag=======")
#
#     # 建立上传文件的文件夹----分类存储文件
#     def make_dir():
#         p = os.getcwd() + "/" + "doc"
#         dirs = os.listdir(p)
#         if pro_name in dirs:
#             print(pro_name)
#             vs = os.listdir(p + "/" + pro_name)
#             print(vs, 89)
#             if vend_name in vs:
#                 print(vend_name)
#             else:
#                 os.makedirs(p + "/" + pro_name + "/" + vend_name)
#         else:
#             os.makedirs(p + "/" + pro_name + "/" + vend_name)
#
#     ess_list = ["公司营业执照", "法人代表授权书", "公司承诺与声明", "参测产品承诺书", "中国建设银行产品选型测评纪律", "公司承诺书", "测试案例", "软件著作权证书"]
#
#     if flag == "1" and pro_name:
#         pro_obj = Projects.objects.filter(project_name=pro_name).first()
#         p_id = pro_obj.id
#         doc_pro_id = Doc.objects.filter(pro_id_id=p_id, flag=flag)
#         vend_obj = ProductsDetail.objects.filter(vend_name=vend_name).first()
#         print(vend_obj)
#         product_obj = ProductsDetail.objects.filter(product_name=vend_obj).first()
#         print(product_obj.id, "%%%%%%%%")
#         v_id = product_obj.id
#         doc_vend_id = Doc.objects.filter(vend_id_id=product_obj)
#         print(doc_vend_id)
#
#         if pro_obj:
#             vend_list = [v.vend_name for v in pro_obj.vend_prod.all()]
#             print(vend_list, "++++++++++vend_list")
#             # doc_li = []
#             doc_obj_all = ""
#             # 点击下拉框 1 厂商文件， 选择了厂商，查询数据库，看里面是否有项目id 或者厂商id外键
#             # 注意一个项目有多家厂商的情况
#
#             if vend_obj and (not doc_pro_id or not doc_vend_id):
#                 for ess in ess_list:
#                     upname = vend_name + "_" + ess + '.pdf'
#                     print(upname)
#                     Doc.objects.create(file_name=ess, upload_filename=upname, flag=1, pro_id_id=p_id, pro_name=pro_name,
#                                        vend_name=vend_name, vend_id_id=v_id)
#                     # doc_obj_all=[{"file_name":d.file_name,"upload_filename":d.upload_filename,"filesize":d.filesize,"status":d.status,"id":d.id} for d in Doc.objects.filter(pro_id_id=p_id,vend_name=vend_name,pro_name=pro_name)]
#                 doc_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,
#                                 "status": d.get_status_display(), "id": d.id, "remark": d.remark,
#                                 "check_remark": d.check_remark} for d in
#                                Doc.objects.filter(vend_name=vend_name, pro_name=pro_name, flag=1)]
#                 make_dir()
#
#             # 存储了之后再次选择时显示数据库中内容
#             elif vend_obj and doc_vend_id and doc_pro_id:
#
#                 doc_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,
#                                 "status": d.get_status_display(), "id": d.id, "remark": d.remark,
#                                 "check_remark": d.check_remark}
#                                for d in Doc.objects.filter(vend_name=vend_name, pro_name=pro_name, flag=1)]
#                 make_dir()
#
#             return JsonResponse({ "code": "0000",
#                                   "vend_list": vend_list,
#                                   "doc_obj_all": doc_obj_all,
#                                  })
#
#     return JsonResponse({"code": "0000"})


# 厂商其他文件上传




# file_path_other = ""
# def get_ven_other_c(request):
#     recv_data = request.POST.dict()
#     pro_name = recv_data.get("pro_name", "")
#     print(pro_name, " pro_name3+++++++")
#     vend_name = recv_data.get("vend_name", "")
#     print(vend_name, " vend_name3++++++++")
#     flag = recv_data.get("flag", "")
#     print(flag, type(flag), "=======flag3=======")
#
#     other_list = ["1", "2", "3", "4", "5"]
#
#     if flag == "3" and pro_name:
#         pro_obj = Projects.objects.filter(project_name=pro_name).first()
#         p_id = pro_obj.id
#         doc_pro_id = Doc.objects.filter(pro_id_id=p_id, flag=flag)
#
#         vend_obj = ProductsDetail.objects.filter(vend_name=vend_name).first()
#         print(vend_obj)
#         product_obj = ProductsDetail.objects.filter(product_name=vend_obj).first()
#         print(product_obj.id, "%%%%%%%%")
#         v_id = product_obj.id
#         doc_vend_id = Doc.objects.filter(vend_id_id=product_obj)
#         print(doc_vend_id)
#
#         if pro_obj:
#             vend_list = [v.vend_name for v in pro_obj.vend_prod.all()]
#             print(vend_list, "+++other++vend_list")
#             # doc_li = []
#             other_obj_all = ""
#             # 点击下拉框 1 厂商文件， 选择了厂商，查询数据库，看里面是否有项目id 或者厂商id外键
#             # 注意一个项目有多家厂商的情况
#
#             if vend_obj and (not doc_pro_id or not doc_vend_id):
#                 for other in other_list:
#                     # upname="pdf格式文件"
#                     Doc.objects.create(file_name=other, flag=3, pro_id_id=p_id, pro_name=pro_name,
#                                        vend_name=vend_name, vend_id_id=v_id)
#                     # doc_obj_all=[{"file_name":d.file_name,"upload_filename":d.upload_filename,"filesize":d.filesize,"status":d.status,"id":d.id} for d in Doc.objects.filter(pro_id_id=p_id,vend_name=vend_name,pro_name=pro_name)]
#                     other_obj_all = [
#                         {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,
#                          "status": d.get_status_display(), "id": d.id, "remark": d.remark, "vend_name": d.vend_name,
#                          "pro_name": pro_name, "check_remark": d.check_remark} for d in
#                         Doc.objects.filter(vend_name=vend_name, pro_name=pro_name, flag=3)]
#                 # make_dir()
#
#
#             # 存储了之后再次选择时显示数据库中内容
#             elif vend_obj and doc_vend_id and doc_pro_id:
#                 print("再次显示其他内容===333=========")
#                 other_obj_all = [
#                     {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,
#                      "status": d.get_status_display(), "id": d.id, "remark": d.remark, "vend_name": d.vend_name,
#                      "pro_name": pro_name, "check_remark": d.check_remark}
#                     for d in Doc.objects.filter(vend_name=vend_name, pro_name=pro_name, flag=3)]
#                 # make_dir()
#
#             return JsonResponse({"code": "0000",
#                                  "vend_list": vend_list,
#                                  "other_obj_all": other_obj_all,
#                                  })
#
#     return JsonResponse({"code": "0000"})




# 上传
# def upload_file(request):
#     if request.method == "POST":
#         myFile = request.FILES.get("myfile")
#         f_code = request.POST.get("f_code")
#         other_vend_name = request.POST.get("other_vend_name")
#         print(other_vend_name)
#         other_pro_name = request.POST.get("other_pro_name")
#         flag = request.POST.get("flag")
#         print(flag, type(flag), "=====myflag333====")
#         print(other_pro_name)
#         print(f_code, "=======mycode=========")
#         print(myFile, "=======myFile=========")
#         filesize = myFile.size / 1024
#
#         if not myFile:
#             return HttpResponse("no files for upload!")
#
#         name_obj = Doc.objects.filter(upload_filename=myFile.name)
#         code_obj = Doc.objects.filter(file_name=f_code, vend_name=other_vend_name)
#         print(name_obj, "====99999999999")
#         file_id = ""
#         now_time = datetime.datetime.today()
#         if name_obj and flag != "3":
#             # 查询数据库中文件状态
#             name_obj.update(filesize=filesize)
#             name_obj.update(create_time=now_time)
#             file_id = name_obj[0].id
#             vend_name = name_obj[0].vend_name
#             print(vend_name, "===========path========")
#             pro_name = name_obj[0].pro_name
#             time_str = name_obj[0].create_time
#             print(time_str)
#             flag = name_obj[0].flag
#             s_time = time.mktime(time_str.timetuple())
#             print(s_time, "=========上传时间=12=======")
#
#             if flag == 1:
#                 print("-----------ess上传------------------")
#                 destination = open(os.path.join("doc", pro_name, vend_name, str(s_time) + '_' + myFile.name),
#                                    'wb+')  # 打开特定的文件进行二进制的写操作
#                 for chunk in myFile.chunks():  # 分块写入文件
#                     file = destination.write(chunk)
#                 destination.close()
#                 name_obj.update(status=2)
#
#             elif flag == 2:
#                 print("-----------pub上传------------------")
#                 destination = open(os.path.join("doc", pro_name, "pub", str(s_time) + '_' + myFile.name), 'wb+')
#                 for chunk in myFile.chunks():  # 分块写入文件
#                     file = destination.write(chunk)
#                 destination.close()
#                 name_obj.update(status=2)
#
#             stat_obj = name_obj[0].status
#             print(stat_obj, "========s_obj")
#
#             # 文档日志
#             op_file = "上传了" + name_obj[0].upload_filename
#             opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#             Doc_log.objects.create(s_time=name_obj[0].create_time, operation=op_file, user_id=opt_usr)
#
#             return JsonResponse({"code": "0000", "file_id": file_id, "stat_obj": stat_obj})
#
#         if name_obj and flag == "3":
#
#             s_time = time.mktime(now_time.timetuple())
#             # print(s_time, "=========上传时间3========")
#             p = os.getcwd() + "/" + "doc"
#             dirs = os.listdir(p)
#             if other_pro_name in dirs:
#                 print(other_pro_name)
#                 vs = os.listdir(p + "/" + other_pro_name)
#                 print(vs, 89)
#                 if other_vend_name + "_other" in vs:
#                     print(other_vend_name)
#                 else:
#                     os.makedirs(p + "/" + other_pro_name + "/" + other_vend_name + "_other")
#             else:
#                 os.makedirs(p + "/" + other_pro_name + "/" + other_vend_name + "_other")
#
#             other_path = os.path.join("doc", other_pro_name, other_vend_name + "_other",
#                                       str(s_time) + '_' + myFile.name)
#             destination = open(other_path, 'wb+')
#             for chunk in myFile.chunks():  # 分块写入文件
#                 file = destination.write(chunk)
#             destination.close()
#             code_obj.update(filesize=filesize)
#             code_obj.update(upload_filename=myFile)
#             code_obj.update(status=2)
#             stat_obj = name_obj[0].status
#             # 文档日志
#             op_file = "上传了" + code_obj[0].upload_filename
#             opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#             Doc_log.objects.create(s_time=code_obj[0].create_time, operation=op_file, user_id=opt_usr)
#             return JsonResponse({"code": "0000", "file_id": file_id, "stat_obj": stat_obj})
#
#         elif not name_obj:
#             stat_obj = code_obj[0].status
#             file_id = code_obj[0].id
#             flag = code_obj[0].flag
#             print(flag, "------------")
#             vend_name = code_obj[0].vend_name
#             pro_name = code_obj[0].pro_name
#             time_str = code_obj[0].create_time
#             s_time = time.mktime(time_str.timetuple())
#             print(stat_obj, "===*****=====s_obj")
#             if flag == 3:
#                 p = os.getcwd() + "/" + "doc"
#                 dirs = os.listdir(p)
#                 if pro_name in dirs:
#                     print(pro_name)
#                     vs = os.listdir(p + "/" + pro_name)
#                     print(vs, 89)
#                     if vend_name + "_other" in vs:
#                         print(vend_name)
#                     else:
#                         os.makedirs(p + "/" + pro_name + "/" + vend_name + "_other")
#                 else:
#                     os.makedirs(p + "/" + pro_name + "/" + vend_name + "_other")
#
#                 print(888)
#                 other_path = os.path.join("doc", pro_name, vend_name + "_other", str(s_time) + '_' + myFile.name)
#                 # other_path= os.getcwd() + "/" + "doc"+"/"+pro_name+"/"+vend_name+"_other"
#                 # if other_path:
#                 destination = open(other_path, 'wb+')  # 打开特定的文件进行二进制的写操作
#                 for chunk in myFile.chunks():  # 分块写入文件
#                     file = destination.write(chunk)
#                 destination.close()
#                 code_obj.update(filesize=filesize)
#                 code_obj.update(upload_filename=myFile)
#                 code_obj.update(status=2)
#                 stat_obj = code_obj[0].status
#                 print(stat_obj, "========s_obj")
#                 # 文档日志
#                 op_file = "上传了" + code_obj[0].upload_filename
#                 opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#                 Doc_log.objects.create(s_time=code_obj[0].create_time, operation=op_file, user_id=opt_usr)
#             return JsonResponse({"code": "0000", "file_id": file_id, "stat_obj": stat_obj})
#
#     return render(request, "doc_t/document_check.html")
#
#
# # 下载
# # 得到下载的路径
# def download_file(request):
#     if request.method == "POST":
#         file_id = request.POST.get("file_id", "")
#         flag = request.POST.get("flag", "")
#         print(flag, 888888)
#         obj_id = Doc.objects.filter(id=file_id)
#         file_name = obj_id[0].upload_filename
#         vend_name = obj_id[0].vend_name
#         print(vend_name)
#         pro_name = obj_id[0].pro_name
#         print(pro_name)
#         create_time = obj_id[0].create_time
#         print(create_time)
#         s_time = time.mktime(create_time.timetuple())
#         print(s_time, "===========下载时间=======")
#         print(vend_name, 9999)
#
#         if flag == "1":
#             f_path = "/doc/" + pro_name + "/" + vend_name + "/" + str(s_time) + "_" + file_name
#             print(f_path)
#             return JsonResponse({"f_path": f_path})
#
#         elif flag == "2":
#             f_path = "/doc/" + pro_name + "/" + "pub" + "/" + str(s_time) + "_" + file_name
#             return JsonResponse({"f_path": f_path})
#
#
#         elif flag == "3":
#             f_path = "/doc/" + pro_name + "/" + vend_name + "_other" + "/" + str(s_time) + "_" + file_name
#             return JsonResponse({"f_path": f_path})
#
#
# # 厂商文件下载
# def down_load(request):
#     print("进来下载")
#     path_obj = request.GET.get("file_path")
#     print(path_obj)
#     print(os.getcwd() + path_obj)
#     with open(os.getcwd() + path_obj, 'rb') as f:
#         response = HttpResponse(f.read(), content_type="application/octet-stream")
#         response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
#             escape_uri_path(path_obj.split("/")[-1]))
#         # 文档日志
#         op_file = "下载了" + path_obj.split("/")[-1]
#         opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#         Doc_log.objects.create(operation=op_file, user_id=opt_usr)
#         return response


# 下载的第二种方法
# file = open(os.getcwd()+path_obj, 'rb')
# print(file)
# # try:
# response = FileResponse(file)
# print(response)
# response['Content-Type'] = 'application/octet-stream'
# print(path_obj.split("/")[-1])
# response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(path_obj.split("/")[-1])
# print(response, 555)
# # except:
# #     return HttpResponse("Sorry but Not Found the File")
# return response


# 添加厂商文件页面
# def doc_add(request):
#     if request.method == "GET":
#         pro_name = request.GET.get("pro_add", "")
#         vend_name = request.GET.get("vend_add", "")
#         flag = request.GET.get("flag", "")
#
#         return render(request, "doc_t/doc_add.html", {"pro_name": pro_name, "vend_name": vend_name, "flag": flag})
#
#     if request.method == "POST":
#         myadd = request.POST.get("myadd", "")
#         pro_name = request.POST.get("pro_name", "")
#         vend_name = request.POST.get("vend_name", "")
#         flag = request.POST.get("flag")
#         print(flag, "---------flag===========")
#         add_obj = Doc.objects.filter(file_name=myadd)
#         # 必要文件
#         if myadd and pro_name and vend_name and flag != "3" and not add_obj:
#             print(1111)
#             up_name = vend_name + "_" + myadd + ".pdf"
#             Doc.objects.create(file_name=myadd, pro_name=pro_name, vend_name=vend_name, flag=flag,
#                                upload_filename=up_name)
#             return JsonResponse({"code": "0000"})
#
#         # 公共文件
#         elif myadd and pro_name and flag != "3" and not add_obj:
#             print(222)
#             up_name = pro_name + "_" + myadd + ".pdf"
#             Doc.objects.create(file_name=myadd, pro_name=pro_name, flag=flag, upload_filename=up_name)
#             return JsonResponse({"code": "0000"})
#
#         # 其他文件
#         elif myadd and pro_name and vend_name and flag == "3" and not add_obj:
#             print(3333)
#             Doc.objects.create(file_name=myadd, pro_name=pro_name, vend_name=vend_name, flag=flag)
#
#             return JsonResponse({"code": "0000"})
#
#         elif add_obj:
#             return JsonResponse({"code": "0001"})
#         else:
#             return JsonResponse({"code": "0002"})


# # 修改文件名字页面
# def change_name(request):
#     if request.method == "GET":
#         f_id = request.GET.get("f_id")
#         f_obj = Doc.objects.get(id=f_id)
#         up_name = f_obj.upload_filename
#         print(f_id, up_name, 999)
#         return render(request, "doc_t/change_name.html", {"f_id": f_id, "up_name": up_name})
#
#     if request.method == "POST":
#         mychange = request.POST.get("mychange")
#         print(mychange)
#         f_id = request.POST.get("f_id")
#         print(f_id)
#         id_obj = Doc.objects.filter(id=int(f_id))
#         print(mychange, f_id, 888)
#         id_obj.update(upload_filename=mychange)
#         return JsonResponse({"code": "0000"})


# def stat_change(request):
#     recv_data = request.POST.dict()
#     type_name = recv_data.get("type_name")
#     print(type_name)
#     status = recv_data.get("change_status")  # 数字状态
#     print(status, "状态============")
#     change_id = recv_data.get("change_id")  # 文件id
#     print(change_id)
#     change_obj = ""
#     filename = ""
#     if type_name == "ess":
#         change_obj = Doc.objects.filter(id=int(change_id)).first()
#
#     elif type_name == "pub":
#         change_obj = Doc.objects.filter(id=int(change_id)).first()
#
#     elif type_name == "other":
#         change_obj = Doc.objects.filter(id=int(change_id)).first()
#
#     # print(s[1],111)
#     filename = change_obj.upload_filename
#     old_stat = change_obj.status
#
#     if change_obj:
#         change_obj.status = str(status)
#         change_obj.save()
#
#         # 文档日志
#         d = Doc(status=old_stat)
#         old_s = d.get_status_display()
#         d1 = Doc(status=int(status))
#         new_s = d1.get_status_display()
#         # op_file = filename+ "状态:"+ str(old_stat) + "===>" + status
#         op_file = "<" + filename + ">" + " 状态 : " + old_s + "===>" + new_s
#         opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#         Doc_log.objects.create(operation=op_file, user_id=opt_usr)
#
#     return JsonResponse({"code": "0000", "stat": change_obj.status, "change_id": change_id})


# # 上传人添加备注页面
# def add_mark(request):
#     if request.method == "GET":
#         m_id = request.GET.get("m_id")
#         print(m_id, 7777)
#         return render(request, "doc_t/add_mark.html", {"m_id": m_id})
#
#     if request.method == "POST":
#         myadd = request.POST.get("myadd")
#         print(myadd)
#         m_id = request.POST.get("m_id")
#         print(m_id)
#         check = request.POST.get("check")
#         id_obj = Doc.objects.filter(id=int(m_id))
#         print(myadd, m_id, 888)
#         id_obj.update(remark=myadd)
#         # 文档日志
#         obj = id_obj.first()
#         old_stat = obj.get_status_display()
#         file_name = obj.upload_filename
#         if check:
#             id_obj.update(status=5)
#             new_obj = Doc.objects.filter(id=int(m_id)).first()
#             new_stat = new_obj.get_status_display()
#
#             op_file = "<<" + file_name + ">>" + " 状态 : " + old_stat + " ===> " + new_stat
#             opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#             print("++++++改变不涉及")
#             Doc_log.objects.create(operation=op_file, user_id=opt_usr)
#         return JsonResponse({"code": "0000"})




# # 公共文件部分
# def get_pub(request):
#     recv_data = request.POST.dict()
#     pub_pro_name = recv_data.get("pub_pro_name", "")
#     print(pub_pro_name, " pub_pro_name================")
#     flag = recv_data.get("flag", "")
#     print(flag, type(flag), "=======flag=======")
#
#     def make_dir():
#         p = os.getcwd() + "/" + "doc"
#         dirs = os.listdir(p)
#         if pub_pro_name in dirs:
#             print(pub_pro_name)
#             vs = os.listdir(p + "/" + pub_pro_name)
#             if "pub" in vs:
#                 print("已存在")
#             else:
#                 os.makedirs(p + "/" + pub_pro_name + "/" + "pub")
#
#     pub_list = ["启动会签到表", "监督小组巡视记录", "测试人员签到表", "每日例行操作检查表", "调试完成报告", "测试录像视频", "上会材料PPT"]
#     pub_list1 = ["启动会签到表", "监督小组巡视记录", "测试人员签到表", "每日例行操作检查表", "调试完成报告", "测试录像视频"]
#
#     if flag == "2" and pub_pro_name:
#         print("进来2")
#         pro_obj = Projects.objects.filter(project_name=pub_pro_name).first()
#         p_id = pro_obj.id
#         # 查看上会状态
#         pro_stat = pro_obj.meeting_status
#         pub_obj = Doc.objects.filter(pro_id_id=p_id, flag=flag).first()
#
#         # 会议纪要
#         pd_obj = ProjectDaily.objects.filter(pj_id_id=p_id)
#
#         if pro_stat == "1":  # 上会  ppt有显示
#             if not pub_obj:
#                 print("没有")
#                 for pub in pub_list:
#                     upname = pub_pro_name + "_" + pub + '.pdf'
#                     Doc.objects.create(file_name=pub, upload_filename=upname, flag=2, pro_id_id=p_id,
#                                        pro_name=pub_pro_name)
#                     print("写入")
#
#                 pub_obj_all = [
#                     {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize, "id": d.id,
#                      "status": d.get_status_display(), "remark": d.remark, "check_remark": d.check_remark} for d in
#                     Doc.objects.filter(pro_name=pub_pro_name, flag=2, pro_id_id=p_id)]
#
#                 make_dir()
#
#                 pd_list = [{"file_name": pd.file_name, "type": pd.type, "up_time": pd.up_time.strftime('%Y-%m-%d'),
#                             "mark": pd.mark} for pd in pd_obj]
#                 print(pd_list, "------------会议纪要")
#             else:
#                 # 存储了之后再次选择时显示数据库中内容
#                 print("有内容123")
#                 pub_obj_all = [
#                     {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize, "id": d.id,
#                      "status": d.get_status_display(), "remark": d.remark, "check_remark": d.check_remark} for d in
#                     Doc.objects.filter(pro_name=pub_pro_name, flag=2, pro_id_id=p_id)]
#
#                 make_dir()
#
#                 pd_list = [{"file_name": pd.file_name, "type": pd.type, "up_time": pd.up_time.strftime('%Y-%m-%d'),
#                             "mark": pd.mark} for pd in pd_obj]
#                 print(pd_list, "------------会议纪要")
#
#             return JsonResponse({"code": "0000",
#                                  "pub_obj_all": pub_obj_all,
#                                  "pd_list": pd_list,
#                                  })
#
#         elif pro_stat == "0":  # 不上会的
#             if not pub_obj:
#                 print("没有")
#                 for pub in pub_list1:
#                     upname = pub_pro_name + "_" + pub + '.pdf'
#                     Doc.objects.create(file_name=pub, upload_filename=upname, flag=2, pro_id_id=p_id,
#                                        pro_name=pub_pro_name)
#                     print("写入")
#                 pub_obj_all = [
#                     {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize, "d": d.id,
#                      "status": d.get_status_display(), "remark": d.remark, "check_remark": d.check_remark} for d in
#                     Doc.objects.filter(pro_name=pub_pro_name, flag=2)]
#
#                 make_dir()
#
#                 pd_list = [{"file_name": pd.file_name, "type": pd.type, "up_time": pd.up_time.strftime('%Y-%m-%d'),
#                             "mark": pd.mark} for pd in pd_obj]
#                 print(pd_list, "------------会议纪要")
#             else:
#                 # 存储了之后再次选择时显示数据库中内容
#                 print("有内容22")
#                 pub_obj_all = [
#                     {"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize, "id": d.id,
#                      "status": d.get_status_display(), "remark": d.remark, "check_remark": d.check_remark} for d in
#                     Doc.objects.filter(pro_name=pub_pro_name, flag=2)]
#
#                 print(pub_obj_all[0]["file_name"])
#                 make_dir()
#                 pd_list = [{"file_name": pd.file_name, "type": pd.type, "up_time": pd.up_time.strftime('%Y-%m-%d'),
#                             "mark": pd.mark} for pd in pd_obj]
#                 print(pd_list, "------------会议纪要")
#
#             return JsonResponse({"code": "0000",
#                                  "pub_obj_all": pub_obj_all,
#                                  "pd_list": pd_list,
#                                  })
#
#     return JsonResponse({"code": "0001"})
#
#
# def doc_log(request):
#     user = ManageUser.objects.filter(id=int(request.session.get("user_id", ""))).first()
#
#     log_list = []
#     if user:
#         log_list = [
#             [log_obj.s_time, log_obj.user_id.user_role.all().first(), log_obj.user_id.username, log_obj.operation]
#             for log_obj in Doc_log.objects.all() if log_obj.user_id == user]
#
#     return render(request, "doc_t/doc_log.html", {"log_list": log_list})
#
#
# def check_pass(request):
#     recv_data = request.POST.dict()
#     pass_id = recv_data.get("pass_id")
#     pass_other_id = recv_data.get("pass_other_id")
#     pass_pub_id = recv_data.get("pass_pub_id")
#     print(pass_id)
#     # if pass_id or pass_pub_id or pass_other_id:
#     ps_id_obj = ""
#     if pass_id:
#         ps_id_obj = Doc.objects.filter(id=pass_id)
#         # pass_pub_id = Doc.objects.filter(id=pass_pub_id)
#     elif pass_other_id:
#         ps_id_obj = Doc.objects.filter(id=pass_other_id)
#         print(ps_id_obj, "===========")
#         # pass_other_id = Doc.objects.filter(id=pass_other_id)
#     elif pass_pub_id:
#         ps_id_obj = Doc.objects.filter(id=pass_pub_id)
#
#     # 文档日志
#     # 旧的 三者统一
#     ps_id_first = ps_id_obj.first()
#     old_stat = ps_id_first.status
#     file_name = ps_id_first.upload_filename
#     d = Doc(status=old_stat)
#     old_s = d.get_status_display()
#
#     ps_id_obj.update(status=3)
#
#     new_obj = ""
#     if pass_id:
#         new_obj = Doc.objects.filter(id=pass_id).first()
#     elif pass_other_id:
#         new_obj = Doc.objects.filter(id=pass_other_id).first()
#     elif pass_pub_id:
#         new_obj = Doc.objects.filter(id=pass_pub_id).first()
#
#     new_s = new_obj.get_status_display()
#
#     op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
#     opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#     print("++++++改变")
#     Doc_log.objects.create(operation=op_file, user_id=opt_usr)
#
#     return JsonResponse({"code": "0000"})
#
#
# def no_check_pass(request):
#     recv_data = request.POST.dict()
#     pass_id = recv_data.get("pass_id")
#     pass_other_id = recv_data.get("pass_other_id")
#     pass_pub_id = recv_data.get("pass_pub_id")
#     print(pass_other_id)
#     # if pass_id or pass_down_id or pass_other_id:
#     #     ps_id = Doc.objects.filter(id=pass_id)
#     #     pass_down_id = Doc.objects.filter(id=pass_down_id)
#     #     pass_other_id = Doc.objects.filter(id=pass_other_id)
#     #     if ps_id:
#     #         ps_id.update(status=4)
#     #     elif pass_other_id:
#     #         pass_other_id.update(status=4)
#     #     elif pass_down_id:
#     #         pass_down_id.update(status=4)
#
#     ps_id_obj = ""
#     if pass_id:
#         ps_id_obj = Doc.objects.filter(id=pass_id)
#         # pass_pub_id = Doc.objects.filter(id=pass_pub_id)
#     elif pass_other_id:
#         ps_id_obj = Doc.objects.filter(id=pass_other_id)
#         print(ps_id_obj, "===========")
#         # pass_other_id = Doc.objects.filter(id=pass_other_id)
#     elif pass_pub_id:
#         ps_id_obj = Doc.objects.filter(id=pass_pub_id)
#
#     # 文档日志
#     # 旧的 三者统一
#     ps_id_first = ps_id_obj.first()
#     old_stat = ps_id_first.status
#     file_name = ps_id_first.upload_filename
#     d = Doc(status=old_stat)
#     old_s = d.get_status_display()
#
#     ps_id_obj.update(status=4)
#
#     new_obj = ""
#     if pass_id:
#         new_obj = Doc.objects.filter(id=pass_id).first()
#     elif pass_other_id:
#         new_obj = Doc.objects.filter(id=pass_other_id).first()
#     elif pass_pub_id:
#         new_obj = Doc.objects.filter(id=pass_pub_id).first()
#
#     new_s = new_obj.get_status_display()
#
#     op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
#     opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
#
#     Doc_log.objects.create(operation=op_file, user_id=opt_usr)
#
#     return JsonResponse({"code": "0000"})
#
#
# # 图形展示
# def shape_show(request):
#     data = {}
#     shape_obj = Doc.objects.all()
#     shape_list = [{"value": 1, "name": s.upload_filename} for s in shape_obj]
#     print(shape_list)
#     return JsonResponse({'shape_list': shape_list})
#
#     # 最后将数据打包成json格式以字典的方式传送到前端
#     # return render(request, 'doc_t/document.html',{'shape_list': shape_list} )

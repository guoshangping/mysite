# -*- coding:utf-8 -*-
from django.utils.encoding import escape_uri_path
from django.shortcuts import render,HttpResponse,redirect
from document.models import Doc
from testm.models import Projects
from xuanxing.models import ProductsDetail
import os
from django.http import JsonResponse
from django.http import FileResponse
from document.models import Doc
from document.models import Doc_log
from xuanxing.models import  ManageUser
from xuanxing.models import  ProjectDaily
# from document.models import  ProjectDaily
from tools.tools import juge_user_pj

import os
import json
import datetime
import time

def document(request):
    # pro_obj = Projects.objects.all()
    venv_obj = ProductsDetail.objects.all()
    uid = request.session.get("user_id")
    pj_list = juge_user_pj(uid)
    print(pj_list,"**")
    pro_obj = [Projects.objects.filter(project_name=p) for p in pj_list]

    pro_name = request.GET.get("pro_name")
    vend_name = request.GET.get("vend_name")
    flag = request.GET.get("flag")
    print(pro_name,vend_name,flag,"---------doc长")
    if pro_name and vend_name:
        return render(request, "doc_t/document.html", {
            "pro_name": pro_name,
            "vend_name": vend_name,
            "flag": flag,
            "pro_obj": pro_obj,
            "venv_obj": venv_obj,
            "stat": Doc.stat,
        })
    elif pro_name and flag == "2":
        return render(request, "doc_t/document.html", {
            "pro_name": pro_name,
            "flag": flag,
            "pro_obj": pro_obj,
            "venv_obj": venv_obj,
            "stat": Doc.stat,
        })
    return render(request, "doc_t/document.html", {
                                                    "pro_obj": pro_obj,
                                                    "venv_obj": venv_obj,
                                                    "stat": Doc.stat
                                                    })

def get_ven(request):
    recv_data = request.POST.dict()
    pro_name = recv_data.get("pro_name", "")
    print(pro_name, "pro_name+++++++")
    vend_name = recv_data.get("vend_name", "")
    print(vend_name,"vend_name++++++++")
    flag = recv_data.get("flag", "")
    print(flag,type(flag),"=======flag=======")

    # 建立上传文件的文件夹----分类存储文件
    def make_dir():
        p = os.getcwd()+"/"+"doc"
        dirs = os.listdir(p)
        if pro_name in dirs:
            print(pro_name)
            vs = os.listdir( p + "/" + pro_name )
            print(vs, 89)
            if vend_name in vs:
                print(vend_name)
            else:
                os.makedirs(p + "/" + pro_name + "/" + vend_name)
        else:
            os.makedirs(p + "/" + pro_name + "/" + vend_name)


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

                doc_obj_all=[{"file_name":d.file_name,"upload_filename":d.upload_filename,"filesize":d.filesize,"status":d.get_status_display(),"id":d.id,"remark":d.remark,"check_remark": d.check_remark,"pro_name":d.pro_name,"vend_name":d.vend_name,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in Doc.objects.filter(vend_name=vend_name,pro_name=pro_name,flag=1)]
                p=[{"create_time":time.mktime(d.create_time.timetuple())} for d in Doc.objects.filter(vend_name=vend_name,pro_name=pro_name,flag=1)]
                print(p,"create tiem pass+++++++++++++++++++++++++++")
                make_dir()

            # 存储了之后再次选择时显示数据库中内容
            elif vend_name and vend_name in  v_name_list and vend_name in vend_list:
                print("后")
                doc_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,"status":d.get_status_display(),"id":d.id,"remark":d.remark,"check_remark": d.check_remark,"pro_name":d.pro_name,"vend_name":d.vend_name,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time }
                               for d in Doc.objects.filter(vend_name=vend_name,pro_name=pro_name,flag=1)]
                make_dir()

            return JsonResponse({"code": "0000",
                                 "vend_list": vend_list,
                                 "doc_obj_all": doc_obj_all,
                                 })

    return JsonResponse({"code": "0000"})


#厂商其他文件上传
file_path_other = ""
def get_ven_other(request):
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

        other_obj_all = ""
        vend_list = ""

        if pro_obj:
            vend_list = [v.vend_name for v in pro_obj.vend_prod.all()]
            print(vend_list, "+++other++vend_list")
            # doc_li = []
            other_obj_all = ""
            # 点击下拉框 1 厂商文件， 选择了厂商，查询数据库，看里面是否有项目id 或者厂商id外键
            # 注意一个项目有多家厂商的情况

            if vend_name and vend_name not in v_name_list and vend_name in vend_list:
                for other in other_list:
                    # upname="pdf格式文件"
                    Doc.objects.create(file_name=other,flag=3, pro_id_id=p_id, pro_name=pro_name,
                                       vend_name=vend_name)
                    # doc_obj_all=[{"file_name":d.file_name,"upload_filename":d.upload_filename,"filesize":d.filesize,"status":d.status,"id":d.id} for d in Doc.objects.filter(pro_id_id=p_id,vend_name=vend_name,pro_name=pro_name)]
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

#上传
def upload_file(request):
    if request.method == "POST":
        myFile = request.FILES.get("myfile")
        f_code = request.POST.get("f_code")
        print(f_code,"fcode===========")

        vend_name = request.POST.get("vend_name")
        pro_name = request.POST.get("pro_name")
        print(vend_name,pro_name,"11111111111----")

        other_vend_name = request.POST.get("other_vend_name")
        print(other_vend_name)
        other_pro_name = request.POST.get("other_pro_name")

        flag = request.POST.get("flag")
        print(flag,type(flag),"=====myflag333111====")

        print(other_pro_name)
        print(f_code,"=======mycode=========")
        print(myFile,"=======myFile=========")
        filesize = myFile.size/1024

        if not myFile:
            return HttpResponse("no files for upload!")

        name_obj = Doc.objects.filter(upload_filename=myFile.name,pro_name=pro_name)
        code_obj = Doc.objects.filter(file_name=f_code,pro_name=other_pro_name,vend_name=other_vend_name)
        print(name_obj,"====99999999999") #厂商其他文件开始上传名字为空
        print(code_obj,"====988889999") #厂商其他文件开始上传名字为空
        file_id = ""
        now_time = datetime.datetime.today()
        #必要和公共文件上传
        if name_obj and flag != "3":
            # 查询数据库中文件状态
            name_obj.update(filesize=filesize)
            name_obj.update(create_time=now_time)
            file_id = name_obj[0].id
            vend_name = name_obj[0].vend_name
            print(vend_name, "===========path========")
            pro_name = name_obj[0].pro_name
            time_str = name_obj[0].create_time
            print(time_str)
            flag = name_obj[0].flag
            s_time = time.mktime(time_str.timetuple())
            print(s_time,"=========上传时间=12=======")

            ess_f_path=""
            if flag == 1:
                print("-----------ess上传-----------")

                ess_f_path = os.path.join("doc", pro_name, vend_name, str(s_time) + '-' + myFile.name)
                destination = open(os.path.join("doc",pro_name,vend_name,str(s_time)+ '-' +myFile.name ),'wb+')# 打开特定的文件进行二进制的写操作
                for chunk in myFile.chunks():  # 分块写入文件
                    file = destination.write(chunk)
                destination.close()
                name_obj.update(status=2)

            else:
                print("-----------pub上传-----------")
                destination = open(os.path.join("doc", pro_name, "pub", str(s_time) + '-' + myFile.name), 'wb+')
                for chunk in myFile.chunks():     # 分块写入文件
                    file = destination.write(chunk)
                destination.close()
                name_obj.update(status=2)

            stat_obj = name_obj[0].status
            print(stat_obj, "========s_obj")

            # 文档日志
            op_file = "上传了" + name_obj[0].upload_filename
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            Doc_log.objects.create(s_time=name_obj[0].create_time,operation = op_file, user_id=opt_usr)
            return JsonResponse({"code": "0000","file_id":file_id,"stat_obj":stat_obj,"ess_f_path":ess_f_path})


        # 其他文件
        # code_obj = Doc.objects.filter(file_name=f_code, pro_name=other_pro_name, vend_name=other_vend_name)
        elif not name_obj and code_obj:
            stat_obj = code_obj[0].status
            file_id = code_obj[0].id
            flag = code_obj[0].flag
            print(flag,"------------")
            vend_name = code_obj[0].vend_name
            pro_name = code_obj[0].pro_name
            time_str = code_obj[0].create_time
            s_time = time.mktime(time_str.timetuple())
            print(stat_obj, "===*****=====s_obj")

            if flag == 3:
                p = os.getcwd() + "/" + "doc"
                dirs = os.listdir(p)
                if pro_name in dirs:
                    print(pro_name)
                    vs = os.listdir(p + "/" + pro_name)
                    print(vs, 89)
                    if vend_name + "_other" in vs:
                        print(vend_name)
                    else:
                        os.makedirs(p + "/" + pro_name + "/" + vend_name + "_other")
                else:
                    os.makedirs(p + "/" + pro_name + "/" + vend_name + "_other")

                other_upname_obj = Doc.objects.filter(upload_filename=myFile.name, pro_name=other_pro_name,
                                                      vend_name=other_vend_name,flag=3)

                print( other_upname_obj,"8888888888888======")
                if not other_upname_obj:
                    print(888)
                    other_path = os.path.join("doc", pro_name, vend_name + "_other", str(s_time) + '-' + myFile.name)
                    destination = open(other_path, 'wb+')  # 打开特定的文件进行二进制的写操作
                    for chunk in myFile.chunks():  # 分块写入文件
                        file = destination.write(chunk)
                    destination.close()
                    code_obj.update(upload_filename=myFile)
                    code_obj.update(filesize=filesize)
                    code_obj.update(status=2)
                    stat_obj = code_obj[0].status
                    print(stat_obj, "========s_obj")
                else:
                    print("已存在")
                    return JsonResponse({"code": "0001"})

                # 文档日志
                op_file = "上传了" + code_obj[0].upload_filename
                opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
                Doc_log.objects.create(s_time=code_obj[0].create_time, operation=op_file, user_id=opt_usr)
            return JsonResponse({"code": "0000", "file_id": file_id, "stat_obj": stat_obj})
    return render(request, "doc_t/document.html")

#下载
#得到下载的路径
def download_file(request):
     if request.method == "POST":
         file_id = request.POST.get("file_id","")
         flag = request.POST.get("flag","")
         print(flag,888)
         obj_id = Doc.objects.filter(id = file_id)
         file_name = obj_id[0].upload_filename
         vend_name = obj_id[0].vend_name
         print(vend_name)
         pro_name = obj_id[0].pro_name
         print(pro_name)
         create_time = obj_id[0].create_time
         print(create_time)
         s_time = time.mktime(create_time.timetuple())
         print(s_time,"===========下载时间=======")
         obj_id.update(download_time=str(s_time))

         if flag == "1":
             f_path="/doc/"+pro_name+"/"+vend_name+"/"+str(s_time)+"-"+file_name
             print( f_path)
             return JsonResponse({"f_path": f_path,"ctime":str(s_time)})

         elif flag == "2":
             f_path = "/doc/" + pro_name + "/" + "pub" + "/" + str(s_time) + "-" + file_name
             return JsonResponse({"f_path": f_path,"ctime":str(s_time)})

         elif flag == "3":
             f_path = "/doc/" + pro_name + "/"+vend_name+"_other"+"/" + str(s_time) + "-" + file_name
             return JsonResponse({"f_path": f_path,"ctime":str(s_time)})


#厂商文件下载
def down_load(request):
    print("进来下载")
    # path_obj = request.GET.get("file_path")
    recv_data = request.GET.dict()
    path_obj = recv_data.get("file_path","")
    print(path_obj)
    try:
        with open(os.getcwd()+path_obj, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(path_obj.split("/")[-1].split("-")[1]))
            # response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(path_obj.split("/")[-1]))

            # 文档日志
            op_file = "下载了" + path_obj.split("/")[-1]
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            Doc_log.objects.create(operation=op_file, user_id=opt_usr)
            return response

    except:
        return HttpResponse("此文件暂未上传!")
        # return JsonResponse({"code":"0000"})


#下载的第二种方法
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
def doc_add(request):
    if request.method == "GET":
        pro_name = request.GET.get("pro_add","")
        vend_name = request.GET.get("vend_add","")
        flag = request.GET.get("flag","")
        return render(request, "doc_t/doc_add.html",{"pro_name":pro_name,"vend_name":vend_name,"flag":flag})

    if request.method == "POST":
        myadd=request.POST.get("myadd","")
        pro_name=request.POST.get("pro_name","")
        vend_name=request.POST.get("vend_name","")
        flag = request.POST.get("flag")
        print(flag,"---------flag=========")
        add_obj = Doc.objects.filter(file_name=myadd)

        #给其中一个项目中一个厂商添加文件，这个项目得其他厂商也要添加此文件
        pro_obj = Projects.objects.filter(project_name=pro_name)[0]
        v_name = pro_obj.vend_prod.all()
        print(v_name,"======所有的厂商=========")

        #必要文件
        if myadd and pro_name and vend_name and flag != "3" and not add_obj:

            for v in v_name:
                # v_all = v.vend_name
                print(1)
                print(v.vend_name)
                up_name = v.vend_name + "_" + myadd + ".pdf"
                Doc.objects.create(file_name=myadd,pro_name=pro_name,vend_name=v.vend_name,flag=flag,upload_filename=up_name)

                #文档日志
                op_file = "项目"+": "+pro_name+","+"新增了文件" + "<<" + v.vend_name+"_"+ myadd + ">>"
                opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
                Doc_log.objects.create(operation=op_file, user_id=opt_usr)
            return JsonResponse({"code": "0000","pro_name":pro_name,"vend_name":vend_name,"flag":flag})

        #公共文件
        # elif myadd and pro_name and flag!="3" and not add_obj:
        elif myadd and pro_name and flag =="2" and not add_obj:
            up_name = pro_name + "_" + myadd + ".pdf"
            Doc.objects.create(file_name=myadd, pro_name=pro_name, flag=flag, upload_filename=up_name)
            return JsonResponse({"code": "0000","pro_name":pro_name,"vend_name":vend_name,"flag":flag})

        #其他文件
        elif myadd and pro_name and vend_name and flag =="3" and not add_obj:
            Doc.objects.create(file_name=myadd, pro_name=pro_name, vend_name=vend_name, flag=flag)

            return JsonResponse({"code": "0000","pro_name":pro_name,"vend_name":vend_name,"flag":flag})

        elif add_obj:
            return JsonResponse({"code": "0001","pro_name":pro_name,"vend_name":vend_name,"flag":flag})
        else:
            return JsonResponse({"code": "0002","pro_name":pro_name,"vend_name":vend_name,"flag":flag})


#修改文件名字页面
def change_name(request):
    if request.method == "GET":
        f_id = request.GET.get("f_id")
        f_obj = Doc.objects.get(id = f_id)
        up_name = f_obj.upload_filename
        print(f_id,up_name,999)
        return render(request, "doc_t/change_name.html", {"f_id": f_id,"up_name":up_name})

    if request.method == "POST":
        mychange = request.POST.get("mychange")
        print(mychange)
        f_id = request.POST.get("f_id")
        print( f_id )
        id_obj = Doc.objects.filter(id=int(f_id))
        print(mychange,f_id,888)
        id_obj.update(upload_filename=mychange)
        return JsonResponse({"code":"0000"})


def stat_change(request):
    recv_data = request.POST.dict()
    type_name = recv_data.get("type_name")
    print(type_name)
    status = recv_data.get("change_status")  #数字状态
    print(status, "状态============")
    change_id = recv_data.get("change_id")   #文件id
    print(change_id)
    change_obj = ""
    filename = ""
    if type_name == "ess":
        change_obj = Doc.objects.filter(id=int(change_id)).first()

    elif type_name == "pub":
        change_obj = Doc.objects.filter(id=int(change_id)).first()

    elif type_name == "other":
        change_obj = Doc.objects.filter(id=int(change_id)).first()

    # print(s[1],111)
    filename = change_obj.upload_filename
    old_stat = change_obj.status

    if change_obj:
        change_obj.status = str(status)
        change_obj.save()

        # 文档日志
        d = Doc(status=old_stat)
        old_s = d.get_status_display()
        d1 = Doc(status=int(status))
        new_s = d1.get_status_display()
        # op_file = filename+ "状态:"+ str(old_stat) + "===>" + status
        op_file ="<"+ filename +">"+ " 状态 : "+old_s + "===>" + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        Doc_log.objects.create(operation=op_file, user_id=opt_usr)

    return JsonResponse({"code": "0000","stat":change_obj.status,"change_id":change_id})


# 上传人添加备注页面
def add_mark(request):
    if request.method == "GET":
        m_id = request.GET.get("m_id")
        obj = Doc.objects.filter(id=m_id).first()
        pro_name = obj.pro_name
        print(pro_name,"====")
        vend_name = obj.vend_name
        flag = obj.flag
        mark=obj.remark
        print(vend_name,"---------vend name")

        return render(request, "doc_t/add_mark.html", {"m_id": m_id,"pro_name":pro_name,"vend_name":vend_name,"flag":flag,"mark":mark})

    if request.method == "POST":
        myadd = request.POST.get("myadd")
        m_id = request.POST.get("m_id")
        pro_name = request.POST.get("pro_name")
        vend_name = request.POST.get("vend_name")
        flag = request.POST.get("flag")
        check = request.POST.get("check","")
        print(check,"状态--------------")
        id_obj = Doc.objects.filter(id=int(m_id))
        id_obj.update(remark=myadd)

        # 文档日志
        obj = id_obj.first()
        old_stat = obj.get_status_display()
        file_name=obj.upload_filename

        if check:
            id_obj.update(status=5)
            new_obj=Doc.objects.filter(id=int(m_id)).first()
            new_stat=new_obj.get_status_display()

            op_file = "<<" + file_name + ">>" + " 状态 : " + old_stat + " ===> " + new_stat
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            Doc_log.objects.create(operation=op_file, user_id=opt_usr)

        return JsonResponse({"code":"0000","pro_name":pro_name,"vend_name":vend_name,"flag":flag})



def make_dir(pub):
    p = os.getcwd()+"/"+"doc"
    print( p)
    dirs = os.listdir(p)
    if pub not in dirs:
        os.makedirs(p + "/" + pub)
    vs = os.listdir(p + "/" + pub)
    if "pub" in vs:
        print("已存在")
    else:
        os.makedirs(p + "/" + pub + "/" + "pub")


#公共文件部分
def get_pub(request):
    recv_data = request.POST.dict()
    pub_pro_name = recv_data.get("pub_pro_name", "")
    print(pub_pro_name, " pub_pro_name============")
    flag = recv_data.get("flag", "")
    print(flag,"公共文件")

    pub_list = ["启动会签到表", "供应商结果意见监督书", "测试人员签到表", "每日例行操作检查表", "调试完成报告", "测试录像视频", "上会材料PPT"]
    pub_list1 = ["启动会签到表", "供应商结果意见监督书", "测试人员签到表", "每日例行操作检查表", "调试完成报告", "测试录像视频"]

    if flag == "2" and pub_pro_name:
        print("进来2")
        pro_obj = Projects.objects.filter(project_name=pub_pro_name).first()
        p_id = pro_obj.id

        #查看上会状态
        pro_stat = pro_obj.meeting_status
        pub_obj = Doc.objects.filter(pro_id_id=p_id,flag=flag).first()

        #会议纪要
        pd_obj = ProjectDaily.objects.filter(pj_id_id=p_id)

        if pro_stat == "1":  # 上会  ppt有显示
            if not pub_obj:
                print("没有")
                for pub in pub_list:
                    upname =pub_pro_name + "_" + pub + '.pdf'
                    Doc.objects.create(file_name=pub, upload_filename=upname, flag=2, pro_id_id=p_id, pro_name=pub_pro_name)
                    print("写入")

                pub_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,"id":d.id,
                                "status": d.get_status_display(),"remark":d.remark,"check_remark": d.check_remark,"pro_name":d.pro_name,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in Doc.objects.filter(pro_name=pub_pro_name, flag=2,pro_id_id=p_id)]

                make_dir(pub_pro_name)

                type_dic = {"1": "日报", "2": "会议"}
                print(type_dic["2"])

                pd_list = [{"id":pd.id,"file_name":pd.file_name,"type": type_dic[pd.type], "up_time":pd.up_time.strftime('%Y-%m-%d'),"status":pd.get_status_display(), "mark":pd.mark,"check_mark":pd.check_mark,"create_time":pd.up_time,"download_time":pd.download_time} for pd in pd_obj]
                print(pd_list,"------------会议纪要111")
            else:
                # 存储了之后再次选择时显示数据库中内容
                print("有内容123")
                pub_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,"id":d.id,
                                "status": d.get_status_display(),"remark":d.remark,"check_remark": d.check_remark,"pro_name":d.pro_name,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in Doc.objects.filter(pro_name=pub_pro_name, flag=2,pro_id_id=p_id)]

                make_dir(pub_pro_name)

                type_dic = {"1": "日报", "2": "会议"}
                print(type_dic["1"])
                pd_list = [{"id":pd.id,"file_name":pd.file_name,"type": type_dic[pd.type], "up_time":pd.up_time.strftime('%Y-%m-%d'),"status":pd.get_status_display(), "mark":pd.mark,"check_mark":pd.check_mark,"create_time":pd.up_time,"download_time":pd.download_time} for pd in pd_obj]
                print(pd_list,"------------会议纪要123")

            return JsonResponse({"code": "0000",
                                "pub_obj_all": pub_obj_all,
                                "pd_list":pd_list,
                                "flag":flag,
                                 })

        else:
            if not pub_obj:
                print("没有")
                for pub in pub_list1:
                    upname = pub_pro_name + "_" + pub + '.pdf'
                    Doc.objects.create(file_name=pub, upload_filename=upname, flag=2, pro_id_id=p_id,
                                       pro_name=pub_pro_name)
                    print("写入")
                pub_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,"d":d.id,
                                "status": d.get_status_display(), "remark": d.remark,"check_remark": d.check_remark,"pro_name":d.pro_name,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in
                               Doc.objects.filter(pro_name=pub_pro_name, flag=2)]

                make_dir(pub_pro_name)


                type_dic = {"1": "日报", "2": "会议"}
                pd_list = [{"id":pd.id,"file_name":pd.file_name,"type": type_dic[pd.type], "up_time":pd.up_time.strftime('%Y-%m-%d'),"status":pd.get_status_display(), "mark":pd.mark,"check_mark":pd.check_mark,"create_time":pd.up_time,"download_time":pd.download_time} for pd in pd_obj]
                print(pd_list, "------------会议纪要")
            else:
                # 存储了之后再次选择时显示数据库中内容
                print("有内容22")
                pub_obj_all = [{"file_name": d.file_name, "upload_filename": d.upload_filename, "filesize": d.filesize,"id":d.id,
                                "status": d.get_status_display(), "remark": d.remark,"check_remark": d.check_remark,"pro_name":d.pro_name,"create_time":time.mktime(d.create_time.timetuple()),"download_time":d.download_time} for d in
                               Doc.objects.filter(pro_name=pub_pro_name, flag=2)]

                make_dir(pub_pro_name)
                type_dic = {"1": "日报", "2": "会议"}
                pd_list = [{"id":pd.id,"file_name":pd.file_name,"type": type_dic[pd.type], "up_time":pd.up_time.strftime('%Y-%m-%d'),"status":pd.get_status_display(), "mark":pd.mark,"check_mark":pd.check_mark,"create_time":pd.up_time,"download_time":pd.download_time } for pd in pd_obj]
                print(pd_list, "------------会议纪要")

            return JsonResponse({"code": "0000",
                                 "pub_obj_all": pub_obj_all,
                                 "pd_list":pd_list,
                                 })

    return JsonResponse({"code": "0001"})


def doc_log(request):
    user = ManageUser.objects.filter(id=int(request.session.get("user_id", ""))).first()
    log_list = []
    if user:
        log_list = [
            [log_obj.s_time, log_obj.user_id.user_role.all().first(), log_obj.user_id.username, log_obj.operation]
            for log_obj in Doc_log.objects.all() if log_obj.user_id == user]

    return render(request,"doc_t/doc_log.html",{"log_list":log_list})


def check_pass(request):
    recv_data = request.POST.dict()
    pass_id = recv_data.get("pass_id")
    pass_ctime = recv_data.get("pass_ctime")
    print(pass_ctime,"pass_ctime+++++++++++",type(pass_ctime))
    pass_other_id = recv_data.get("pass_other_id")
    pass_other_ctime = recv_data.get("pass_other_ctime")
    pass_pub_id = recv_data.get("pass_pub_id")
    pass_pub_ctime = recv_data.get("pass_pub_ctime")
    pass_jy_id = recv_data.get("pass_jy_id")
    pass_jy_ctime = recv_data.get("pass_jy_ctime")
    print(pass_jy_ctime,"======pass_jy_ctime")
    print(pass_jy_id,"pass_jy_id的值纪要")
    # if pass_id or pass_pub_id or pass_other_id:

    ps_id_obj = ""

    if pass_id:
        ps_id_obj = Doc.objects.filter(id=pass_id)

    elif pass_other_id:
        ps_id_obj = Doc.objects.filter(id=pass_other_id)
        print(ps_id_obj, "===========")
    elif pass_pub_id:
        ps_id_obj = Doc.objects.filter(id=pass_pub_id)
    elif pass_jy_id:
        print("jy文件通过进来")
        ps_jy_obj = ProjectDaily.objects.filter(id=pass_jy_id)

        ps_jy_first = ps_jy_obj.first()
        old_stat = ps_jy_first.status
        file_name = ps_jy_first.file_name

        create_time = ps_jy_first.up_time
        s_time = time.mktime(create_time.timetuple())
        print("jjjjyyyyyy s_time",s_time)
        d = ProjectDaily(status=old_stat)
        old_s = d.get_status_display()

        s_time = str(s_time)
        print("jjjjyy----yyyy s_time", s_time)
        if s_time == pass_jy_ctime:
            ps_jy_obj.update(status=3)
            new_obj = ProjectDaily.objects.filter(id=pass_jy_id).first()
            new_s = new_obj.get_status_display()

            op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            print("++++++改变--纪要")
            Doc_log.objects.create(operation=op_file, user_id=opt_usr)
            return JsonResponse({"code": "0000", "status": "3"})
        else:
            return JsonResponse({"code": "0001"})


    # 文档日志
    # 旧的 三者统一
    ps_id_first = ps_id_obj.first()
    old_stat = ps_id_first.status
    file_name = ps_id_first.upload_filename
    create_time = ps_id_first.create_time
    print(create_time,"----create_time------",type(create_time))
    s_time = time.mktime(create_time.timetuple())
    print(str(s_time))
    d = Doc(status=old_stat)
    old_s = d.get_status_display()


    #保证下载审核的文件是当时下载的没有上传新的，否则需要重新下载
    s_time = str(s_time)
    if s_time == pass_ctime:
        ps_id_obj.update(status=3)
        new_obj = ""
        if pass_id:
            new_obj = Doc.objects.filter(id=pass_id).first()
        elif pass_other_id:
            new_obj = Doc.objects.filter(id=pass_other_id).first()
        elif pass_pub_id:
            new_obj = Doc.objects.filter(id=pass_pub_id).first()

        new_s = new_obj.get_status_display()

        op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        print("++++++改变")
        Doc_log.objects.create(operation=op_file, user_id=opt_usr)
        return JsonResponse({"code": "0000", "status": "3"})

    elif s_time == pass_other_ctime:
        ps_id_obj.update(status=3)

        new_obj = ""
        if pass_id:
            new_obj = Doc.objects.filter(id=pass_id).first()
        elif pass_other_id:
            new_obj = Doc.objects.filter(id=pass_other_id).first()
        elif pass_pub_id:
            new_obj = Doc.objects.filter(id=pass_pub_id).first()

        new_s = new_obj.get_status_display()

        op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        print("++++++改变")
        Doc_log.objects.create(operation=op_file, user_id=opt_usr)
        return JsonResponse({"code": "0000", "status": "3"})

    elif s_time == pass_pub_ctime:
        ps_id_obj.update(status=3)

        new_obj = ""
        if pass_id:
            new_obj = Doc.objects.filter(id=pass_id).first()
        elif pass_other_id:
            new_obj = Doc.objects.filter(id=pass_other_id).first()
        elif pass_pub_id:
            new_obj = Doc.objects.filter(id=pass_pub_id).first()

        new_s =new_obj.get_status_display()

        op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
        print("++++++改变")
        Doc_log.objects.create(operation=op_file, user_id=opt_usr)
        return JsonResponse({"code": "0000","status": "3"})

    else:
        return JsonResponse({"code": "0001"})



def no_check_pass(request):
    recv_data = request.POST.dict()
    pass_id = recv_data.get("pass_id")
    pass_ctime = recv_data.get("pass_ctime")
    pass_other_id = recv_data.get("pass_other_id")
    pass_other_ctime = recv_data.get("pass_other_ctime")
    print(pass_other_ctime,"pass_other_ctime---&&&----")
    pass_pub_id = recv_data.get("pass_pub_id")
    pass_pub_ctime = recv_data.get("pass_pub_ctime")
    print(pass_pub_ctime, "pass_pub_ctime----***---")
    print(pass_other_id)
    pass_jy_id = recv_data.get("pass_jy_id")
    pass_jy_ctime = recv_data.get("pass_jy_ctime")
    print( pass_jy_id,"不通过纪要！")

    ps_id_obj = ""
    if pass_id:
        ps_id_obj = Doc.objects.filter(id=pass_id)
    elif pass_other_id:
        ps_id_obj = Doc.objects.filter(id=pass_other_id)
        print(ps_id_obj, "===========")
    elif pass_pub_id:
        ps_id_obj = Doc.objects.filter(id=pass_pub_id)
    elif pass_jy_id:
        ps_jy_obj = ProjectDaily.objects.filter(id=pass_jy_id)

        ps_jy_first = ps_jy_obj.first()
        old_stat = ps_jy_first.status
        file_name = ps_jy_first.file_name

        create_time = ps_jy_first.up_time
        s_time = time.mktime(create_time.timetuple())

        d = ProjectDaily(status=old_stat)
        old_s = d.get_status_display()

        s_time=str(s_time)
        if s_time == pass_jy_ctime:
            ps_jy_obj.update(status=4)

            new_obj = ProjectDaily.objects.filter(id=pass_jy_id).first()
            new_s = new_obj.get_status_display()

            op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            print("++++++改变--纪要不通过")
            Doc_log.objects.create(operation=op_file, user_id=opt_usr)

            return JsonResponse({"code": "0000", "status": "4"})
        else:
            return JsonResponse({"code": "0001"})


    # 文档日志
    # 旧的 三者统一
    ps_id_first = ps_id_obj.first()
    old_stat = ps_id_first.status
    file_name = ps_id_first.upload_filename

    create_time = ps_id_first.create_time
    print(create_time, "----create_time------", type(create_time))
    s_time = time.mktime(create_time.timetuple())
    print(str(s_time))
    print(s_time, type(s_time), "========")

    d = Doc(status=old_stat)
    old_s = d.get_status_display()

    s_time = str(s_time)
    if s_time == pass_ctime:
        ps_id_obj.update(status=4)
        new_obj = ""
        if pass_id:
            new_obj = Doc.objects.filter(id=pass_id).first()
        elif pass_other_id:
            new_obj = Doc.objects.filter(id=pass_other_id).first()
        elif pass_pub_id:
            new_obj = Doc.objects.filter(id=pass_pub_id).first()
        new_s = new_obj.get_status_display()

        op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()

        Doc_log.objects.create(operation=op_file, user_id=opt_usr)

        return JsonResponse({"code": "0000"})
    elif s_time == pass_other_ctime:
        ps_id_obj.update(status=4)

        new_obj = ""
        if pass_id:
            new_obj = Doc.objects.filter(id=pass_id).first()
        elif pass_other_id:
            new_obj = Doc.objects.filter(id=pass_other_id).first()
        elif pass_pub_id:
            new_obj = Doc.objects.filter(id=pass_pub_id).first()
        new_s = new_obj.get_status_display()

        op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()

        Doc_log.objects.create(operation=op_file, user_id=opt_usr)

        return JsonResponse({"code": "0000"})
    elif s_time == pass_pub_ctime:
        ps_id_obj.update(status=4)

        new_obj = ""
        if pass_id:
            new_obj = Doc.objects.filter(id=pass_id).first()
        elif pass_other_id:
            new_obj = Doc.objects.filter(id=pass_other_id).first()
        elif pass_pub_id:
            new_obj = Doc.objects.filter(id=pass_pub_id).first()
        new_s = new_obj.get_status_display()

        op_file = "<<" + file_name + ">>" + " 状态 : " + old_s + " ===> " + new_s
        opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()

        Doc_log.objects.create(operation=op_file, user_id=opt_usr)

        return JsonResponse({"code": "0000"})
    else:
        return JsonResponse({"code": "0001"})

#得到纪要下载的路径
def download_file_jy(request):
    if request.method == "POST":
         file_id = request.POST.get("file_id","")
         print( file_id)
         obj_id = ProjectDaily.objects.filter(id = file_id)
         file_name = obj_id[0].file_name
         pj_id = obj_id[0].pj_id_id
         print(pj_id,type(pj_id),9990)

         create_time = obj_id[0].up_time
         print(create_time)
         s_time = time.mktime(create_time.timetuple())
         print(s_time, "===========下载时间jy=======")

         #更新下载时间字段
         obj_id.update(download_time=str(s_time))
         p_obj = Projects.objects.filter(id=pj_id).first()
         pro_name=p_obj.project_name
         print(pro_name)
         f_path="/static/project_daily/"+pro_name+"/" + file_name
         print(f_path,"纪要项目名")
         return JsonResponse({"f_path": f_path,"ctime":str(s_time)})

#纪要文件下载
def down_load_jy(request):
    print("进来下载")
    recv_data = request.GET.dict()
    path_obj = recv_data.get("file_path","")
    print(path_obj,"纪要文件-----")
    try:
        with open(os.getcwd()+path_obj, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(path_obj.split("/")[-1]))

            # 文档日志
            op_file = "下载了" + path_obj.split("/")[-1]
            opt_usr = ManageUser.objects.filter(id=int(request.session.get("user_id", "0"))).first()
            Doc_log.objects.create(operation=op_file, user_id=opt_usr)
            return response
    except:
        return HttpResponse("此文件暂未上传!")


# 图形展示
def shape_show(request):
    data = {}
    shape_obj = Doc.objects.all()
    shape_list = [{"value": 1, "name":s.upload_filename} for s in shape_obj]
    print(shape_list)
    return JsonResponse({'shape_list': shape_list})

    # 最后将数据打包成json格式以字典的方式传送到前端
    # return render(request, 'doc_t/document.html',{'shape_list': shape_list} )

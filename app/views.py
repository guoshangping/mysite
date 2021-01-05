# Create your views here.
from ast import literal_eval
import json
import re
from itertools import chain
from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator
from django.db import transaction
from mylib.form import UploadFileForm
from mylib.createDoc import createDoc
from mylib.uploadFile import handle_uploaded_file
from mylib.docReader import scanDoc
from docxtpl import *
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.utils import timezone
from app.models import Input, User, Pros
import os, time
from django.views import generic
from django.db.models import Q
from functools import wraps
import random, string
from captcha.image import ImageCaptcha
import collections

'''def regist(request):
    print('这是注册页面view')
    return render(request,'register.html')'''

'''def regist_logic(request):
    print('这是注册逻辑view')
    username = request.POST.get('realname')
    password = request.POST.get('password')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    birth = request.POST.get('birth')
    print(username,password,age,gender,birth)
    try:
        with transaction.atomic():
            user = User.objects.create(username=username,password=password,age=age,gender=gender,birth=birth)
            user.save()
            return HttpResponse('1')
    except Exception as e:
        print(str(e))
        return HttpResponse('0')'''

'''def check_ifregist(request):
    print('这是检测用户是否已经注册的view')
    name = request.POST.get('name')
    print('name:',name)
    res = User.objects.filter(username=name)
    if res:
        return HttpResponse('1')
    else:
        return HttpResponse('0')'''

'''def login_logic(request):
    print('这是验证登录信息的view')
    username = request.POST.get('username')
    password = request.POST.get('password')
    identifycode = request.POST.get('identifycode')
    code = request.session.get('code')
    print('用户输入的验证码是：',identifycode)
    if code.lower() == identifycode.lower():
        user = User.objects.filter(username=username,password=password)
        if user:
            request.session['is_login'] = '1'  # 这个session用于之后访问每个页面，即调用每个视图函数，判断用户是否已经登录
            request.session['user_id'] = user[0].id
            request.session['user_name'] = user[0].username

            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        return HttpResponse('2')'''

'''def login_page(request):
    print('这是访问登录页面的view')
    return render(request,'login.html')'''

'''#生成验证码
def getcaptcha(request):
    image = ImageCaptcha(fonts=[os.path.abspath("captcha/data/DroidSansMono.ttf")])
    code = random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4)
    random_code = "".join(code)
    print('验证码中的字符是：',random_code)
    request.session['code'] = random_code
    data = image.generate(random_code)
    return HttpResponse(data, "image/png")'''

'''#检测是否登录
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            print('此用户已登录')
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner'''


# class select(generic.ListView):
#     template_name = 'select.html'
#     context_object_name = 'list'
#     def get_queryset(self):
#         tag = self.request.session['user_id']
#         return Input.objects.filter(tag_id=tag)[:5]

# @check_login
def select(request):
    print('跳转至select.html的view')
    # tag = request.session['user_id']
    userid = request.GET.get('userid')
    proid = request.GET.get('proid')
    proname = request.GET.get('proname')
    pros = Pros.objects.filter(proname=proname).values('chargeperson', 'participant')
    chargeperson = pros[0]['chargeperson']
    participant = pros[0]['participant']
    print(proname,proid,pros, chargeperson, participant)
    loguser = User.objects.filter(id=userid).values()[0]['username']
    print(loguser)
    if loguser in chargeperson or loguser in participant:
        # inputs = Input.objects.filter(user_id=userid).order_by('-pub_date')[:5]
        # inputs = Input.objects.filter(tag_id=userid,pro_id=proid).order_by('-pub_date')[:5]
        # users = User.objects.filter(input__pro_id=proid).order_by('-input__pub_date')[:5][0]
        inputs = Input.objects.filter(pro_id=proid).order_by('-pub_date')[:5]
        print(inputs)
        # print(len(users.input_set.all()))
        # for i in users:
        #     print(i.input_set.all().values())
        # user = User.objects.filter(pk=1)[0]
        return render(request, 'select.html', {'inputs': inputs, 'userid': userid})
    else:
        return HttpResponse('您没有权限使用测试报告进行编辑，请联系负责人将您添加到参与者')


'''def select(request):
    return render(request, 'select.html')'''


# @check_login
def select2(request):
    print('这是根据输入项目名称查询结果并跳转至select.html的view')
    # tag = request.session['user_id']
    # tag = request.Get.get('userid')
    mark = request.POST.get('mark')
    print('用户输入的项目名称是：', mark)
    if mark:
        inputs2 = Input.objects.filter(mark=mark).order_by('-pub_date').values()
        if inputs2:
            print(inputs2)
            return JsonResponse(list(inputs2), safe=False)
        else:
            return HttpResponse('0')
    else:
        return HttpResponse('2')


# class index(generic.ListView):
#     template_name = 'index.html'
#     context_object_name = 'list'
#     def get_queryset(self):
#         return Input.objects.order_by('-pub_date')[:5]

# @check_login
def index(request):
    print('这是跳转至index.html的view')
    userid = request.GET.get('userid')
    print(userid)
    uname = User.objects.filter(id=userid).values()[0]['username']
    print(uname)
    inputs = Input.objects.order_by('-pub_date')[:5]
    return render(request, 'index.html', {'inputs': inputs})

def query_participant(request):
    print('这是查询所有参与人的视图函数')
    pros = list(Pros.objects.filter(status=1).values('participant'))
    print(pros)
    a = []
    for i in pros:
        i = i['participant']
        print(i, type(i))
        if i != str([]) and i != '未指定':
            y = eval(i)
            print(y, type(y))
            for j in y:
                print(j, type(j))
                j1 = j.strip(" ")
                j2 = j1.split(",")
                for k in j2:
                    a.append(k)
        elif i == '未指定':
            a.append(i)
    a = list(set(a))
    print(a)
    return JsonResponse({'participant': a})


def query_charperson(request):
    print('这是查询所有负责人的视图函数')
    pros = list(Pros.objects.filter(status=1).values('chargeperson'))
    print(pros)
    a = []
    for i in pros:
        i = i['chargeperson']
        print(i, type(i))
        if i != str([]) and i != '未指定':
            y = eval(i)
            print(y, type(y))
            for j in y:
                print(j, type(j))
                j1 = j.strip(" ")
                j2 = j1.split(",")
                for k in j2:
                    a.append(k)
        elif i == '未指定':
            a.append(i)
    a = list(set(a))
    print(a)
    return JsonResponse({'charperson': a})

def query_proname(request):
    print('这是查询所有项目名称的视图函数')
    pros = Pros.objects.filter(status=1).values('proname')
    print(pros)
    a = []
    for i in pros:
        i = i['proname']
        a.append(i)
    a = list(set(a))
    print(a)
    return JsonResponse({'proname':a})


def query_proxmjd(request):
    print('这是查询所有项目进度的视图函数')
    pros = list(Pros.objects.filter(status=1).values('prostatus'))
    print(pros)
    a = []
    for i in pros:
        i = i['prostatus']
        a.append(i)
    a = list(set(a))
    print(a)
    return JsonResponse({'xmjd': a})


def query_protime(request):
    print('这是查询所有项目创建时间的视图函数')
    pros = list(Pros.objects.filter(status=1).values('createtime'))
    print(pros)
    a = []
    for i in pros:
        i = str(i['createtime']).split('-')[0]
        print(i, type(i))
        a.append(i)
    a = list(set(a))
    print(a)

    return JsonResponse({'time': a})

def query_protime_yue(request):
    print('这是联合查询功能中根据年份查询月份的视图函数')
    year = request.GET.get('year')
    print(year)
    pros = list(Pros.objects.filter(createtime__year=year,status=1).values('createtime'))
    print(pros)
    a = []
    for i in pros:
        i = str(i['createtime']).split('-')[1]
        a.append(i)
    a = list(set(a))
    print(a)
    return JsonResponse({'yue':a})


def query_properson(request):
    print('这是查询所有项目创建人的视图函数')
    pros = list(Pros.objects.filter(status=1).values('createprouser'))
    print(pros)
    a = []
    for i in pros:
        i = str(i['createprouser'])
        print(i)
        a.append(i)
    a = list(set(a))
    print(a)
    return JsonResponse({'person': a})


def pro_check(request):
    print('这是用户在index页面输入项目名称后检测项目可操作性的视图函数')
    proname = request.GET.get('proname')
    userid = request.GET.get('userid')
    print(proname, userid)
    # proid = Pros.objects.filter(proname=proname).values()[0]['id']
    # print(proid)
    username = User.objects.filter(id=userid).values()[0]['username']
    print(username)
    p = Pros.objects.filter(proname=proname,status=1).values('chargeperson', 'participant')
    print(p)
    flag = 1
    for i in p:
        print(eval(i['chargeperson']))
        print(eval(i['participant']))
        if username in eval(i['chargeperson']):
            flag = 1
            break
        elif username in eval(i['participant']):
            flag = 1
            break
        else:
            flag = 0
        for n in eval(i['participant']):
            n = n.strip()
            print(n)
            if username == n:
                flag = 1
                break
            else:
                flag = 0
    print(flag)
    if flag == 1:
        return HttpResponse('1')
    else:
        return HttpResponse('0')


# class index2(generic.ListView):
#     template_name = 'index2.html'
#     context_object_name = 'list'
#     def get_queryset(self):
#         tag = self.request.session['user_id']
#         print(tag)
#         return Input.objects.filter(Q(tag_id=tag) and Q(id=1))


def lianhe_query(request):
    print('这是联合查询的视图函数')
    year = request.GET.get('year')
    yue = request.GET.get('yue')
    char = request.GET.get('char')
    par = request.GET.get('par')
    xmjd = request.GET.get('xmjd')
    username = request.GET.get('username')
    userclass = request.GET.get('userclass')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    flag = 9
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    print(year, yue, char, par, xmjd, username, userclass, userid)
    number = request.GET.get('num')
    if not number:
        number = 1
    dic = {}
    dic['year'] = year
    dic['yue'] = yue
    dic['char'] = char
    dic['par'] = par
    dic['xmjd'] = xmjd
    print('dic:',dic)
    if dic['year'] == '请选择年份' or dic['year'] == '':
        del dic['year']
    if dic['yue'] == '请选择月份' or dic['yue'] == '':
        del dic['yue']
    if dic['char'] == '请选择负责人' or dic['char'] == '':
        del dic['char']
    if dic['par'] == '请选择参与人' or dic['par'] == '':
        del dic['par']
    if dic['xmjd'] == '请选择项目进度' or dic['xmjd'] == '':
        del dic['xmjd']
    print('过滤后的dic：',dic)
    keys = list(dic.keys())
    pross = Pros.objects.filter(status=1).order_by('status')
    if keys:
        for i in keys:
            if i == 'year':
                year = dic[i]
                pros = Pros.objects.filter(createtime__year=year,status=1)
                pross = list(set(pross) & set(pros))
                print(pross)
            elif i == 'yue':
                yue = dic[i]
                pros = Pros.objects.filter(createtime__month=yue,status=1)
                pross = list(set(pross) & set(pros))
                print(pross)

            elif i == 'char':
                char = dic[i]
                pros = Pros.objects.filter(chargeperson__contains=char,status=1)
                pross = list(set(pross) & set(pros))
                print(pross)

            elif i == 'par':
                par = dic[i]
                pros = Pros.objects.filter(participant__contains=par,status=1)
                pross = list(set(pross) & set(pros))
                print(pross)

            elif i == 'xmjd':
                xmjd = dic[i]
                pros = Pros.objects.filter(prostatus=xmjd,status=1)
                pross = list(set(pross) & set(pros))
                print(pross)

        pross = list(pross)
        print(pross,'**********')
        if pross:
            for i in pross:
                print(i.participant, i.chargeperson, i.createtime, type(i.createtime))
                i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", i.chargeperson.strip("[]"))
                i.participant = re.sub("[0-9\!\%\[\]\'\。]", "", i.participant.strip("[]"))
                i.createtime = str(i.createtime).replace("-", ".")
                print(i.participant, i.chargeperson, i.createtime, type(i.createtime), '****************')
            ts2 = request.session.get('ts')
            print('ts2是：', ts2)
            pagtor = Paginator(pross, per_page=ts2)
            page = pagtor.page(number)
            print(page)
            if userclass == 'True':
                return render(request, 'pros1.html',{'page': page, 'username': username, 'userclass': userclass, 'userid': userid, 'flag': flag,'ts': ts2,'year':year,'yue':yue,'char':char,'par':par,'lianhexmjd':xmjd})
            else:
                return render(request, 'pros2.html',{'page': page, 'username': username, 'userclass': userclass, 'userid': userid, 'flag': flag,'ts': ts2,'year':year,'yue':yue,'char':char,'par':par,'lianhexmjd':xmjd})
        else:
            return HttpResponse('根据条件未查到数据')
    else:
        return redirect('/ap/pro_page/?username='+username+'&userclass='+userclass+'&userid='+userid)
    # print(pros)



#createtime__month=yue,chargeperson__contains=char,participant__contains=par,prostatus=xmjd

def pro_page(request):
    #print('这是分页查询的视图函数')
    username = request.GET.get('username')
    userclass = request.GET.get('userclass')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1!= int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
        # if ts:
        #     ts=int(ts)
        #     request.session['ts'] = ts
        # else:
        #     ts = 10
    print(userclass, username,userid,ts)
    number = request.GET.get('num')
    flag = 1
    if not number:
        number = 1
    pros = Pros.objects.filter(status=1).order_by("prostatus")
    print(pros)
    for i in pros:
        print(i.participant, i.chargeperson, i.createtime, type(i.createtime))
        i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "",i.chargeperson.strip("[]"))
        i.participant = re.sub("[0-9\!\%\[\]\'\。]", "",i.participant.strip("[]"))
        i.createtime = str(i.createtime).replace("-", ".")
        print(i.participant, i.chargeperson, i.createtime, type(i.createtime),'****************')
    print('修改格式后的pros',pros)
    ts2 = request.session.get('ts')
    print('ts2是：',ts2)
    pagtor = Paginator(pros, per_page=ts2)
    page = pagtor.page(number)
    print(page)
    if userclass == 'True':
        return render(request, 'pros1.html',
                      {'page': page, 'username': username, 'userclass': userclass, 'userid': userid, 'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html',
                      {'page': page, 'username': username, 'userclass': userclass, 'userid': userid, 'flag': flag,'ts':ts2})


def pro(request):
    print('这是转发至pros.html的视图函数')
    username = request.GET.get('username')
    userclass = request.GET.get('userclass')
    userid = request.GET.get('userid')
    print(userclass, userid)
    if userclass == 'True':
        userclass = '1'
    else:
        userclass = '0'
    return render(request, 'pros.html', {'username': username, 'userclass': userclass, 'userid': userid})


def create_pro_page(request):
    print('这是转发至创建项目页面的视图函数')
    createprouser = request.GET.get('username')
    userclass = request.GET.get('userclass')
    userid = request.GET.get('userid')
    charges = User.objects.filter(groups__name='行员').values()
    print(charges)
    print(createprouser,userclass,userid)
    return render(request, 'createpro.html', {'createprouser': createprouser, 'userclass':userclass,'userid':userid,'charges': charges})


def create_pro(request):
    print('这是创建项目的视图函数')
    proname = request.POST.get('proname')
    prostatus = request.POST.get('xmjd')
    create_time = request.POST.get('createprotime')
    createprouser = request.POST.get('createprouser')
    chargeperson = request.POST.getlist('chargeperson')
    print(proname, prostatus, chargeperson, create_time, createprouser)
    res = Pros.objects.filter(proname=proname,status=1)
    print(res)
    if res:
        return HttpResponse('2')
    else:
        try:
            if chargeperson:
                q = Pros(proname=proname, prostatus=prostatus, chargeperson=chargeperson, createtime=create_time,
                         createprouser=createprouser)
            else:
                q = Pros(proname=proname, prostatus=prostatus, createtime=create_time, createprouser=createprouser)
            q.save()
            return HttpResponse('1')
        except Exception as e:
            print(e)
            return HttpResponse('0')

#超级用户修改项目界面
def superconfigpro(request):
    print('这是转发至超级用户管理项目页面的视图函数')
    proname = request.GET.get('proname')
    proid = request.GET.get('proid')
    username = request.GET.get('username')
    userclass = request.GET.get('userclass')
    userid = request.GET.get('userid')
    charges = User.objects.filter(groups__name='行员').values()
    return render(request,'superconfigpro.html',{'proname':proname,'chars':charges,'proid':proid,'username':username,'userclass':userclass,'userid':userid})

#这是超级用户一键修改项目的视图函数
def superudate(request):
    print('这是超级用户一键修改项目的视图函数')
    if request.method == "POST":
        username = request.POST.get('username')
        userclass = request.POST.get('userclass')
        userid = request.POST.get('userid')
        participant = request.POST.getlist('par')
        chargeperson = request.POST.getlist('char')
        newproname = request.POST.get('newproname')
        oldproname = request.POST.get('oldproname')
        newtime = request.POST.get('newtime')
        print(username,userclass,userid,bool(participant),chargeperson,newproname,oldproname,newtime)
        pro = Pros.objects.filter(proname=oldproname,status=1)[0]
        proid = pro.id
        print(proid)
        if newproname:
            Pros.objects.filter(id=proid).update(proname=newproname)
        if newtime:
            Pros.objects.filter(id=proid).update(createtime=newtime)
        if chargeperson != ['']:
            Pros.objects.filter(id=proid).update(chargeperson=chargeperson)
        if participant != ['']:
            Pros.objects.filter(id=proid).update(participant=participant)
        return HttpResponse('1')
    else:
        return HttpResponse('0')

#超级用户在修改项目界面修改项目名称的视图函数
def updateproname(request):
    print('这是超级用户修改项目名称的视图函数')
    newproname = request.GET.get('newproname')
    oldproname = request.GET.get('oldproname')
    print(newproname,oldproname)
    try:
        Pros.objects.filter(proname=oldproname,status=1).update(proname=newproname)
        return HttpResponse('1')
    except Exception as e:
        return HttpResponse(e)

#这是超级用户修改项目创建时间的视图函数
def updateprotime(request):
    print('这是超级用户修改项目创建时间的视图函数')
    newtime = request.GET.get('newtime')
    proname = request.GET.get('proname')
    print(newtime,proname)
    try:
        Pros.objects.filter(proname=proname,status=1).update(createtime=newtime)
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse(e)


#这是超级用户在项目修改界面修改负责人的视图函数
def updatechar(request):
    print('这是超级用户在项目修改界面修改负责人的视图函数')
    proname = request.GET.get('proname')
    chars = request.GET.getlist('chargeperson')
    print(proname,chars,type(chars))
    try:
        Pros.objects.filter(proname=proname,status=1).update(chargeperson=chars)
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse(e)

#这是超级用户在项目修改界面修改参与人的视图函数
def updatepar(request):
    print('这是超级用户在项目修改界面修改参与人的视图函数')
    proname = request.GET.get('proname')
    pars = request.GET.getlist('participant')
    print(proname, pars, type(pars))
    try:
        Pros.objects.filter(proname=proname,status=1).update(participant=pars)
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse(e)

#这是超级用户在项目修改界面删除项目的视图函数
def delpro(request):
    print('这是超级用户在项目修改界面删除项目的视图函数')
    proname = request.GET.get('proname')
    print(proname)
    try:
        Pros.objects.filter(proname=proname,status=1).update(status=0)
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('0')

# def curd_delete(request):
#     #从前端(html)获取did数据
#     did=request.GET.get('did')
#     if did:
#         #找到该数据，将其删除
#         Book.objects.get(id=did).delete()
#         #删除成功，返回显示页
#         return redirect('/curd/')

#批量删除操作
def delete_all(request):
    print('这是超级用户进行批量删除项目的视图函数')
    #先判断发过来的是否是post请求
    if request.method=="POST":
        #得到要删除的id列表
        values=request.POST.getlist('vals')
        for i in values:
            #如果id不为空，获取该字段，并将其删除，我们只删除book表，publisher表不变
            if i != '':
                print(i)
                Pros.objects.filter(id=i,status=1).update(status=0)
        return HttpResponse('1')

def configpro(request):
    print('这是转发至配置项目页面的视图函数')
    proname = request.GET.get('proname')
    loguser = request.GET.get('loguser')
    userid = request.GET.get('userid')
    userclass = request.GET.get('userclass')
    ts = request.GET.get('ts')
    print(proname, loguser,userid,userclass,ts)
    charges = Pros.objects.filter(proname=proname,status=1).values()[0]['chargeperson']
    print(type(charges))
    if loguser in charges:
        return render(request, 'configpro.html', {'proname': proname,'username':loguser,'userid':userid,'userclass':userclass,'ts':ts})
    else:
        return HttpResponse('您不是项目负责人，您没有权限配置项目')


def query_all_users(request):
    print('这是查询所有用户的视图函数')
    users = list(User.objects.all().values('username'))
    return JsonResponse({'users': users})


def save_config(request):
    print('这是保存配置项目的视图函数')
    participant = list(request.POST.getlist('participant'))
    proname = request.POST.get('configproname')
    print(type(participant), participant, proname)
    participants = Pros.objects.filter(proname=proname).values()[0]['participant']
    print(participants, type(participants))
    if participants == '未指定':
        print(type(participants))
        # participants = eval(participants)
        # print(participants)
        # for i in participant:
        #     print(i)
        #     if i in participants:
        #         pass
        #     else:
        #         participants.append(i)
        # participants = str(participants)
        print(participants)
        participant = str(list(participant))
        print(participant)
        Pros.objects.filter(proname=proname,status=1).update(participant=participant)
        return HttpResponse('1')
    else:
        participants = eval(participants)
        print(participants,'$$$$$$$$$$$')
        participants = [item.strip(" ") for item in participants]
        print(participants,'###########')
        for i in participant:
            i = i.strip(" ")
            print(i, type(i))
            if i not in participants:
                participants.append(i)
        participants = str(list(set(participants)))
        print(participants)
        Pros.objects.filter(proname=proname,status=1).update(participant=participants)
        return HttpResponse('1')


def query_pro(request):
    print('这是查询项目的视图函数')
    pros = list(Pros.objects.all().values('proname'))
    print(pros)
    if pros:
        return JsonResponse({'pros': pros})
    else:
        return HttpResponse('0')


def update_pro_page(request):
    print('这是转发至修改项目进度页面的视图函数')
    proname = request.GET.get('proname')
    status = request.GET.get('status')
    loguser = request.GET.get('loguser')
    userclass = request.GET.get('userclass')
    userid = request.GET.get('userid')
    print(proname, status, loguser,userclass,userid)
    pro = Pros.objects.filter(proname=proname,status=1).values('chargeperson', 'participant')
    print(pro)
    chargeperson = pro[0]['chargeperson']
    participant = pro[0]['participant']
    print(chargeperson, participant)
    if loguser in chargeperson or loguser in participant:
        return render(request, 'updatepro.html', {'proname': proname, 'status': status,'loguser':loguser,'userclass':userclass,'userid':userid})
    else:
        return HttpResponse('您没有权限修改项目进度')


def update_pro(request):
    print('这是修改项目进度的视图函数')
    proname = request.GET.get('proname')
    status = request.GET.get('xmjd')
    print(proname, status)
    prostatus = Pros.objects.filter(proname=proname,status=1).values('prostatus')[0]['prostatus']
    print(prostatus)
    if prostatus == status:
        return HttpResponse('0')
    else:
        Pros.objects.filter(proname=proname).update(prostatus=status)
        return HttpResponse('1')

def pro_chaxun_mohu(request):
    print('这是根据项目名称模糊查询的视图函数')
    userclass = request.GET.get('userclass')
    number = request.GET.get('num')
    proname = request.GET.get('proname')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 8
    print(proname)
    if not number:
        number = 1
    pros = Pros.objects.filter(proname__contains=proname,status=1)
    print(pros)
    for i in pros:
        i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", i.chargeperson.strip("[]"))
        i.participant = re.sub("[0-9\!\%\[\]\'\。]", "", i.participant.strip("[]"))
        i.createtime = str(i.createtime).replace("-", ".")
    print(pros)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pros, per_page=ts2)
    page = pagtor.page(number)
    if userclass == 'True':
        return render(request, 'pros1.html',
                      {'page': page, 'proname': proname, 'userclass': userclass, 'username': username, 'userid': userid,
                       'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html',
                      {'page': page, 'proname': proname, 'userclass': userclass, 'username': username, 'userid': userid,
                       'flag': flag,'ts':ts2})

def pro_chaxun_byproname(request):
    print('这是根据项目名称筛选进行精确查询的视图函数')
    userclass = request.GET.get('userclass')
    number = request.GET.get('num')
    proname = request.GET.get('proname')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 7
    if not number:
        number = 1
    proname1 = proname.strip("'")
    proname2 = proname1.split(",")
    pros = Pros.objects.filter(proname__in=proname2,status=1)
    print(pros)
    for i in pros:
        i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", i.chargeperson.strip("[]"))
        i.participant = re.sub("[0-9\!\%\[\]\'\。]", "", i.participant.strip("[]"))
        i.createtime = str(i.createtime).replace("-", ".")
    print(pros)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pros, per_page=ts2)
    page = pagtor.page(number)
    if userclass == 'True':
        return render(request, 'pros1.html', {'page': page, 'proname': proname, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html', {'page': page, 'proname': proname, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})

def pro_chaxun_bycretime(request):
    print('这是项目看板页面根据项目创建时间筛选显示项目的视图函数')
    time = request.GET.get('time')
    number = request.GET.get('num')
    userclass = request.GET.get('userclass')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    print(time,type(time))
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 2
    if not number:
        number = 1
    time1 = time.strip("'")
    time2 = time1.split(",")
    pros = Pros.objects.filter(createtime__year__in=time2,status=1)
    print(pros)
    for i in pros:
        i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", i.chargeperson.strip("[]"))
        i.participant = re.sub("[0-9\!\%\[\]\'\。]", "", i.participant.strip("[]"))
        i.createtime = str(i.createtime).replace("-", ".")
    print(pros)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pros, per_page=ts2)
    page = pagtor.page(number)
    if userclass == 'True':
        return render(request, 'pros1.html', {'page': page, 'time': time, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html', {'page': page, 'time': time, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})


def pro_chaxun_bycretuser(request):
    print('这是项目看板页面根据项目创建人筛选显示项目的视图函数')
    creatuser = request.GET.get('creatuser')
    number = request.GET.get('num')
    userclass = request.GET.get('userclass')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 3
    if not number:
        number = 1
    print(creatuser)
    if creatuser:
        creatuser1 = creatuser.strip("'")
        creatuser2 = creatuser1.split(",")
        print(creatuser)
    pros = Pros.objects.filter(createprouser__in=creatuser2,status=1)
    for i in pros:
        i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", i.chargeperson.strip("[]"))
        i.participant = re.sub("[0-9\!\%\[\]\'\。]", "", i.participant.strip("[]"))
        i.createtime = str(i.createtime).replace("-", ".")
    print('pros', pros)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pros, per_page=ts2)
    page = pagtor.page(number)
    if userclass == "True":
        return render(request, 'pros1.html',
                      {'page': page, 'creatuser': creatuser, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html',
                      {'page': page, 'creatuser': creatuser, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})


def pro_chaxun_byxmjd(request):
    print('这是项目看板页面根据项目进度筛选显示项目的视图函数')
    xmjd = request.GET.get('xmjd')
    userclass = request.GET.get('userclass')
    number = request.GET.get('num')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 4
    if not number:
        number = 1
    print(xmjd, userclass)
    xmjd1 = xmjd.strip("'")
    xmjd2 = xmjd1.split(",")
    print(xmjd2)
    pros = Pros.objects.filter(prostatus__in=xmjd2,status=1)
    for i in pros:
        i.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", i.chargeperson.strip("[]"))
        i.participant = re.sub("[0-9\!\%\[\]\'\。]", "", i.participant.strip("[]"))
        i.createtime = str(i.createtime).replace("-", ".")
    print(pros)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pros, per_page=ts2)
    page = pagtor.page(number)
    if userclass == 'True':
        return render(request, 'pros1.html', {'page': page, 'xmjd': xmjd, 'userclass': userclass, 'username':username,'userid':userid,'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html', {'page': page, 'xmjd': xmjd, 'userclass': userclass,'username':username,'userid':userid, 'flag': flag,'ts':ts2})


def pro_chaxun_bychargeperson(request):
    print('这是根据负责人筛选项目的视图函数')
    charperson = request.GET.get('charperson')
    userclass = request.GET.get('userclass')
    number = request.GET.get('num')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 5
    if not number:
        number = 1
    print(charperson, userclass)
    charperson1 = charperson.strip("'")
    charperson2 = charperson1.split(",")
    print(charperson2)
    pross = Pros.objects.none()
    for j in charperson2:
        pro = Pros.objects.filter(chargeperson__contains=j,status=1)
        print(pro, '**********')
        # for i in pro:
        #     for s in pross:
        #         if i != s:
        #             i.chargeperson = i.chargeperson.strip("[]")
        #             i.participant = i.participant.strip("[]")
        #             i.createtime = str(i.createtime).replace("-", ".")
        pross = chain(pross, pro)
        pross =list(set([iterm for iterm in pross]))
    for a in pross:
        a.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", a.chargeperson.strip("[]"))
        a.participant = re.sub("[0-9\!\%\[\]\'\。]", "", a.participant.strip("[]"))
        a.createtime = str(a.createtime).replace("-", ".")
    print(pross)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pross, per_page=ts2)
    page = pagtor.page(number)
    if userclass == 'True':
        return render(request, 'pros1.html',{'page': page, 'charperson': charperson, 'userclass': userclass, 'username':username,'userid':userid,'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html',{'page': page, 'charperson': charperson, 'userclass': userclass, 'username':username,'userid':userid,'flag': flag,'ts':ts2})

def pro_chaxun_byparticipant(request):
    print('这是根据参与人筛选项目的视图函数')
    participant = request.GET.get('participant')
    userclass = request.GET.get('userclass')
    number = request.GET.get('num')
    username = request.GET.get('username')
    userid = request.GET.get('userid')
    ts = request.GET.get('ts')
    ts1 = request.session.get('ts')
    if not ts1:
        if ts:
            request.session['ts'] = int(ts)
        else:
            request.session['ts'] = 10
    else:
        if ts:
            if ts1 != int(ts):
                request.session['ts'] = int(ts)
        else:
            request.session['ts'] = ts1
    flag = 6
    if not number:
        number = 1
    print(participant, userclass)
    participant1 = participant.strip("'")
    participant2 = participant1.split(",")
    print(participant2)
    pross = Pros.objects.none()
    for j in participant2:
        pro = Pros.objects.filter(participant__contains=j,status=1)
        print(pro, '**********')
        # for i in pro:
        #     for s in pross:
        #         if i != s:
        #             i.chargeperson = i.chargeperson.strip("[]")
        #             i.participant = i.participant.strip("[]")
        #             i.createtime = str(i.createtime).replace("-", ".")
        pross = chain(pross, pro)
        pross = list(set([iterm for iterm in pross]))
    for a in pross:
        a.chargeperson = re.sub("[0-9\!\%\[\]\'\。]", "", a.chargeperson.strip("[]"))
        a.participant = re.sub("[0-9\!\%\[\]\'\。]", "", a.participant.strip("[]"))
        a.createtime = str(a.createtime).replace("-", ".")
    print(pross)
    ts2 = request.session.get('ts')
    pagtor = Paginator(pross, per_page=ts2)
    page = pagtor.page(number)
    if userclass == 'True':
        return render(request, 'pros1.html',{'page': page, 'participant': participant, 'userclass': userclass,'username':username,'userid':userid,'flag': flag,'ts':ts2})
    else:
        return render(request, 'pros2.html',{'page': page, 'participant': participant, 'userclass': userclass, 'username':username,'userid':userid,'flag': flag,'ts':ts2})

# def pro_chaxun(request):
#     print('这是select页面根据年份显示项目的view1111')
#     time = request.GET.get('time')
#     time = time.split('-')[0]
#     print(time)
#     # Proinputs = Input.objects.filter(pub_date__year=time)
#     Users = list(User.objects.filter(input__pub_date__year=time).values('username','input__mark','input__pub_date','input__xmjd'))
#     print(Users)
#     if Users:
#         # Users = serializers.serialize("json",Users)
#         # return JsonResponse({'Proinputs':Proinputs},safe=False)
#         # return render(request,'select.html',{'Users':Users})
#         return JsonResponse({'Users':Users})
#     else:
#         return HttpResponse('0')


# def pro_chaxun2(request):
#     print('这是select页面根据年份显示项目的view2222')
#     time = request.GET.get('time')
#     time = time.split('-')[0]
#     print(time)
#     # Proinputs = Input.objects.filter(pub_date__year=time).values()
#     Users = list(User.objects.filter(input__pub_date__year=time).values())
#     print(Users)
#     if Users:
#         # Proinputs = serializers.serialize("json",Proinputs)
#         # return JsonResponse({'Proinputs':Proinputs},safe=False)
#         # return render(request,'select.html',{'Users':Users})
#         return JsonResponse({'Users':Users})
#     else:
#         return HttpResponse('0')


# @check_login
def select_to_index2(request):
    print('这是跳转至index2.heml的view')
    # tag = request.session['user_id']
    id = request.GET.get("id")
    userid = request.GET.get("userid")
    print(id, userid)
    inputs = Input.objects.filter(Q(tag_id=userid) & Q(id=id))
    print(inputs)
    return render(request, 'index2.html', {'inputs': inputs})


def upload(request):
    return render(request, 'upload.html')


@api_view(['POST'])
def fulfill(request):
    request.encoding = 'utf-8'
    data = request.POST
    print(data)
    tpl = DocxTemplate('template.docx')
    context = {
               # 'myescvar': 'It can be escaped with a "|e" jinja filter in the template too : < ',
               # 'nlnp': R(
               #     'Here is a multiple\nlines\nstring\aand some\aother\aparagraphs\aNOTE: the current character styling is removed'),
               # 'mylisting': Listing('the listing\nwith\nsome\nlines\nand special chars : <>&\f ... and a page break'),
               # 'page_break': R('\f'),
               # 'col_labels': ['fruit', 'vegetable', 'stone', 'thing'],
               # 'tbl_contents': [
               #     {'label': 'yellow', 'cols': ['banana', 'capsicum', 'pyrite', 'taxi']},
               #     {'label': 'red', 'cols': ['apple', 'tomato', 'cinnabar', 'doubledecker']},
               #     {'label': 'green', 'cols': ['guava', 'cucumber', 'aventurine', 'card']},
               # ]
               'first1': R(data['first1']),'first2': R(data['first2']),'first3': R(data['first3']),'first4': R(data['first4']),
                'first5': R(data['first5']),'first6': R(data['first6']),'first7': R(data['first7']),'first8': R(data['first8']),
                'first9': R(data['first9']),'first10': R(data['first10']),'first11':R(data['first11']),'first12':R(data['first12']),
                'first13': R(data['first13']),'first14':R(data['first14']),'first15':R(data['first15']),'first16':R(data['first16']),
                'first17': R(data['first17']),'first18':R(data['first18']),'first19':R(data['first19']),'first20':R(data['first20']),
                'first21': R(data['first21']),'first22':R(data['first22']),'first23':R(data['first23']),'first24':R(data['first24']),
                'first25': R(data['first25']),'first26':R(data['first26']),'first27':R(data['first27']),'first28':R(data['first28']),
                'first29': R(data['first29']),'first30':R(data['first30']),'first31':R(data['first31']),'first32':R(data['first32']),
                'first33': R(data['first33']),'first34':R(data['first34']),'first35':R(data['first35']),'first36': R(data['first36']),
                'first37':R(data['first37']),'first38':R(data['first38']),'first39':R(data['first39']),'first40':R(data['first40']),
                'first41': R(data['first41']),'first42':R(data['first42']),'first43':R(data['first43']),'first44':R(data['first44']),
                'first45': R(data['first45']),'first46':R(data['first46']),'first47':R(data['first47']),'first48':R(data['first48']),
                'first49': R(data['first49']),'first50':R(data['first50']),'first51':R(data['first51']),'first52':R(data['first52']),
                'first53': R(data['first53']),'first54':R(data['first54']),'first55':R(data['first55']),'first56':R(data['first56']),
                'first57': R(data['first57']),'first58':R(data['first58']),'first59':R(data['first59']),'first60':R(data['first60']),
                'first61': R(data['first61']),'first62':R(data['first62']),'first63':R(data['first63']),'first64':R(data['first64']),'first65':R(data['first65']),
               }
    tpl.render(context)
    tpl.save('output/test.docx')
    return render(request, 'index.html')


@api_view(['GET'])
def download(request):
    filename = 'test.docx'
    filepath = "output/"
    response = StreamingHttpResponse(read_file(os.path.join(filepath, filename), 512))
    response['Content-Type'] = 'application/msword'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    # time.sleep(10)
    return response


@api_view(['POST'])
def save(request):
    data = request.POST
    print(data,'########')
    # tag = request.session['user_id']
    mark = request.POST.get('mark')
    tag = request.POST.get('userid')
    csbj = request.FILES.get('csbj')
    csdx = request.FILES.get('csdx')
    xxxq = request.FILES.get('xxxq')
    tgxyq = request.FILES.get('tgxyq')
    pjxyq = request.FILES.get('pjxyq')
    csal = request.FILES.get('csal')
    hxxxgys = request.FILES.get('hxxxgys')
    cssj = request.FILES.get('cssj')
    csdd = request.FILES.get('csdd')
    cslc = request.FILES.get('cslc')
    cshj = request.FILES.get('cshj')
    csjilu = request.FILES.get('csjilu')
    csjlun = request.FILES.get('csjlun')
    csjg = request.FILES.get('csjg')
    xmjd = request.POST.get('xmjd')
    print('xmjd', xmjd, 'mark', mark)
    proid = Pros.objects.filter(proname=mark).values()[0]['id']
    print(proid)

    q = Input(tag_id=tag, input_1=data['first1'], input_2=data['first2'], input_3=data['first3'],
              input_4=data['first4'], input_5=data['first5'], input_6=data['first6'],
              input_7=data['first7'], input_8=data['first8'], input_9=data['first9'], input_10=data['first10'],
              input_11=data['first11'],input_12=data['first12'],
              input_13=data['first13'],input_14=data['first14'],input_15=data['first15'],input_16=data['first16'],input_17=data['first17'],input_18=data['first18'],
              input_19=data['first19'],input_20=data['first20'],input_21=data['first21'],input_22=data['first22'],input_23=data['first23'],input_24=data['first24'],
              input_25=data['first25'],input_26=data['first26'],input_27=data['first27'],input_28=data['first28'],input_29=data['first29'],input_30=data['first30'],
              input_31=data['first31'],input_32=data['first32'],input_33=data['first33'],input_34=data['first34'],input_35=data['first35'],input_36=data['first36'],
              input_37=data['first37'],input_38=data['first38'],input_39=data['first39'],input_40=data['first40'],input_41=data['first41'],input_42=data['first42'],
              input_43=data['first43'],input_44=data['first44'],input_45=data['first45'],input_46=data['first46'],input_47=data['first47'],input_48=data['first48'],
              input_49=data['first49'],input_50=data['first50'],input_51=data['first51'],input_52=data['first52'],input_53=data['first53'],input_54=data['first54'],
              input_55=data['first55'],input_56=data['first56'],input_57=data['first57'],input_58=data['first58'],input_59=data['first59'],input_60=data['first60'],
              # input_61=data['first61'],input_62=data['first62'],input_63=data['first63'],input_64=data['first64'],input_65=data['first65'],
              pub_date=timezone.now(), mark=data['mark'],
              csbj=csbj, csdx=csdx, xxxq=xxxq, tgxyq=tgxyq, pjxyq=pjxyq, csal=csal,
              hxxxgys=hxxxgys, cssj=cssj, csdd=csdd, cslc=cslc, cshj=cshj, csjilu=csjilu, csjlun=csjlun, csjg=csjg,
              pro_id=proid)
    q.save()
    return HttpResponse('object python', status=200)


def file_name(file):
    if file:
        return file.name
    else:
        return None


def read_file(file_name, size):
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


def upload_file(request, filename):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f_path = 'files/temp/' + filename + '.docx'
            createDoc(f_path)
            if handle_uploaded_file(request.FILES['file'], f_path):
                time.sleep(3)
                scanDoc(f_path)
                return f_path
            else:
                return -1
        else:
            return 0
    else:
        return 1


'''def download(request):
    uuid_str = uuid.uuid4().hex
    result = upload_file(request,uuid_str)
    print(result)
    if result == -1:
        return render(request,'download.html',{'form':"write file wrong"})
    elif result == 0:
        return render(request, 'download.html', {'form': "form is unvalid"})
    elif result == 1:
        return render(request, 'download.html', {'form': "upload must use post method"})
    else :
        return render(request, 'download.html', {'form':"window.open('http://"+request.get_host()+'/'+result+"')"})

import win32com.client
word = win32com.client.Dispatch('ket.Application')
doc = word.Documents.Add('files/example.html')
doc.SaveAs('example.docx', FileFormat=0)
doc.Close()
word.Quit()

import win32com
from win32com.client import Dispatch, DispatchEx
word = Dispatch('Word.Application') # 打开word应用程序
# word = DispatchEx('Word.Application') #启动独立的进程
word.Visible = 0 # 后台运行,不显示
word.DisplayAlerts = 0 # 不警告
path = 'D:/project/task/mysite/ttt.docx' # word文件路径
doc = word.Documents.Open(FileName=path, Encoding='gbk')
# content = doc.Range(doc.Content.Start, doc.Content.End)
# content = doc.Range()
print '----------------'
print '段落数: ', doc.Paragraphs.count
# 利用下标遍历段落
for i in range(len(doc.Paragraphs)):
  para = doc.Paragraphs[i]
  print para.Range.text
print '-------------------------'
# 直接遍历段落
for para in doc.paragraphs:
  print para.Range.text
  # print para #只能用于文档内容全英文的情况
doc.Close() # 关闭word文档
# word.Quit #关闭word程序
'''

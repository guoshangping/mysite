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
from django.http import FileResponse
from itertools import product


def get_files(request):
    # fileresponse的方式
    # file_path = os.getcwd() + "/static/all_test/"
    # file_path = file_path + "我.pdf"
    # file = open(file_path, 'rb')
    # response = FileResponse(file)
    # response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path("模板.pdf"))
    # return response

    # HttpResponse的方式
    file_path = os.getcwd() + "/static/all_test/"

    file_path = file_path + "我.pdf"
    print(file_path)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path("模板.pdf"))
        return response


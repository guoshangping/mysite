from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
import django.utils.timezone as timezone
from xuanxing.models import ProductsDetail
from testm.models import Projects
from xuanxing.models import  ManageUser


# 最新表
class Doc(models.Model):
    id = models.BigAutoField(primary_key=True)
    filesize = models.IntegerField(blank=True, null=True)
    #存储文件 名字  营业执照
    file_name = models.CharField(max_length=200, default="无")
    # 选择项目，厂商之后,百度 - 营业执照.pdf
    upload_filename = models.CharField(max_length=200, default="")
    stat = (
                (1, "未上传"),
                (2, "已上传"),
                (3, "审核通过"),
                (4, "审核不通过"),
                (5, "不涉及"),
            )
    status = models.SmallIntegerField(default=1, choices=stat)
    pro_id = models.ForeignKey(Projects, on_delete=models.SET_NULL, null=True,   verbose_name="项目名称")
    pro_name = models.CharField(max_length=200, default="无")
    vend_id = models.ForeignKey(ProductsDetail,  on_delete=models.SET_NULL, null=True,verbose_name="厂商名称")
    vend_name = models.CharField(max_length=200, default="无")
    create_time = models.DateTimeField("上传日期",default=timezone.now)
    download_time = models.CharField(max_length=200)
    remark = models.TextField(verbose_name='备注')
    check_remark = models.TextField(verbose_name='审核备注',default="")

    # 标志必要，公共，其他材料
    flag=models.IntegerField(blank=True, null=True)


class Doc_log(models.Model):
    user_id = models.ForeignKey(ManageUser, on_delete=models.SET_NULL, null=True, verbose_name='操作人')
    s_time = models.DateTimeField(verbose_name='操作时间', default=timezone.now)
    operation = models.CharField(max_length=200, verbose_name='操作详情')

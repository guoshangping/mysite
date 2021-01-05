from django.db import models
from xuanxing.models import Index
from xuanxing.models import ProductsDetail
from xuanxing.models import ProductsType
from products.models import Products
import django.utils.timezone as timezone
from xuanxing.models import ManageUser


# Create your models herine.

class Pro_speed(models.Model):
    speed_name = models.CharField(max_length=30, verbose_name='项目进度')


# 测试项目模型
class Projects(models.Model):
    # 测试案例ID
    id = models.BigAutoField(primary_key=True)
    # 创建时间
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    # 项目名称
    project_name = models.CharField(max_length=20, verbose_name='项目名称')
    # 项目进度
    # project_speed = models.IntegerField(choices=Speed_Name, verbose_name='项目进度')
    project_speed = models.ManyToManyField(Pro_speed, related_name='pro_sp', db_table='pro_sp', verbose_name='项目进度')
    # 创建人
    create_user = models.ForeignKey(ManageUser, related_name='create_user', on_delete=models.SET_NULL, null=True,
                                    verbose_name='创建人')
    # 负责人
    deal_user = models.ManyToManyField(ManageUser, related_name='dealname', db_table='deal_users', verbose_name='负责人')
    # 参与人
    members = models.ManyToManyField(ManageUser, related_name='membersname', db_table='members_users',
                                     verbose_name='参与人')
    # 厂商名称
    vend_prod = models.ManyToManyField(ProductsDetail, related_name='project_prod', db_table='projects_prods',
                                       verbose_name='厂商名称')
    # 产品子类
    product_subclass = models.ManyToManyField(ProductsType, related_name='subclass', db_table='sub_class',
                                              verbose_name='产品子类')
    # 项目上会状态
    meeting_status = models.CharField(max_length=20, verbose_name='上会状态', null=True, blank=True, default="0")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.project_name)

    class Meta:
        db_table = 'projects_t'
        verbose_name = '测试项目'
        verbose_name_plural = '测试项目'
        unique_together = ('project_name',)


# 进度时间
class Sp_time(models.Model):
    pid = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, verbose_name='项目id')
    s_time = models.DateTimeField(verbose_name='开始时间', default=timezone.now)
    e_time = models.DateTimeField(verbose_name='结束时间', default='2020-12-31 01:01:01')

    status = models.CharField(max_length=30, verbose_name='状态', default='未启动')
    name = models.CharField(max_length=30, default="", verbose_name='项目名称')


# 测试案例模型
class TestCase(models.Model):
    # 测试案例ID
    id = models.BigAutoField(primary_key=True)
    # 案例(三级)指标
    case_name = models.ForeignKey(Index, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='案例(三级指标)名称')
    project_name = models.ForeignKey(Projects, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='测试项目名称')
    # 案例名称
    # case_name = models.CharField(max_length=100,verbose_name='测试案例名称')
    # 测试时间
    test_date = models.CharField(max_length=20, verbose_name='测试时间', default="_____年___月___日")
    # 测试位置
    test_location = models.CharField(max_length=10, choices=(('YQ', u'洋桥'), ('DXH', u'稻香湖')), default='YQ',
                                     verbose_name="测试地点")
    # 测试产品名
    prod_name = models.CharField(max_length=20, verbose_name='产品名', default='')
    # 厂商名
    vend_name = models.CharField(max_length=20, verbose_name='供应商', default='')
    # 测试目的
    test_purpose = models.TextField(verbose_name='测试目的')
    # 测试设计
    test_design = models.TextField(verbose_name='测试设计')
    # 测试条件
    test_conditions = models.TextField(verbose_name='测试条件')
    # 测试步骤
    test_procedure = models.TextField(verbose_name='测试步骤')
    # 预期结果
    expected_results = models.TextField(verbose_name='预期结果')
    # 测试结果
    test_result = models.TextField(verbose_name='测试结果', default="□通过  □部分通过  □未通过  □未测试")
    # 签名
    sign = models.TextField(verbose_name='签名', default="测试人员____________________       供应商______________________")
    # 备注
    remark = models.TextField(verbose_name='备注', default="“通过”需满足全部要求")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.case_name)

    class Meta:
        db_table = 'case_t'
        verbose_name = '测试案例'
        verbose_name_plural = '测试案例'
        unique_together = ('case_name',)


class Reports_groups(models.Model):
    group_name = (
        (0, u'协助组',),
        (1, u'作业组',),
    )
    group_str = ''
    name = models.CharField(max_length=200, verbose_name='姓名', blank=True)
    department = models.CharField(max_length=200, verbose_name='部门', blank=True)
    contacts = models.CharField(max_length=20, verbose_name='联系方式', blank=True)
    responsibilities = models.CharField(max_length=200, verbose_name='职责', blank=True)
    group_flag = models.IntegerField(choices=group_name, verbose_name='组标识', default=0)

    def __unicode__(self):
        return self.name

    def __str__(self):
        group_dic = {0: '协助组', 1: '作业组'}
        if self.group_flag in group_dic:
            self.group_str = group_dic[self.group_flag]
        return "组别: {}     |     部门: {}    |     姓名: {}".format(self.group_str, self.department, self.name)

    # return self.group_str+'|'+self.department+'|'+self.name
    class Meta:
        db_table = 'groups_t'
        verbose_name = '测试报告|小组组成'
        verbose_name_plural = '测试报告|小组组成'


class Conclusion(models.Model):
    vend_product = models.ForeignKey(Products, related_name='conclusion_product', on_delete=models.SET_NULL, null=True,
                                     verbose_name='供应商产品')
    pass_index = models.CharField(max_length=20, verbose_name='通过性', blank=True)
    evaluate_index = models.CharField(max_length=200, verbose_name='评价性', blank=True)

    def __unicode__(self):
        return self.vend_product

    def __str__(self):
        return "供应商产品: {}     |     通过性: {}    |     评价性: {}".format(self.vend_product, self.pass_index,
                                                                     self.evaluate_index)

    # return str(self.vend_product)+'|'+self.pass_index+'|'+self.evaluate_index

    class Meta:
        db_table = 'conclusion_t'
        verbose_name = '测试报告|产品测试结论'
        verbose_name_plural = '测试报告|产品测试结论'
        unique_together = ('vend_product',)


class Executes(models.Model):
    execute_name = models.CharField(max_length=20, verbose_name='实施阶段')
    responsible_party = models.CharField(max_length=20, verbose_name='责任方')
    start_time = models.DateField('开始时间', default=timezone.now)
    end_time = models.DateField('结束时间', default=timezone.now)
    execute_description = models.CharField(max_length=200, verbose_name='实施描述')

    def __unicode__(self):
        return self.execute_name

    def __str__(self):
        return self.execute_name + ' | ' + self.responsible_party + ' |  ' + str(self.start_time) + ' | ' + str(
            self.end_time)

    class Meta:
        db_table = 'executes_t'
        verbose_name = '测试报告|实施时间'
        verbose_name_plural = '测试报告|实施时间'
        unique_together = ('execute_name',)


# 测试报告模型
class Reports(models.Model):
    # from docxtpl import DocxTemplate, RichText

    flow = '    采购部组织召开选型测试启动会，候选选型供应商代表签到，学习测试工作纪律，提交测试文件并进行测试顺序抽签。' \
           '\r    候选选型供应商按照抽签次序分成两组进行测试。每家供应商只能推荐1个型号的设备进行测试，原则上每家供应商测试时间为1天。' \
           '\r    按照抽签次序，首先由供应商人员负责安装调试，时间为30分钟左右，在安装调试过程中可以更换机具，供应商授权代表确认可以开始测试后，' \
           '不再允许更换备件或整机。' \
           '\r    供应商授权代表确认可以开始测试后，供应商测试操作员进行测试操作，每测试一个用例，建行测试记录员当场记录测试结果，测试结果由建行人' \
           '员及供应商授权代表共同签字确认。对于测试结果描述的涂改，需测试记录员与供应商授权代表共同签名，并注明涂改原因。' \
 \
        # flows = {{ flow | safe}}
    '''	organization_des ='        本次测试由财务会计部采购部牵头成立选型测试小组，相关组织机构职责如下：\n' \
                      '       【选型组织】财务会计部采购部负责选型测试工作的牵头组织，负责测试计划推进以及参测单位之间的问题、资源协调\n' \
                      '       【选型需求（管理）部门】XXXX负责提出选型测试需求；参与产品调研、测试案例编写和选型测试工作；参与选型测试实施过程管理；' \
                      '参与测试报告的汇总、编写。\n ' \
                      '       【选型测试单位】XXXX负责协助提出选型测试需求；负责编写测试方案、测试计划、测试用例及测试需要的其他技术资料；' \
                      '负责进行选型需求分析和调研；负责选型的具体实施，记录和保存测试过程数据；组织起草选型测试报告；负责保管选型测试样品、' \
                      '录音录像和过程资料。'
                      '''
    from django.utils.safestring import mark_safe
    # organization_des = mark_safe(RichText("    aa\n    bb"))

    organization_des = '    本次测试由财务会计部采购部牵头成立选型测试小组，相关组织机构职责如下：' \
                       '\r    【选型组织】财务会计部采购部负责选型测试工作的牵头组织，负责测试计划推进以及参测单位之间的问题、资源协调。' \
                       '\r    【选型需求（管理）部门】XXXX负责提出选型测试需求；参与产品调研、测试案例编写和选型测试工作；参与选型测试实施过程管理；' \
                       '参与测试报告的汇总、编写。' \
                       '\r    【选型测试单位】XXXX负责协助提出选型测试需求；负责编写测试方案、测试计划、测试用例及测试需要的其他技术资料；' \
                       '负责进行选型需求分析和调研；负责选型的具体实施，记录和保存测试过程数据；组织起草选型测试报告；负责保管选型测试样品、' \
                       '录音录像和过程资料。'

    # 测试项目名称
    project_name = models.ForeignKey(Projects, related_name='reports_project', on_delete=models.SET_NULL, blank=True,
                                     null=True, verbose_name='测试项目名称')
    # 报告名称
    report_name = models.CharField(max_length=200, verbose_name='报告名称')
    # 测试背景(ect需求概述)
    test_background = models.TextField(verbose_name='测试背景', blank=True)
    # 测试对象(需求概述)
    test_object = models.TextField(verbose_name='测试对象', blank=True)
    # 选型需求文档(需求概述)
    test_demand = models.FileField(upload_to='upload', verbose_name='需求文档', blank=True)
    # 测试方法(通过性文档)
    pass_index = models.FileField(upload_to='upload', verbose_name='通过性文档', blank=True)
    # 测试方法(评价性文档)
    evaluate_index = models.FileField(upload_to='upload', verbose_name='评价性文档', blank=True)
    # 测试方法(验证性文档)
    # Pass_index = models.FileField(verbose_name='通过性文档上传')
    # 测试案例文档
    test_case = models.FileField(upload_to='upload', verbose_name='测试案例', blank=True)
    # 选项组织(组织架构)
    organization_framework = models.TextField(verbose_name='组织架构', default=organization_des)
    # organization_framework = HTMLField(verbose_name='组织架构', default=organization_des)
    # 组织架构(小组组成)
    group_part = models.ManyToManyField(Reports_groups, blank=True, related_name='report_group',
                                        db_table='report_groups', verbose_name='小组组成')
    # 候选选型供应商产品
    prod_vend = models.ManyToManyField(Products, related_name='report_prod', blank=True, db_table='reports_prods',
                                       verbose_name='候选选型产品供应商')
    # 测试时间( 测试计划)
    test_time = models.ManyToManyField(Executes, related_name='report_execute', blank=True, db_table='report_executes',
                                       verbose_name='测试时间')
    # 测试地点( 测试计划)
    test_location = models.CharField(max_length=200, blank=True, verbose_name='测试地点')
    # 测试流程
    test_flow = models.TextField(verbose_name='测试流程', blank=True, default=flow)
    # 测试环境
    test_environment = models.TextField(verbose_name='测试环境', blank=True)
    # 测试记录(测试情况)
    test_records = models.TextField(verbose_name='测试记录', blank=True)
    # 测试结果
    test_results = models.TextField(verbose_name='测试结果', blank=True)
    # 测试结论
    test_conclusion = models.ManyToManyField(Conclusion, blank=True, related_name='prod_conclusion',
                                             db_table='products_conclusion', verbose_name='测试结论')

    def __unicode__(self):
        return self.report_name

    def __str__(self):
        return str(self.report_name)

    class Meta:
        db_table = 'reports_t'
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告'
        unique_together = ('report_name',)


class Score(models.Model):
    class Meta:
        verbose_name = '打分工具'
        verbose_name_plural = '打分工具'


class Dongtai(models.Model):
    s_time = models.DateTimeField(verbose_name='操作时间', default=timezone.now)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, verbose_name='项目id')
    operation = models.CharField(max_length=200, verbose_name='操作进度')


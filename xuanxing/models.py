from django.db import models
from django.contrib.admin.models import LogEntry
# Create your models here.
import django.utils.timezone as timezone
import testm


# 产品架构表
class ProductStructure(models.Model):
    # 架构ID
    id = models.BigAutoField(primary_key=True)
    # 架构名称(9大类)
    product_structure_name = models.CharField(max_length=100, verbose_name='架构名称')
    # 架构标识
    product_structure_flag = models.CharField(max_length=100, verbose_name='架构标识', default="0")
    # 创建时间
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.product_structure_name)

    class Meta:
        db_table = 'product_structure_t'
        verbose_name = '测试架构'
        verbose_name_plural = '测试架构'


# 案例文档
class AnliDoc(models.Model):
    id = models.BigAutoField(primary_key=True)
    doc_name = models.CharField(max_length=100, verbose_name="案例文档名称")
    project_id = models.ForeignKey("testm.Projects", on_delete=models.CASCADE, null=True, verbose_name='项目id')
    reserve1 = models.CharField(max_length=100, verbose_name='预留字段1', default="")
    reserve2 = models.CharField(max_length=100, verbose_name='预留字段2', default="")
    reserve3 = models.CharField(max_length=100, verbose_name='预留字段3', default="")
    reserve4 = models.CharField(max_length=100, verbose_name='预留字段4', default="")
    reserve5 = models.CharField(max_length=100, verbose_name='预留字段5', default="")

    def __unicode__(self):
        return self.doc_name

    def __str__(self):
        return str(self.doc_name)

    class Meta:
        db_table = 'anlidoc_t'
        verbose_name = '案例文档'
        verbose_name_plural = '案例文档'


# 测试案例二级分类表
class CaseMiddleType(models.Model):
    id = models.BigAutoField(primary_key=True)
    m_type_name = models.CharField(max_length=100, verbose_name="案例二级分类")
    doc_name = models.ForeignKey(AnliDoc, on_delete=models.CASCADE, blank=True, null=True, verbose_name='案例文档名称')
    md_project = models.ForeignKey("testm.Projects", on_delete=models.CASCADE, null=True, verbose_name='项目id')

    # is_delete =

    def __unicode__(self):
        return self.m_type_name

    def __str__(self):
        return str(self.m_type_name)

    class Meta:
        db_table = 'casemiddletype_t'
        verbose_name = '案例二级分类'
        verbose_name_plural = '案例二级分类'


# 测试案例小类表
class CaseSamllType(models.Model):
    id = models.BigAutoField(primary_key=True)
    m_type = models.ForeignKey(CaseMiddleType, on_delete=models.CASCADE, blank=True, null=True,
                               verbose_name='二级分类名称')
    s_type_name = models.CharField(max_length=200, verbose_name="案例小类")
    doc_name = models.ForeignKey(AnliDoc, on_delete=models.CASCADE, blank=True, null=True, verbose_name='案例文档名称')
    project = models.ForeignKey("testm.Projects", on_delete=models.CASCADE, null=True, verbose_name='项目id')

    def __unicode__(self):
        return self.s_type_name

    def __str__(self):
        return str(self.s_type_name)

    class Meta:
        db_table = 'casesmalltype_t'
        verbose_name = '案例小类'
        verbose_name_plural = '案例小类'


class CaseDocx(models.Model):
    # 案例ID
    id = models.BigAutoField(primary_key=True)
    case_type = models.ForeignKey(CaseSamllType, on_delete=models.CASCADE, blank=True, null=True, verbose_name='小类名称')
    case_id = models.TextField(verbose_name='案例编号')
    test_goal = models.TextField(verbose_name='测试目的')
    pre_condition = models.TextField(verbose_name='预置条件')
    test_steps = models.TextField(verbose_name='测试步骤')
    expect_result = models.TextField(verbose_name='预期结果')
    test_result = models.TextField(verbose_name='实测结果')
    test_conclusion = models.TextField(verbose_name='测试结论')
    remark = models.TextField(verbose_name='备注')
    check_person = models.TextField(verbose_name='审核人员', default="操作员： 复核员： ")
    # 创建时间
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    reserve1 = models.CharField(max_length=100, verbose_name='预留字段1', default="")
    reserve2 = models.CharField(max_length=100, verbose_name='预留字段2', default="")
    reserve3 = models.CharField(max_length=100, verbose_name='预留字段3', default="")
    reserve4 = models.CharField(max_length=100, verbose_name='预留字段4', default="")
    reserve5 = models.CharField(max_length=100, verbose_name='预留字段5', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.case_id)

    class Meta:
        db_table = 'case_docx_t'
        verbose_name = '测试案例'
        verbose_name_plural = '测试案例'


class OptionsType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=100, verbose_name='权限类型名称')

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.type_name)

    class Meta:
        db_table = 'options_type_t'
        verbose_name = '权限类型表'
        verbose_name_plural = '权限类型表'


class Options(models.Model):
    id = models.BigAutoField(primary_key=True)
    option_name = models.CharField(max_length=100, verbose_name='权限名称')

    option_type = models.ForeignKey(OptionsType, related_name='option_type', on_delete=models.CASCADE, null=True,
                                    verbose_name='权限类型')

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.option_name)

    class Meta:
        db_table = 'options_t'
        verbose_name = '权限表'
        verbose_name_plural = '权限表'


class Role(models.Model):
    # 用户ID
    id = models.BigAutoField(primary_key=True)
    rolename = models.CharField(max_length=100, verbose_name='角色名称')
    desc = models.CharField(max_length=100, verbose_name='权限描述', default="")
    option = models.ManyToManyField(Options, related_name='user_options', db_table='user_options_t', verbose_name='权限')
    # 创建时间
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.rolename)

    class Meta:
        db_table = 'role_t'
        verbose_name = '权限管理'
        verbose_name_plural = '权限管理'


class ManageUser(models.Model):
    # 用户ID
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, verbose_name='用户名称')
    user_mobile = models.CharField(max_length=100, verbose_name='用户手机号')
    user_email = models.CharField(max_length=100, verbose_name='用户邮箱')
    user_workid = models.CharField(max_length=100, verbose_name='员工ID')
    rz_time = models.CharField(max_length=100, verbose_name='入职时间')
    user_status = models.CharField(max_length=100, verbose_name='状态', default="0")
    user_role = models.ManyToManyField(Role, related_name='user_role', db_table='user_roles', verbose_name='用户角色')
    # 123的Md5加密 202cb962ac59075b964b07152d234b70
    user_pwd = models.CharField(max_length=100, verbose_name='用户密码', default="202cb962ac59075b964b07152d234b70")
    # 创建时间
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = 'manage_user_t'
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'


class ProductsType(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=100, verbose_name='项目AB标识', blank=True, null=True, default="A")
    struct_name = models.ForeignKey(ProductStructure, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='产品大类')
    prod_type = models.CharField(max_length=100, verbose_name='产品类型', blank=True, null=True)
    child_type = models.CharField(max_length=100, verbose_name='产品子类', blank=True, null=True)
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.struct_name)

    class Meta:
        db_table = 'productstype_t'
        verbose_name = '产品类型明细'
        verbose_name_plural = '产品类型明细'


class ProductsDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=100, verbose_name='项目AB标识', blank=True, null=True, default="A")
    product_type = models.ForeignKey(ProductsType, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='产品大中小类')
    vend_tactics = models.TextField(verbose_name='厂商策略', blank=True, null=True, default="")
    lifecycle = models.TextField(verbose_name='生命周期', blank=True, null=True, default="")
    performance_type = models.TextField(verbose_name='性能分类', blank=True, null=True, default="")
    vend_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='厂商名称')
    product_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='产品名称')
    main_index = models.TextField(verbose_name='主要技术指标', blank=True, null=True, default="")
    apply_scene = models.TextField(verbose_name='应用场景', blank=True, null=True, default="")
    work_scope = models.TextField(verbose_name='部署范围', blank=True, null=True, default="")
    work_years = models.CharField(max_length=100, blank=True, null=True, verbose_name='使用年限')
    mark_info = models.TextField(verbose_name='备注', blank=True, null=True, default="")
    creation_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    flag = models.CharField(verbose_name='修改记号(0:原始 1:修改或者新增)', max_length=100, default="0")
    test_flag = models.CharField(verbose_name='参测记号(0:不参测 1:参测)', max_length=100, default="1")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.product_name)

    class Meta:
        db_table = 'productsdetail_t'
        verbose_name = '产品明细'
        verbose_name_plural = '产品明细'


# 一级指标表
class FirstIndex(models.Model):
    # 一级指标ID
    id = models.BigAutoField(primary_key=True)
    # 一级指标名称
    first_index = models.CharField(max_length=100, verbose_name='一级指标')

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.first_index

    class Meta:
        db_table = 'first_index_x'
        verbose_name = '一级指标'
        verbose_name_plural = '一级指标'


# 二级指标表
class TwoIndex(models.Model):
    # 指标关系ID
    id = models.BigAutoField(primary_key=True)
    # 一级指标
    first_index = models.ForeignKey(FirstIndex, on_delete=models.CASCADE, verbose_name='一级指标', null=True)
    # 二级指标
    two_index = models.CharField(max_length=100, verbose_name='二级指标')
    # 指标说明
    index_explanation = models.TextField(verbose_name='指标说明')
    # 二级指标ID
    index_number = models.CharField(max_length=100, verbose_name='二级指标ID', null=True)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.two_index)

    class Meta:
        db_table = 'two_index_x'
        verbose_name = '二级指标'
        verbose_name_plural = '二级指标'


# 三级指标表（三级指标）
class Index(models.Model):
    # 指标ID
    id = models.BigAutoField(primary_key=True)
    # 项目名称
    project_name = models.CharField(max_length=100, verbose_name='项目名称', blank=True, null=True, default="项目A")

    # 产品类别ID
    prod_class = models.ForeignKey(ProductsType, on_delete=models.CASCADE, verbose_name='产品类别')
    # 一级指标ID
    first_index = models.ForeignKey(FirstIndex, on_delete=models.CASCADE, verbose_name='一级指标', null=True)
    # 二级指标ID
    two_index = models.ForeignKey(TwoIndex, related_name='twoindex', on_delete=models.CASCADE, verbose_name='二级指标',
                                  null=True)
    # 指标说明
    index_explain = models.CharField(max_length=200, null=True, blank=True, verbose_name='指标说明')
    # 指标名称
    index_name = models.CharField(max_length=200, verbose_name='指标名称')
    # 指标描述
    index_description = models.TextField(verbose_name='指标描述', null=True, blank=True)
    # 指标id
    index_id = models.CharField(max_length=200, verbose_name='指标id')
    # 案例编号
    anli_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='案例编号')
    # 测试类型
    test_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="测试类型")
    # 工具
    tool = models.CharField(max_length=100, verbose_name='工具', null=True, blank=True)
    # 备注
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    # 标记(修改记号(0:原始 1:修改或者新增))
    flag = models.CharField(verbose_name='修改记号(0:原始 1:修改或者新增)', max_length=100, default="0")

    def __unicode__(self):
        return self.index_name

    def __str__(self):
        return self.index_name

    class Meta:
        db_table = 'index_x'
        verbose_name = '三级指标'
        verbose_name_plural = '三级指标'


class Log(models.Model):
    user_id = models.ForeignKey(ManageUser, on_delete=models.CASCADE, null=True, verbose_name='操作人')
    s_time = models.DateTimeField(verbose_name='操作时间', default=timezone.now)
    operation = models.CharField(max_length=200, verbose_name='操作')


class AnliMap(models.Model):
    id = models.BigAutoField(primary_key=True)
    anli_key = models.CharField(max_length=200, null=True, verbose_name='案例字段key')
    anli_name = models.CharField(max_length=200, null=True, verbose_name='案例字段名')

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.anli_name)

    class Meta:
        db_table = 'anli_map_t'
        verbose_name = '案例map表'
        verbose_name_plural = '案例map表'


# 考核 选型测试事项
class XuanXingRank(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, verbose_name='事项名称')
    changshang_num = models.CharField(max_length=200, null=True, verbose_name='厂商数')
    anli_num = models.CharField(max_length=200, null=True, verbose_name='案例数')
    hj_level = models.CharField(max_length=200, null=True, verbose_name='环境复杂程度')
    xuanxing_type = models.CharField(max_length=200, null=True, verbose_name='选型类型')
    hj_score = models.CharField(max_length=200, null=True, verbose_name='环境复杂系数')
    anli_score = models.CharField(max_length=200, null=True, verbose_name='测试案例系数')
    scale_score = models.CharField(max_length=200, null=True, verbose_name='测试规模系数')
    stage_percent = models.CharField(max_length=200, null=True, verbose_name='各阶段占比,如 3,3,4')
    fangan_percent = models.CharField(max_length=200, null=True, verbose_name='方案准备占比,如 戴路_0.1,张勇_0.9')
    hj_percent = models.CharField(max_length=200, null=True, verbose_name='环境准备占比,如 戴路_0.1,张勇_0.9')
    exec_percent = models.CharField(max_length=200, null=True, verbose_name='案例执行占比,如 戴路_0.1,张勇_0.9')
    xuanxing_score = models.CharField(max_length=200, null=True, verbose_name='该选型事项的分数')
    is_delete = models.CharField(max_length=200, verbose_name='删除标记', default="0")
    is_rank = models.CharField(max_length=200, verbose_name='是否评分', default="0")
    input_user = models.CharField(max_length=200, null=True, verbose_name='录入人')
    huping = models.CharField(max_length=200, verbose_name='互评', default="")
    hp_score = models.CharField(max_length=200, verbose_name='同事互评总分', default="")
    final_score = models.CharField(max_length=200, verbose_name='最终分', default="")
    lingdao_input = models.CharField(max_length=200, verbose_name='领导输入分', default="")
    markinfo = models.CharField(max_length=200, verbose_name='备注信息', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'xuanxing_rank_t'
        verbose_name = '选型评分表'
        verbose_name_plural = '选型评分表'


class ZhuangXiangRank(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, verbose_name='事项名称')
    shuxing = models.CharField(max_length=200, null=True, verbose_name='属性')
    zhuanxiang_percent = models.CharField(max_length=200, null=True, verbose_name='人员占比 如 戴路_0.1,张勇_0.9')
    zhuanxiang_desc = models.CharField(max_length=200, null=True, verbose_name='描述')
    zhuanxiang_score = models.CharField(max_length=200, null=True, verbose_name='该选型事项的分数')
    is_delete = models.CharField(max_length=200, verbose_name='删除标记', default="0")
    is_rank = models.CharField(max_length=200, verbose_name='是否评分', default="0")
    input_user = models.CharField(max_length=200, null=True, verbose_name='录入人')
    huping = models.CharField(max_length=200, verbose_name='互评', default="")
    hp_score = models.CharField(max_length=200, verbose_name='同事互评总分', default="")
    final_score = models.CharField(max_length=200, verbose_name='最终分', default="")
    lingdao_input = models.CharField(max_length=200, verbose_name='领导输入分', default="")
    markinfo = models.CharField(max_length=200, verbose_name='备注信息', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'zhuanxiang_rank_t'
        verbose_name = '专项工作评分表'
        verbose_name_plural = '专项工作评分表'


class ChushiRank(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, verbose_name='事项名称')
    chushi_percent = models.CharField(max_length=200, null=True, verbose_name='人员占比 如 戴路_10,张勇_90')
    chushi_desc = models.CharField(max_length=200, null=True, verbose_name='描述')
    chushi_score = models.CharField(max_length=200, null=True, verbose_name='该事项的分数')
    is_delete = models.CharField(max_length=200, verbose_name='删除标记', default="0")
    is_rank = models.CharField(max_length=200, verbose_name='是否评分', default="0")
    input_user = models.CharField(max_length=200, null=True, verbose_name='录入人')
    huping = models.CharField(max_length=200, verbose_name='互评', default="")
    hp_score = models.CharField(max_length=200, verbose_name='同事互评总分', default="")
    final_score = models.CharField(max_length=200, verbose_name='最终分', default="")
    lingdao_input = models.CharField(max_length=200, verbose_name='领导输入分', default="")
    markinfo = models.CharField(max_length=200, verbose_name='备注信息', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'chushi_rank_t'
        verbose_name = '处室工作评分表'
        verbose_name_plural = '处室工作评分表'


class AddScoreRank(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, verbose_name='事项名称')
    add_percent = models.CharField(max_length=200, null=True, verbose_name='人员占比 如 戴路_0.1,张勇_0.9')
    add_desc = models.CharField(max_length=200, null=True, verbose_name='描述')
    add_score = models.CharField(max_length=200, null=True, verbose_name='该事项的分数')
    is_delete = models.CharField(max_length=200, verbose_name='删除标记', default="0")
    is_rank = models.CharField(max_length=200, verbose_name='是否评分', default="0")
    input_user = models.CharField(max_length=200, null=True, verbose_name='录入人')
    huping = models.CharField(max_length=200, verbose_name='互评', default="")
    hp_score = models.CharField(max_length=200, verbose_name='同事互评总分', default="")
    final_score = models.CharField(max_length=200, verbose_name='最终分', default="")
    lingdao_input = models.CharField(max_length=200, verbose_name='领导输入分', default="")
    markinfo = models.CharField(max_length=200, verbose_name='备注信息', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'add_score_rank_t'
        verbose_name = '加分项评分表'
        verbose_name_plural = '加分项评分表'


class MinusScoreRank(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, verbose_name='事项名称')
    minus_percent = models.CharField(max_length=200, null=True, verbose_name='人员占比 如 戴路_0.1,张勇_0.9')
    minus_desc = models.CharField(max_length=200, null=True, verbose_name='描述')
    minus_score = models.CharField(max_length=200, null=True, verbose_name='该事项的分数')
    is_delete = models.CharField(max_length=200, verbose_name='删除标记', default="0")
    is_rank = models.CharField(max_length=200, verbose_name='是否评分', default="0")
    input_user = models.CharField(max_length=200, null=True, verbose_name='录入人')
    huping = models.CharField(max_length=200, verbose_name='互评', default="")
    hp_score = models.CharField(max_length=200, verbose_name='同事互评总分', default="")
    final_score = models.CharField(max_length=200, verbose_name='最终分', default="")
    lingdao_input = models.CharField(max_length=200, verbose_name='领导输入分', default="")
    markinfo = models.CharField(max_length=200, verbose_name='备注信息', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'minus_score_rank_t'
        verbose_name = '扣分项评分表'
        verbose_name_plural = '扣分项评分表'


class FinalScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    score = models.CharField(max_length=200, verbose_name='每个人的最终分', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.score)

    class Meta:
        db_table = 'final_score_t'
        verbose_name = '每个人的最终分表'
        verbose_name_plural = '每个人的最终分表'


class KaoheJili(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='姓名', default="")
    date = models.CharField(max_length=200, verbose_name='日期', default="")
    jili = models.CharField(max_length=200, verbose_name='激励', default="")
    level = models.CharField(max_length=200, verbose_name='档次', default="")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'kaohe_jili_t'
        verbose_name = '每个人的激励和档次'
        verbose_name_plural = '激励与档次表'


class ProjectDaily(models.Model):
    id = models.BigAutoField(primary_key=True)
    pj_id = models.ForeignKey("testm.Projects", on_delete=models.CASCADE, null=True, verbose_name='项目id')
    name = models.CharField(max_length=200, verbose_name='项目或日报名称', default="")
    type = models.CharField(max_length=200, verbose_name='类型(日报or会议)', default="")
    file_name = models.CharField(max_length=200, verbose_name='上传的材料名称', default="")
    mark = models.TextField(verbose_name='备注')
    check_mark = models.TextField(verbose_name='审核备注')
    up_time = models.DateTimeField(verbose_name='上传时间', default=timezone.now)
    download_time = models.CharField(max_length=200,default="")
    stat = (
        (1, "未上传"),
        (2, "已上传"),
        (3, "审核通过"),
        (4, "审核不通过"),
        (5, "不涉及"),
    )
    status = models.SmallIntegerField(default=1, choices=stat)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'project_daily_t'
        verbose_name = '项目日报表'
        verbose_name_plural = '项目日报表'

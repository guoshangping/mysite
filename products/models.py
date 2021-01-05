from django.db import models
from django.contrib.admin import ListFilter
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Group


# Create your models here.
# 产品位置模型
class ProductsLocation(models.Model):
    # 产品位置ID
    id = models.BigAutoField(primary_key=True)
    # 产品位置名称
    location_type_name = models.CharField(max_length=20, verbose_name="产品位置名称")

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.location_type_name)

    class Meta:
        db_table = 'product_location_t'
        verbose_name = '产品位置字典表'
        verbose_name_plural = '产品位置表'
        unique_together = ('location_type_name',)


# 产品类型模型
class ProductsTypes(models.Model):
    # 产品类型ID
    id = models.BigAutoField(primary_key=True)
    # 产品位置类型
    location_type = models.ForeignKey(ProductsLocation, on_delete=models.CASCADE, verbose_name="产品位置", default=1)
    # 产品类型名称
    prod_type_name = models.CharField(max_length=50, verbose_name="产品类型名称")


    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.prod_type_name)

    class Meta:
        db_table = 'product_types_t'
        verbose_name = '产品类型字典表'
        verbose_name_plural = '产品类型字典表'
        unique_together = ('location_type', 'prod_type_name',)


# 产品类别表
class ProductsClass(models.Model):
    # 产品类别ID
    id = models.BigAutoField(primary_key=True)
    # 产品位置ID
    location_type = models.ForeignKey(ProductsLocation, on_delete=models.CASCADE, verbose_name="产品位置")
    # 产品类型ID
    prod_type = models.ForeignKey(ProductsTypes, on_delete=models.CASCADE, verbose_name="产品类型")
    # 产品子类
    prod_subclass = models.CharField(max_length=100, verbose_name="产品子类")
    # 厂商策略
    vend_strategy = models.TextField(verbose_name="厂商策略")
    # 生命使用周期
    life_cycle_state = models.CharField(max_length=5, verbose_name="生命使用周期")
    # 性能分类
    performance_classification = models.CharField(max_length=5, verbose_name="性能分类")
    # 主要技术指标
    main_specifications = models.TextField(null=True, verbose_name="主要技术指标")
    # 部署范围
    deployment_scope = models.CharField(max_length=100, verbose_name="部署范围")
    # 应用范围
    application_scenario = models.TextField(verbose_name="应用范围", blank=True)
    # 建议生产使用年限
    recommended_production_life = models.CharField(max_length=100, verbose_name="建议生产使用年限", default='无限期')
    # 备注
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.location_type) + '—' + str(
            self.prod_type) + '—' + self.prod_subclass + '—' + self.performance_classification

    class Meta:
        db_table = 'product_class_t'
        verbose_name = '产品分类信息'
        verbose_name_plural = '产品分类信息'
        unique_together = ('location_type', 'prod_type', 'prod_subclass', 'performance_classification')


# 产品模型
class Products(models.Model):
    # 产品ID
    id = models.BigAutoField(primary_key=True)
    # 产品名称
    prod_name = models.CharField(max_length=100, verbose_name="产品(设备)名称")
    # 厂商名称
    vend_name = models.CharField(max_length=100, verbose_name="厂商名称")
    # 产品类型ID
    prod_class = models.ForeignKey(ProductsClass, on_delete=models.CASCADE, verbose_name="产品类别", null=True)
    # 技术指标
    technical_index = models.TextField(verbose_name="技术指标", blank=True, null=True)

    def __unicode__(self):
        return self.prod_name

    def __str__(self):
        return str(self.prod_name) + ' | ' + str(self.vend_name)

    class Meta:
        db_table = 'products_t'
        verbose_name = '产品信息'
        verbose_name_plural = '产品信息'
        unique_together = ('prod_name', 'vend_name')


# 产品指标模型
class Statistics(models.Model):
    pass


class SingleTextInputFilter(ListFilter):
    """
    renders filter form with text input and submit button
    """
    parameter_name = None
    parameter_name2 = None
    template = "textinput_filter.html"

    def __init__(self, request, params, model, model_admin):
        super(SingleTextInputFilter, self).__init__(
            request, params, model, model_admin)
        if self.parameter_name is None and self.parameter_name2 is None:
            raise Exception(
                "The list filter '%s' does not specify "
                "a 'parameter_name'." % self.__class__.__name__)
        # print(type(params))
        # params = {'vend_name':request.GET.get("vend_name"),'prod_name':request.GET.get("prod_name")}
        # print(params)
        if self.parameter_name in params and self.parameter_name2 in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value
            value2 = params.pop(self.parameter_name2)
            self.used_parameters[self.parameter_name2] = value2
        # print(self.used_parameters)

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, None)

    def value2(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name2, None)

    def has_output(self):
        return True

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name, self.parameter_name2]

    def choices(self, cl):
        all_choice = {
            'selected': self.value() is None,
            'selected2': self.value2() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name, self.parameter_name2]),
            'display': _('All'),
        }
        return ({
                    'get_query': cl.params,
                    'current_value': self.value(),
                    'current_value2': self.value2(),
                    'all_choice': all_choice,
                    'parameter_name': self.parameter_name,
                    'parameter_name2': self.parameter_name2,
                },)


class VendProdNameListFilter(SingleTextInputFilter):
    title = '厂商名-产品名输入'
    parameter_name = 'vend_name'
    parameter_name2 = 'prod_name'

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(vend_name__icontains=self.value())
        if self.value2():
            queryset = queryset.filter(prod_name__icontains=self.value2())
        return queryset

from django_filters import rest_framework as drf_filters

from .models import Post, Category, Tag


class PostFilter(drf_filters.FilterSet):
    # 等价于查询条件created_time__year
    created_year = drf_filters.NumberFilter(
        field_name="created_time", lookup_expr="year", label='年份', help_text='根据年份过滤'
    )
    # 等价于查询条件created_time__month
    created_month = drf_filters.NumberFilter(
        field_name="created_time", lookup_expr="month", label='月份', help_text='根据月份过滤'
    )
    # 配合接口文档添加help_text
    category = drf_filters.ModelChoiceFilter(queryset=Category.objects.all(), help_text='根据分类过滤')
    tags = drf_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), help_text='根据标签过滤')

    class Meta:
        model = Post
        # category和tags不附加过滤条件的话直接传入, 也可直接通过视图集的filter_fields属性传入
        fields = ["category", "tags", "created_year", "created_month"]

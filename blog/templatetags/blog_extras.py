from django import template
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth

from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all()[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    # 统计每月发布的文章数
    # 方法一:
    # date_list = Post.objects.dates('created_time', 'month', order='DESC')
    # res = []
    # for date in date_list:
    #     post_count = Post.objects.filter(created_time__year=date.year, created_time__month=date.month).count()
    #     res.append((date, post_count))
    # return {
    #     'date_list': date_list
    # }

    # 方法二:
    return {
        # 按年份和月份分组
        'date_list': Post.objects.annotate(
            year=ExtractYear('created_time'), month=ExtractMonth('created_time')
        )
        # 生成只包含上一步分组结果的字典
            .values('year', 'month')
        # 排序
            .order_by('year', 'month')
        # 再次分组将year与month相同的元素聚合
            .annotate(post_count=Count('pk'))
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        # 按文章分类分组, 过滤分类下文章数量大于0的分类
        'category_list': Category.objects.annotate(post_count=Count('post')).filter(post_count__gt=0),
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        # 按文章标签分组, 过滤标签下文章数量大于0的标签
        'tag_list': Tag.objects.annotate(post_count=Count('post')).filter(post_count__gt=0),
    }

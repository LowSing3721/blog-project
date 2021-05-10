import re

from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.db.models import Q
from markdown import Markdown
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, action
from drf_yasg.utils import swagger_auto_schema

from .models import Post, Category, Tag
from .serializers import PostListSerializer, PostRetrieveSerializer, TagSerializer,\
    CategorySerializer
from .filters import PostFilter
from comment.serializers import CommentSerializer


# 非RESTful风格CBV
class PostListView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 5


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        # 文章阅读量+1
        post.increase_pv()
        # 创建Markdown对象
        md = Markdown(extensions=[
            'markdown.extensions.extra',  # 基础拓展
            'markdown.extensions.codehilite',  # 语法高亮拓展
            # 'markdown.extensions.toc',  # 自动生成目录拓展, 默认使用_数字称作为锚点
            TocExtension(slugify=slugify),  # 自动生成目录拓展, 使用标题名称作为锚点, 使用django的slugify函数处理中文标题
        ])
        # 使用第三方库Markdown将Markdown格式文本转换为HTML格式
        post.body = md.convert(post.body)
        # 取出body中的[TOC]目录用于其他地方
        # 不存在目录(Markdown标题文本)则不生成相关HTML
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


class PostFilterByCreatedTimeView(PostListView):
    def get_queryset(self):
        return super().get_queryset().filter(
            created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month')
        )


class PostFilterByCategoryView(PostListView):
    def get_queryset(self):
        cg = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cg)


class PostFilterByTagView(PostListView):
    def get_queryset(self):
        tg = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tg)


class PostSearchView(PostListView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        return super().get_queryset().filter(Q(title__contains=query) | Q(body__contains=query))


# 数据集: 把对同一个资源的不同操作, 集中到一个类中, 只需要继承不同action对应的混入类, 或使用快捷类
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """文章

    list:文章列表
    retrieve:文章详情
    list_comments:文章评论列表
    """
    queryset = Post.objects.all()  # 响应数据
    filterset_class = PostFilter  # 过滤器类

    def get_serializer_class(self):
        # 为不同的action定制不同的序列化器
        if self.action == 'list':
            return PostListSerializer
        else:
            return PostRetrieveSerializer

    # 自定义行为(action名称为函数名)
    @action(methods=['GET'], detail=True, url_path='comments')
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值(前提设置detail为True)获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论
        queryset = post.comment_set.all().order_by("-created_time")
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = CommentSerializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # 在接口文档中隐藏
    swagger_schema = None


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """文章分类

    list:
    文章分类列表
    retrieve:
    文章详情
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@swagger_auto_schema(methods=['GET'])
@api_view(http_method_names=['GET'])
def test(request):
    """测试接口"""
    return Response({'msg': 'hello'}, status.HTTP_200_OK)

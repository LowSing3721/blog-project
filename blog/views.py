import re

from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from markdown import Markdown
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import Blog, Category, Tag, Comment, MyUser
from .serializers import BlogListSerializer, BlogRetrieveSerializer, TagSerializer,\
    CategorySerializer, CommentSerializer
from .filters import BlogFilter
from .forms import CommentForm, BlogForm


class BlogListView(PaginationMixin, ListView):
    model = Blog
    template_name = 'blog/list.html'
    paginate_by = 5


class BlogDetail(DetailView):
    model = Blog
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)

        # 文章阅读量+1
        blog.increase_pv()

        # 防止XSS攻击: 在转换Markdown之前去除HTML标签
        blog.body = strip_tags(blog.body)

        # 创建Markdown对象
        md = Markdown(extensions=[
            'markdown.extensions.extra',  # 基础拓展
            'markdown.extensions.codehilite',  # 语法高亮拓展
            # 'markdown.extensions.toc',  # 自动生成目录拓展, 默认使用_数字称作为锚点
            TocExtension(slugify=slugify),  # 自动生成目录拓展, 使用标题名称作为锚点, 使用django的slugify函数处理中文标题
        ])
        # 使用第三方库Markdown将Markdown格式文本转换为HTML格式
        blog.body = md.convert(blog.body)

        # 取出body中的[TOC]目录用于其他地方
        # 不存在目录(Markdown标题文本)则不生成相关HTML
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        blog.toc = m.group(1) if m is not None else ''

        return blog


class BlogFilterByCreatedTimeView(BlogListView):
    def get_queryset(self):
        return super().get_queryset().filter(
            created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month')
        )


class BlogFilterByCategoryView(BlogListView):
    def get_queryset(self):
        cg = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cg)


class BlogFilterByTagView(BlogListView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)


class BlogFilterByAuthor(BlogListView):
    def get_queryset(self):
        author = get_object_or_404(MyUser, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(author=author)


class BlogSearchView(BlogListView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        return super().get_queryset().filter(Q(title__contains=query) | Q(body__contains=query))


@require_http_methods(['GET', 'POST'])
@login_required
def new_blog(request):
    if request.method == 'GET':
        return render(request, 'blog/newblog.html', context={
            'form': BlogForm()
        })
    else:
        form = BlogForm(request.POST)
        print(form)
        if form.is_valid():
            author = get_object_or_404(MyUser, pk=request.user.pk)
            blog = form.save(commit=False)
            blog.author = author
            blog.save()
            messages.add_message(request, messages.SUCCESS, '博客发布成功!', extra_tags='success')
            return redirect(blog)
        messages.add_message(request, messages.ERROR, '博客发布失败!', extra_tags='danger')
        return render(request, 'blog/newblog.html', context={
            'form': form
        })


@require_POST
@login_required
def new_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = get_object_or_404(MyUser, pk=request.user.pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.blog = blog
        comment.user = user
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功!', extra_tags='success')
        return redirect(blog)
    else:
        print(form.errors)
    messages.add_message(request, messages.ERROR, '评论发表失败!', extra_tags='danger')
    return render(request, 'blog/preview.html', context={
        'form': form,
        'Blog': blog,
    })


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()  # 响应数据
    filterset_class = BlogFilter  # 过滤器类

    def get_serializer_class(self):
        # 为不同的action定制不同的序列化器
        if self.action == 'list':
            return BlogListSerializer
        else:
            return BlogRetrieveSerializer

    # 自定义行为(action名称为函数名)
    @action(methods=['GET'], detail=True, url_path='comments')
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值(前提设置detail为True)获取到博客文章记录
        blog = self.get_object()
        # 获取文章下关联的全部评论
        queryset = blog.comment_set.all().order_by("-created_time")
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = CommentSerializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

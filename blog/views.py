import re

from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from markdown import Markdown
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin

from .models import Post, Category, Tag


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


def search(request):
    query = request.GET.get('query')
    if not query:
        messages.add_message(request, level=messages.ERROR, message='查询条件不能为空', extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__contains=query) | Q(body__contains=query))
    return render(request, 'blog/index.html', context={
        'object_list': post_list,
    })

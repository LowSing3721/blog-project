from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .forms import CommentForm
from .models import Comment
from .serializers import CommentSerializer
from blog.models import Post


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        # ModelForm的save方法用于提交表单数据至数据库, commit参数为False时不提交只返回绑定模型实例
        cm = form.save(commit=False)
        # 将评论绑定至文章
        cm.post = post
        # 手动提交
        cm.save()
        # 发送成功消息
        messages.add_message(request, messages.SUCCESS, '评论发表成功!', extra_tags='success')
        return redirect(post)
    # 发送失败消息
    messages.add_message(request, messages.ERROR, '评论发表失败!', extra_tags='danger')
    return render(request, 'comment/preview.html', context={
        'form': form,
        'post': post,
    })


class CommentViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ['post']

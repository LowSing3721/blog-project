from django import template

from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.inclusion_tag(filename='comment/inclusions/_comment_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    """评论表单"""
    if form is None:
        form = CommentForm()
    return {
        'post': post,
        'form': form,
    }


@register.inclusion_tag(filename='comment/inclusions/_comment_list.html', takes_context=True)
def show_comments(context, post):
    """评论列表"""
    # 正向查询
    comment_list = Comment.objects.filter(post=post)
    # 反向查询
    # comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count,
    }

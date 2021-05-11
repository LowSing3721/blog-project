from django import template
from markdown import markdown

from ..forms import CommentForm
from ..models import Comment

register = template.Library()


@register.inclusion_tag(filename='blog/inclusions/_comment_form.html', takes_context=True)
def show_comment_form(context, blog, form=None):
    """评论表单"""
    if form is None:
        form = CommentForm()
    return {
        'blog': blog,
        'form': form,
    }


@register.inclusion_tag(filename='blog/inclusions/_comment_list.html', takes_context=True)
def show_comments(context, blog):
    """评论列表"""
    comment_list = Comment.objects.filter(blog=blog)
    # 支持Markdown
    for comment in comment_list:
        comment.text = markdown(comment.text)
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count,
    }

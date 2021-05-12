from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from markdown import Markdown


class MyUser(AbstractUser):
    """博客用户/作者"""

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        verbose_name = '博客用户/作者'
        verbose_name_plural = verbose_name


class Category(models.Model):
    """博客分类"""
    name = models.CharField(max_length=100, verbose_name='博客分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """博客标签"""
    name = models.CharField(max_length=100, verbose_name='博客标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """博客"""
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='博客作者')
    title = models.CharField(max_length=70, verbose_name='博客标题')
    body = models.TextField(verbose_name='博客正文')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='博客摘要')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='博客分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='博客标签')
    created_time = models.DateTimeField(default=timezone.now, editable=False, verbose_name='发布时间')
    modified_time = models.DateTimeField(default=timezone.now, editable=False, verbose_name='最后修改时间')
    page_view = models.PositiveIntegerField(default=0, editable=False, verbose_name='博客阅读量')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # 如果摘要为空则自动取前54个字符为摘要
        if not self.excerpt:
            # 去除Markdown标记: Markdown文本 -> HTML文本 -> 纯文本
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 更新最后修改时间
        self.modified_time = timezone.now()

        super().save(*args, **kwargs)

    def increase_pv(self):
        self.page_view += 1
        self.save(update_fields=['page_view'])  # 使用update_fields提高效率

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class Comment(models.Model):
    """评论"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='评论用户')
    text = models.TextField(verbose_name='评论内容')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='评论文章')
    created_time = models.DateTimeField(default=timezone.now, editable=False, verbose_name='评论时间')

    def __str__(self):
        return f'{self.user}: {self.text[:20]}'

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

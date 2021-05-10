from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.html import strip_tags
from django.utils import timezone
from markdown import markdown


class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100, verbose_name='文章分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(max_length=100, verbose_name='文章标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Post(models.Model):
    """文章"""
    title = models.CharField(max_length=70, verbose_name='标题', help_text='标题帮助')
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(default=timezone.now, editable=False, verbose_name='发布时间')
    modified_time = models.DateTimeField(default=timezone.now, editable=False, verbose_name='最后修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    # 默认值为0, 不可从表单中修改的正整数字段
    page_view = models.PositiveIntegerField(default=0, editable=False, verbose_name='文章阅读量')
    # 关联到auth应用User模型的外键
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # 如果摘要为空则自动取前54个字符为摘要
        if not self.excerpt:
            # 将Markdown文本转换为纯文本:
            # 先使用markdown将Markdown文本转换为HTML文本, 再使用django内置工具strip_tags将HTML文本标签去除
            self.excerpt = strip_tags(markdown(self.body[:54], extensions=[
                'markdown.extensions.extra',  # 基础拓展
                'markdown.extensions.codehilite',  # 语法高亮拓展
            ]))

        # 更新最后修改时间
        self.modified_time = timezone.now()

        super().save(*args, **kwargs)

    def increase_pv(self):
        self.page_view += 1
        self.save(update_fields=['page_view'])  # 使用update_fields提高效率

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

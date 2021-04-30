from django.db import models
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(verbose_name='网址', blank=True)
    text = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(default=timezone.now, editable=False, verbose_name='评论时间')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return f'{self.name}: {self.text[:20]}'

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


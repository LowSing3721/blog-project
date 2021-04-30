from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User

from blog.models import Post, Category
from blog.templatetags.blog_extras import show_recent_posts


class TemplateTagTestCase(TestCase):
    """测试标签"""

    def setUp(self):
        self.cate = Category.objects.create(name='测试标签')
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin'
        )
        self.ctx = {}

    def test_show_recent_posts_with_posts(self):
        post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=self.cate,
            author=self.user,
        )
        # 创建上下文
        context = Context(show_recent_posts(self.ctx))
        # 创建模板
        template = Template(
            '{% load blog_extras %}'
            '{% show_recent_posts %}'
        )
        # 渲染模板
        expected_html = template.render(context)
        self.assertInHTML('<h3 class="widget-title">最新文章</h3>', expected_html)
        self.assertInHTML(f'<a href="{post.get_absolute_url()}">{post.title}</a>', expected_html)

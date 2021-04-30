import sys

from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from blog.models import Category, Post, Tag


class ModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@hellogithub.com',
            password='admin')
        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )

    def test_str(self):
        """测试__str__方法"""
        self.assertEqual(self.post.__str__(), self.post.title)
        tag = Tag.objects.create(name='测试标签')
        self.assertEqual(tag.__str__(), tag.name)

    def test_auto_populate_modified_time(self):
        """测试最终修改时间"""
        self.assertIsNotNone(self.post.modified_time)

        old_post_modified_time = self.post.modified_time
        self.post.body = '新的测试内容'
        self.post.save()
        self.post.refresh_from_db()
        self.assertGreaterEqual(self.post.modified_time, old_post_modified_time)

    def test_auto_populate_excerpt(self):
        """测试摘要"""
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) <= 54)

    def test_get_absolute_url(self):
        """测试get_absolute_url方法"""
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        """测试PV方法"""
        self.post.increase_pv()
        # 刷新该值为数据库中最新值
        self.post.refresh_from_db()
        self.assertEqual(self.post.page_view, 1)

        self.post.increase_pv()
        self.post.refresh_from_db()
        self.assertEqual(self.post.page_view, 2)



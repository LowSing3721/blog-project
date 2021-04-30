from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

from blog.models import Category, Tag, Post


class ViewTestCase(TestCase):
    def setUp(self):
        # User
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@hellogithub.com',
            password='admin'
        )

        # 分类
        self.cate1 = Category.objects.create(name='测试分类一')
        self.cate2 = Category.objects.create(name='测试分类二')

        # 标签
        self.tag1 = Tag.objects.create(name='测试标签一')
        self.tag2 = Tag.objects.create(name='测试标签二')

        # 文章
        self.post1 = Post.objects.create(
            title='测试标题一',
            body='测试内容一',
            category=self.cate1,
            author=self.user,
        )
        self.post1.tags.add(self.tag1)
        self.post1.save()

        self.post2 = Post.objects.create(
            title='测试标题二',
            body='测试内容二',
            category=self.cate2,
            author=self.user,
            created_time=timezone.now() - timedelta(days=100)
        )


class CategoryViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:category', kwargs={'pk': self.cate1.pk})
        self.url2 = reverse('blog:category', kwargs={'pk': self.cate2.pk})

    def test_visit_a_nonexistent_category(self):
        """测试获取标签"""
        url = reverse('blog:category', kwargs={'pk': 100})
        # 模拟客户端请求
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        """测试主页"""
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertContains(response, '暂时还没有发布的文章！')

    def test_with_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_qs = self.cate1.post_set.all().order_by('-created_time')
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])


class PostDetailViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.md_post = Post.objects.create(
            title='Markdown 测试标题',
            body='# 标题',
            category=self.cate1,
            author=self.user,
        )
        self.url = reverse('blog:detail', kwargs={'pk': self.md_post.pk})

    def test_good_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertContains(response, self.md_post.title)
        self.assertIn('post', response.context)

    def test_visit_a_nonexistent_post(self):
        url = reverse('blog:detail', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_increase_views(self):
        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.page_view, 1)

        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.page_view, 2)

    def test_markdownify_post_body_and_set_toc(self):
        response = self.client.get(self.url)
        self.assertContains(response, '文章目录')
        self.assertContains(response, self.md_post.title)

        post_template_var = response.context['post']
        # self.assertHTMLEqual(post_template_var.body_html, "<h1 id='标题'>标题</h1>")
        self.assertHTMLEqual(post_template_var.toc, '<li><a href="#标题">标题</li>')


class MoreTestCase(ViewTestCase):
    def test_tag_view(self):
        url = reverse('blog:tag', kwargs={'pk': self.tag1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        for post in resp.context['object_list']:
            self.assertIn(self.tag1, post.tags.all())

    def test_archive_view(self):
        url = reverse('blog:archive', kwargs={
            'year': self.post1.created_time.year,
            'month': self.post1.created_time.month,
        })
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        for post in resp.context['object_list']:
            self.assertEqual(post.created_time.year, self.post1.created_time.year)
            self.assertEqual(post.created_time.month, self.post1.created_time.month)

    def test_simple_search(self):
        url = reverse('blog:search')
        # 空查询
        resp = self.client.get(url, {'query': ''}, follow=True)
        self.assertRedirects(resp, reverse('blog:index'))
        self.assertIn('messages', resp.context)
        self.assertContains(resp, '查询条件不能为空')
        # 查询无结果
        resp = self.client.get(url, {'query': '自行车'}, follow=True)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 0)
        # 查询有结果
        resp = self.client.get(url, {'query': '测试'})
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 2)
        for post in resp.context['object_list']:
            self.assertIn('测试', post.title + post.body)

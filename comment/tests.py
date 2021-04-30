from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.template import Context, Template

from blog.models import Post, Category
from comment.models import Comment
from comment.forms import CommentForm
from comment.templatetags.comment_extras import show_comment_form, show_comments


class CommentTestCase(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title='测试文章',
            body='测试正文',
            category=Category.objects.create(name='测试分类'),
            author=User.objects.create_superuser(
                username='admin',
                password='admin'
            )
        )


class ModelTestCase(CommentTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.comment = Comment.objects.create(
            name='测试姓名',
            email='test@qq.com',
            text='测试内容',
            post=self.post,
        )

    def test_str(self):
        self.assertEqual(self.comment.__str__(), f'{self.comment.name}: {self.comment.text[:20]}')


class ViewTestCase(CommentTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('comment:comment', kwargs={'post_pk': self.post.pk})

    def test_method_not_allowed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 405)

    def test_not_found(self):
        resp = self.client.post(reverse('comment:comment', kwargs={'post_pk': 666}))
        self.assertEqual(resp.status_code, 404)

    def test_invalid_comment(self):
        invalid_data = {
            'email': 'test@qq'
        }
        resp = self.client.post(self.url, invalid_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'comment/preview.html')
        self.assertIn('post', resp.context)
        self.assertIn('form', resp.context)
        self.assertIn('messages', resp.context)
        self.assertContains(resp, '评论发表失败!')

    def test_valid_comment(self):
        valid_data = {
            'name': '测试姓名',
            'email': 'test@qq.com',
            'text': '测试内容',
            'post': self.post,
        }
        self.assertEqual(Comment.objects.count(), 0)
        # follow=True追踪重定向
        resp = self.client.post(self.url, valid_data, follow=True)
        self.assertRedirects(resp, self.post.get_absolute_url())
        self.assertIn('messages', resp.context)
        self.assertContains(resp, '评论发表成功!')
        self.assertEqual(Comment.objects.count(), 1)


class TemplateTagTestCase(CommentTestCase):
    def test_comment_form(self):
        context = Context(show_comment_form({}, self.post))
        self.assertIn('post', context)
        self.assertIn('form', context)
        template = Template(
            '{% load comment_extras %}'
            '{% show_comment_form post form %}'
        )
        expected_html = template.render(context)
        for field in CommentForm():
            label = '<label for="{}">{}：</label>'.format(field.id_for_label, field.label)
            self.assertInHTML(label, expected_html)
            self.assertInHTML(str(field), expected_html)
            self.assertInHTML(str(field.errors), expected_html)

    def test_comments(self):
        context = Context(show_comments({}, self.post))
        self.assertIn('comment_list', context)
        self.assertIn('comment_count', context)
        template = Template(
            '{% load comment_extras %}'
            '{% show_comments post %}'
        )

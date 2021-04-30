import os
import pathlib
import random
import sys

import django
import faker
from django.utils import timezone

# 将项目根目录添加到 Python 的模块搜索路径中
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR))
# 外部导入django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogproject.settings")
django.setup()
from blog.models import Category, Post, Tag
from comment.models import Comment
from django.contrib.auth.models import User


def clear_old_data():
    print('清空数据库旧数据')
    # User.objects.all().delete()
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comment.objects.all().delete()


def create_users():
    print('创建超级用户')
    User.objects.create_superuser('admin', 'admin@hellogithub.com', 'admin')


def create_categories():
    print('创建文章分类')
    category_list = ['Python学习笔记', '开源项目', '工具资源', '程序员生活感悟', 'test category']
    for cate in category_list:
        Category.objects.create(name=cate)


def create_tags():
    print('创建文章标签')
    tag_list = ['django', 'Python', 'Pipenv', 'Docker', 'Nginx', 'Elasticsearch',
                'Gunicorn', 'Supervisor', 'test tag']
    for tag in tag_list:
        Tag.objects.create(name=tag)


def create_posts():
    print('创建文章')
    # 实例化Faker对象, locale指定文本语言(默认英文)
    fake = faker.Faker(locale='zh_CN')
    for _ in range(100):
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        # 返回随机日期
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            # 返回随机句子
            title=fake.sentence().rstrip('.'),
            # 返回随机段落列表
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            author=User.objects.get(username='admin'),
        )
        post.tags.add(tag1, tag2)
        post.save()


def create_comments():
    print('创建评论')
    fake = faker.Faker(locale='zh_CN')
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_time
        # 评论时间取文章创建时间与当前时间的区间
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                name=fake.name(),
                email=fake.email(),
                url=fake.uri(),
                text=fake.paragraph(),
                created_time=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone()),
                post=post,
            )


if __name__ == '__main__':
    print('开始创建测试数据')
    clear_old_data()
    # create_users()
    create_categories()
    create_tags()
    create_posts()
    create_comments()
    print('创建测试数据结束')

from rest_framework import serializers

from .models import Blog, Category, Tag, MyUser, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username']


class BlogListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = MyUserSerializer()

    class Meta:
        model = Blog
        exclude = ['body', 'tags']


class BlogRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = MyUserSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

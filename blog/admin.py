from django.contrib import admin

from .models import Category, Tag, Blog, Comment, MyUser


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_time', 'modified_time']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created_time']


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MyUser, MyUserAdmin)

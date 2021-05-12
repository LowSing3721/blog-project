from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(prefix='api-blog', viewset=views.BlogViewSet, basename='blog')
router.register(prefix='api-tag', viewset=views.TagViewSet)
router.register(prefix='api-cate', viewset=views.CategoryViewSet)
router.register(prefix='api-comment', viewset=views.CommentViewSet)

app_name = 'blog'

urlpatterns = [
    # 前端页面
    path('list/', views.BlogListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.BlogDetail.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.BlogFilterByCreatedTimeView.as_view(), name='archive'),
    path('category/<int:pk>/', views.BlogFilterByCategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.BlogFilterByTagView.as_view(), name='tag'),
    path('author/<int:pk>/', views.BlogFilterByAuthor.as_view(), name='author'),
    path('create/', views.new_blog, name='create'),
    path('search', views.BlogSearchView.as_view(), name='search'),
    path('comment/<int:pk>', views.new_comment, name='comment'),

    # API页面
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]

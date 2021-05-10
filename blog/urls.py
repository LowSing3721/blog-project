from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# 注册视图集为API, 第一个参数为URL前缀, 第二个参数为视图集, 第三个参数为视图集生成的视图函数前缀(后缀为action)
router.register(prefix='posts', viewset=views.PostViewSet, basename='post')
router.register(prefix='tags', viewset=views.TagViewSet)
router.register(prefix='cates', viewset=views.CategoryViewSet)

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.PostFilterByCreatedTimeView.as_view(), name='archive'),
    path('category/<int:pk>/', views.PostFilterByCategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.PostFilterByTagView.as_view(), name='tag'),
    # path('search', views.search, name='search'),
    path('search', views.PostSearchView.as_view(), name='search'),
    # API视图
    path("api/", include(router.urls)),
    # 登录视图
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('test/', views.test),
]

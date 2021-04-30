from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('archive/<int:year>/<int:month>/', views.PostFilterByCreatedTimeView.as_view(), name='archive'),
    path('category/<int:pk>/', views.PostFilterByCategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', views.PostFilterByTagView.as_view(), name='tag'),
    path('search', views.search, name='search'),
]

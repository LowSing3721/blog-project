from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('comments', views.CommentViewSet)

app_name = 'comment'
urlpatterns = [
    path('<int:post_pk>/', views.comment, name='comment'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

from django.urls import path

from . import views


app_name = 'comment'
urlpatterns = [
    path('<int:post_pk>/', views.comment, name='comment')
]

from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    # path('change/', views.change_password, name='change'),
]

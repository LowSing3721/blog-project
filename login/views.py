from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_GET
from django.conf import settings

from .forms import LoginForm, RegisterForm
# 关联任意Django User拓展类
from blog.models import MyUser as User


INDEX_URL = settings.INDEX_URL


def login(request):
    if request.user.is_authenticated:
        return redirect(INDEX_URL)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 表单验证: 根据表单类字段属性验证
        error_dict = login_form.errors
        if not error_dict:
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 自定义验证: 除表单验证外的业务验证
            try:
                exist_user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                error_dict['_'] = '不存在该用户'  # 借用表单验证的ErrorDict类提供的error_dict变量
                context = {
                    'login_form': login_form,
                    'error_dict': error_dict,
                }
                return render(request, 'login/login.html', context=context)
            # 使用auth.hashers模块的快捷函数check_password判断明文和密文
            if not check_password(password=password, encoded=exist_user.password):
                error_dict['_'] = '密码不正确'
                context = {
                    'login_form': login_form,
                    'error_dict': error_dict,
                }
                return render(request, 'login/login.html', context=context)
            # 登录
            auth.login(request, user=exist_user)
            return redirect('blog:list')
        # 未通过表单验证
        else:
            context = {
                'login_form': login_form,
                'error_dict': error_dict,
            }
            return render(request, 'login/login.html', context=context)
    else:
        context = {
            'login_form': LoginForm()
        }
        return render(request, 'login/login.html', context=context)


def register(request):
    # 已登录用户跳转主页
    if request.user.is_authenticated:
        return redirect(INDEX_URL)
    # POST请求进一步处理
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        # 表单验证
        error_dict = register_form.errors
        if not error_dict:
            # 只有经过表单验证成功后才可使用cleaned_data属性
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            gender = register_form.cleaned_data.get('gender')
            # 用户名冲突验证
            same_name_user = User.objects.filter(username=username)
            if same_name_user:
                error_dict['_'] = '该用户名已存在'
                context = {
                    'error_dict': error_dict,
                    'register_form': register_form
                }
                return render(request, 'login/register.html', context=context)
            # 密码一致性验证
            if password != password2:
                error_dict['_'] = '两次输入密码不一致'
                context = {
                    'error_dict': error_dict,
                    'register_form': register_form
                }
                return render(request, 'login/register.html', context=context)
            try:
                # 使用auth模块内置的密码验证器
                validate_password(password=password, user=User)
            except ValidationError as ve:
                error_dict['_'] = ve
                # error_dict['_'] = password_validators_help_text_html(my_validators)
                context = {
                    'error_dict': error_dict,
                    'register_form': register_form
                }
                return render(request, 'login/register.html', context=context)
            # 邮箱冲突验证
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                error_dict['_'] = '该邮箱已被注册'
                context = {
                    'error_dict': error_dict,
                    'register_form': register_form
                }
                return render(request, 'login/register.html', context=context)
            # 验证通过, 跳转登录页面
            # 使用快捷函数make_password通过传入明文、盐和哈希算法生成密文
            User.objects.create(
                username=username, password=make_password(password=password, salt='hello-world'),
                email=email
            )
            return redirect('login:login')
        else:
            context = {
                'error_dict': error_dict,
                'register_form': register_form
            }
            return render(request, 'login/register.html', context=context)
    # 其他请求返回空表单
    else:
        context = {
            'register_form': RegisterForm()
        }
        return render(request, 'login/register.html', context=context)


@require_GET
def logout(request):
    auth.logout(request)
    return redirect(INDEX_URL)


# def change_password(request):
#     if not request.user.is_authenticated:
#         return redirect('login:login')
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         try:
#             validate_password(password)
#         except ValidationError as ve:
#             error_msg = ve
#             return render(request, 'login/list.html', {'error_msg': error_msg})
#         user = User.objects.get(username=request.user.get('user_name'))
#         user.password = make_password(password=password, salt='login')
#         user.save()
#         return HttpResponse('修改密码成功')
#     return redirect('login:index')

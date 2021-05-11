from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 分页
    'pure_pagination',
    # drf
    'rest_framework',
    # 过滤器
    'django_filters',
    # OpenAPI
    'drf_yasg',
    # 验证码
    'captcha',
    # 博客
    'blog.apps.BlogConfig',
    # 登录/注册系统
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogproject.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# 自定义用户类
AUTH_USER_MODEL = 'blog.MyUser'

# 主页
INDEX_URL = 'blog:list'

# django-pure-pagination设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 4,  # 分页条当前页前后应该显示的总页数（两边均匀分布，因此要设置为偶数），
    'MARGIN_PAGES_DISPLAYED': 2,  # 分页条开头和结尾显示的页数
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,  # 当请求了不存在页，显示第一页
}

# django-rest-framework设置
REST_FRAMEWORK = {
    # 设置 DEFAULT_PAGINATION_CLASS 后，将全局启用分页，所有 List 接口的返回结果都会被分页。
    # 如果想单独控制每个接口的分页情况，可不设置这个选项，而是在视图函数中进行配置
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # 这个选项控制分页后每页的资源个数
    "PAGE_SIZE": 10,
    # API默认操作权限
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
    # 过滤器后端, 需要安装django_filters
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 限流类
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    # 限流频率
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/min',
    }
}


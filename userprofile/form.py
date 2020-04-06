from django import forms  # 引入表单类
from django.contrib.auth.models import User  # 引入 User 模型


# 登录表单，继承 forms.Form 类
class UserLoginForm(forms.Form):  # forms.Form适用于不与数据库进行直接交互的功能
    username = forms.CharField()
    password = forms.CharField()
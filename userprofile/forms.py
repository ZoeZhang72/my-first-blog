from django import forms  # 引入表单类
from django.contrib.auth.models import User  # 引入 User 模型
from .models import Profile  # 引入 Profile 模型


# 登录表单
class UserLoginForm(forms.Form):  # forms.Form适用于不与数据库进行直接交互的功能，因为登录不需要对数据库改动
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(forms.ModelForm):  # 对数据库进行操作的表单，可以自动生成模型中已有的字段。
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):  # def clean_[字段]这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")


# 用户信息表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')

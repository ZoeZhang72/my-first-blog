from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,  logout
from django.http import HttpResponse
from .form import UserLoginForm


# Create your views here.

# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data  # .cleaned_data 清洗出合法数据产生一致的输出
            # 检验账号密码是否正确匹配数据库中的某个用户，如果均匹配则返回这个 user 对象
            user = authenticate(
                username=data['username'],
                password=data['password'])
            if user:
                # 将用户数据保存在 session 中实现登录动作
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号密码输入有误，请重新输入~")
        else:
            return HttpResponse("账号密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")
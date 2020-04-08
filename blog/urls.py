from django.contrib import admin
from django.urls import path, include  # 引入include方法,path为Django的路由语法

# 正在部署的应用的名称
app_name = 'article'

# 存放映射关系的列表 ,
urlpatterns = [
    path('admin/', admin.site.urls),

    # 配置app的url: 参数article/分配了app的访问路径; include将路径分给下一步处理; namespace可以保证反查到唯一的url,即使不同的app用了相同的url
    path('', include('article.urls')),

    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),

    path('password-reset/', include('password_reset.urls')),

    # 评论
    path('comment/', include('comment.urls', namespace='comment')),

]

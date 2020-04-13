from django.contrib import admin
from .models import Comment


# 将评论模块注册到后台
admin.site.register(Comment)

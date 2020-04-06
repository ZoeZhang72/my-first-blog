from django.contrib import admin
from .models import ArticlePost  # 添加models里的数据表ArticlePost

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

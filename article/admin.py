from django.contrib import admin
from .models import ArticlePost  # 添加models里的数据表ArticlePost
from .models import ArticleColumn


# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

# 注册文章栏目
admin.site.register(ArticleColumn)
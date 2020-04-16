# path将根路径为article的访问都分发给article这个app去处理。但是app通常有多个页面地址，因此需要app自己也有一个路由分发，就是article.urls
from django.urls import path
from . import views  # 引入views.py

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # path函数将url映射到视图，参数name用于反查url地址
    path(
        '',
        views.article_list,
        name='article_list'
    ),

    # 文章详情。<int:id>: path语法，用尖括号定义需要传递的参数，传递名叫id的整数到视图函数中去。
    path(
        'article-detail/<int:id>/',
        views.article_detail,
        name='article_detail'
    ),

    # 写文章
    path(
        'article-create/',
        views.article_create,
        name='article_create'
    ),

    # 安全删除文章
    path(
        'article-delete/<int:id>/',
        views.article_safe_delete,
        name='article_safe_delete'
    ),

    # 更新文章
    path(
        'article-update/<int:id>/',
        views.article_update,
        name='article_update'
    ),

    # 点赞 +1
    path(
        'increase-likes/<int:id>/',
        views.IncreaseLikesView.as_view(),
        name='increase_likes'
    ),
]

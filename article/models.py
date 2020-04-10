from django.db import models  # 对数据库的支持
from django.contrib.auth.models import User  # 导入内建的User模型。
from django.utils import timezone  # timezone 用于处理时间相关事务。
from django.urls import reverse
# 博客文章数据模型


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式, 外键ForeignKey解决一对多关系
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    total_views = models.PositiveIntegerField(default=0)

    # 文章标题。models.CharField为字符串字段, 用于保存较短的字符串.
    title = models.CharField(max_length=100)  # max_length用于定义数据库结构和验证数据

    # 文章正文。TextField 可以保存大量文本
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 内部类 Meta中的ordering定义了数据的排列方式。
    class Meta:
        ordering = ('-created',)  # -created表示将以创建时间的倒序排列

    # __str__方法定义了需要表示数据时应该显示的名称
    def __str__(self):
        return self.title
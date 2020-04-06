from django.db import models  # 对数据库的支持
from django.contrib.auth.models import User  # 导入内建的User模型。
from django.utils import timezone  # timezone 用于处理时间相关事务。

# 博客文章数据模型


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式, 外键ForeignKey解决一对多关系
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField为字符串字段, 用于保存较短的字符串.
    title = models.CharField(max_length=100)  # max_length用于定义数据库结构和验证数据

    # 文章正文。TextField 可以保存大量文本
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据,ordering是元组，只包含一个元素要加逗号.
    class Meta:
        ordering = ('-created',)  # 使模型返回的数据排列顺序为倒序.
    # 定义当调用对象的 str() 方法时的返回值内容

    def __str__(self):
        return self.title

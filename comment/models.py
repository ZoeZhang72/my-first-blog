from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost


# 博文的评论
class Comment(models.Model):
    article = models.ForeignKey(  # 外键 article是被评论的文章
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(  # 外键 user是评论的发布者
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]

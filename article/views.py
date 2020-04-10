from django.shortcuts import render, redirect  # redirect重定向模块
from .models import ArticlePost
import markdown
from django.http import HttpResponse
from .forms import ArticlePostForm  # 引入ArticlePostForm表单类
from django.contrib.auth.models import User  # 引入User模型
from django.core.paginator import Paginator  # 引入分页模块
from django.db.models import Q  # 引入 Q 对象
from comment.models import Comment
from django.contrib.auth.decorators import login_required


# 视图函数
def article_list(request):  # request与网页发来的请求有关
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
    else:
        search = ''
        article_list = ArticlePost.objects.all()
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    else:
        pass

    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # context定义了需要传递给模板的上下文
    context = {'articles': articles, 'order': order, 'search': search}
    # render变量：request是固定的request对象，context定义了需要传递给模块的上下文
    return render(request, 'article/list.html', context)


# 文章详情,参数id是Django自动生成用于索引数据表的主键(Primary Key)
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)  # 在所有文章中找出id值相符合的唯一一篇文章

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():  # Django内置方法:is_valid
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)  # 根据 id 获取需要删除的文章
        article.delete()  # 调用.delete()方法删除文章
        return redirect("article:article_list")  # 完成删除后返回文章列表
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
# 提醒用户登录
@login_required(login_url='/userprofile/login/')
def article_update(request, id):

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
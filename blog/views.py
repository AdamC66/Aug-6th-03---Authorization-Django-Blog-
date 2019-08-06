from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from blog.models import Article, Comment, ArticleForm, CommentForm
from blog.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def root(request):
    return HttpResponseRedirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/home')
    else:
        form = UserCreationForm()
    html_response = render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)


def home(request):
    context = {'date' : datetime.today().strftime('%Y-%m-%d'), 
    'articles': Article.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def article(request, id):
    form = CommentForm(request.POST)
    context = {'article': Article.objects.get(pk=id), 'form': form}
    return render(request, 'article.html', context)

def create_comment(request):
    article_id = request.POST['article']
    articlelink = Article.objects.filter(id=article_id).first()
    # name = request.POST['name']
    # message = request.POST['message']
    # new_comment = Comment(name=name, message=message, article=articlelink)
    # new_comment.save()
    form = CommentForm(request.POST)
    context = {'article': articlelink, 'form': form}
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = articlelink
        form.save()
        return HttpResponseRedirect(f'/article/{article_id}')
    else:
        return render(request, 'article.html', context)

@login_required
def new_article(request):
    form = ArticleForm(request.POST)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return HttpResponseRedirect('/home')
    return render(request, 'articleform.html', context)

@login_required
def edit(request, id):
    article = get_object_or_404(Article, pk=id, user=request.user.pk)
    form = ArticleForm(request.POST, instance=article)
    if request.method == 'POST':
        article = form.save(commit=False)
        article.user = request.user
        article.save()
        context = {'article':article}
        return render(request, 'article.html', context)
    else:
        context = {'article': article, 'form': form}
        return render(request, 'edit.html', context)

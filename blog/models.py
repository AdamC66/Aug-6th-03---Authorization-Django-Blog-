from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length = 255, null=False)
    body = models.TextField(blank = True, null=False)
    draft = models.BooleanField()
    published_date = models.DateField()
    author = models.CharField(max_length = 63, null = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return (f'{self.title}, By: {self.author}')


class Comment(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body', 'draft', 'published_date', 'author')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'message')
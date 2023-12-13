from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    tag = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_poll = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_responses(self):
        return self.responses.filter(parent=None)

    def is_poll(self):
        return False
    

class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='responses')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    def get_responses(self):
        return Response.objects.filter(parent=self)

class Blog(models.Model):
    tag = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_responses(self):
        return self.blog_responses.all()

class BlogResponse(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null=False, on_delete=models.CASCADE, related_name='blog_responses')
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

class Poll(models.Model):
    tag = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    options = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def is_poll(self):
        return True

class Choice(models.Model):
    poll = models.ForeignKey(Poll, null=False, on_delete = models.CASCADE, related_name='choices')
    text = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.text

class Track(models.Model):
    poll = models.ForeignKey(Poll, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
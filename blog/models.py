from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BlogPost(models.Model):
    owner = models.ForeignKey(User, name = 'owner', on_delete = models.CASCADE)
    slug = models.SlugField(name = 'slug')
    title = models.CharField(name = 'title', max_length = 255)
    intro = models.TextField(name = 'intro',max_length = 255)
    body = models.TextField(name = 'body')
    created_at = models.DateField(auto_now_add = True)
    
    class Meta:
        ordering = ('-created_at', )
    
class BlogComment(models.Model):
    owner = models.ForeignKey(User, name = 'owner', on_delete = models.CASCADE)
    post = models.ForeignKey(BlogPost, name = 'post', on_delete = models.CASCADE)
    body = models.TextField(name = 'body')
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering = ('-created_at', )
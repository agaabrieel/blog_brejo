from django import forms
from django.contrib.auth.models import User
from .models import BlogComment, BlogPost
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class CreateAccountForm(forms.Form):
    username = forms.CharField(max_length = 255, label = 'Seu nome de usuário.', required = True)
    email = forms.EmailField(label = 'Seu e-mail.', required = True)
    password = forms.CharField(max_length = 255, label = 'Sua senha.', required = True)
    
    def clean_email(self):
        data = self.cleaned_data['email']
        
        if User.objects.filter(email = data).count():
            raise ValidationError(_('Já existe um usuário cadastrado neste e-mail.'))
        
        return data
    
    def clean_username(self):
        data = self.cleaned_data['username']
        
        if User.objects.filter(username = data).count():
            raise ValidationError(_('Já existe um usuário cadastrado com este username.'))
        
        return data
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 255, label = 'Seu nome de usuário.', required = True)
    password = forms.CharField(required = True, max_length = 255, label = 'Sua senha')
    
    def clean_username(self):
        data = self.cleaned_data['username']
        
        if User.objects.filter(username = data).count() == 0:
            raise ValidationError(_('Usuário ou senha incorretos.'))
            
        
class CommentForm(forms.Form):
    body = forms.CharField(max_length = 1000, required = True)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(forms.Form, self).__init__(*args, **kwargs)
        
    def clean_body(self):
        data = self.cleaned_data['body']
        
        if not self.user.is_authenticated:
            raise ValidationError(_('Para comentar é preciso estar logado (y)'))
        
        
        return data      
        
    
class PostForm(forms.Form):
    title = forms.CharField(max_length = 255, required = True)
    intro = forms.CharField(max_length = 511, required = True)
    body = forms.CharField(max_length = 1023, required = True)
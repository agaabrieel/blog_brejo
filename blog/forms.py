from django import forms
from django.contrib.auth.models import User
from .models import BlogComment, BlogPost

class CreateAccountForm(forms.Form):
    username = forms.CharField(max_length = 255, label = 'Seu nome de usuário.', required = True)
    user_email = forms.EmailField(label = 'Seu e-mail.', required = True)
    user_password = forms.CharField(max_length = 255, label = 'Sua senha.', required = True)
        
class LoginForm(forms.Form):
    username_or_email = forms.ComboField(
                        fields = [forms.CharField(max_length = 255), forms.EmailField()], 
                        required = True, 
                        label = 'Seu nome de usuário ou senha')

    user_password = forms.CharField(required = True, max_length = 255, label = 'Sua senha')
        
class CommentForm(forms.Form):
    body = forms.CharField(max_length = 1000, required = True)
    
class PostForm(forms.Form):
    title = forms.CharField(max_length = 255, required = True)
    intro = forms.CharField(max_length = 511, required = True)
    body = forms.CharField(max_length = 1023, required = True)
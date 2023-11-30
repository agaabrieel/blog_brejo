from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from .forms import CreateAccountForm, LoginForm
from .models import BlogPost, BlogComment

# Create your views here.

def index(request):
    posts = BlogPost.objects.all()
    
    return render(request, 'blog/homepage.html', {'posts' : posts})

def login_user(request):
    
    if request.method == 'POST':
        
        form = LoginForm(request.POST)
        
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return render(request, 'blog/homepage.html')
            else:
                return render(request, 'blog/login_or_create_account.html')
            
    else:
        context = {'create_account' : False}
        return render(request, 'blog/login_or_create_account.html', context)

def create_user_account(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        user_password = request.POST['password']
        user_email = request.POST['email']
    
        form = CreateAccountForm(request.POST)
        
        if form.is_valid:
            try:
                user = User.objects.get(username = username, email = user_email)
                context = {'response' : 'Senha ou usuário incorretos.'}
                return render(request, 'blog/login_or_create_account.html', context)
            except User.DoesNotExist:
                user = User.objects.create_user(username = username, email = user_email, password = user_password)
                user.save()
                authenticated_user = authenticate(username = username, password = user_password)
                login(request, authenticated_user)
                return render(request, 'blog/homepage.html')
        else:
            return render(request, 'blog/login_or_create_account.html', context)
    else:
        context = {'create_account' : True}
        return render(request, 'blog/login_or_create_account.html', context)
    
def post_details(request, slug):
    
    if request.method == 'GET':
        post = get_object_or_404(BlogPost, slug = slug)
        return render(request, 'blog/post_details.html', {'post' : post})
    else:
        raise NotImplementedError
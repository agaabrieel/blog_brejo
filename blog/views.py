from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .forms import CreateAccountForm, LoginForm, CommentForm
from .models import BlogPost, BlogComment

# Create your views here.

def index(request):
    posts = BlogPost.objects.all()
    
    return render(request, 'blog/homepage.html', {'posts' : posts})

def login_user(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)    
        form = LoginForm(request.POST)
        
        if form.is_valid:
            if user is not None:
                login(request, user)
                return render(request, 'blog/homepage_template.html')
            else:
                context = {'response' : 'Senha ou nome de usuário incorreto.'}
                return render(request, 'blog/user_login_error_template.html')
        else:
            context = {'response' : form.errors}
            return render(request, 'blog/user_login_error_template.html')           
    else:
        form = LoginForm(request.GET)
        context = {'form' : form}
        return render(request, 'blog/user_login_template.html', context)

def create_user_account(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        user_password = request.POST['password']
        user_email = request.POST['email']
    
        form = CreateAccountForm(request.POST)
        
        if form.is_valid:
            try:
                user = User.objects.get(username = username, email = user_email)
                context = {'response' : 'Já existe um usuário cadastrado com este e-mail/username.'}
                return render(request, 'blog/create_account_error_template.html', context)
            except User.DoesNotExist:
                user = User.objects.create_user(username = username, email = user_email, password = user_password)
                user.save()
                authenticated_user = authenticate(username = username, password = user_password)
                login(request, authenticated_user)
                return render(request, 'blog/homepage_template.html')
        else:
            context = {'response' : form.errors}
            return render(request, 'blog/create_account_error_template.html', context)
    else:
        form = CreateAccountForm()
        context = {'form' : form}
        return render(request, 'blog/create_account_template.html', context)
    
def post_details(request, slug):
    
    form = CommentForm(request.POST)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid:
                post = BlogPost.objects.get(slug = slug)
                comment = BlogComment.objects.create(owner = request.POST['username'], body = form.body, post = post)
                comment.save()
        else:
            return render()

    form = CommentForm(request.POST)
    post = get_object_or_404(BlogPost, slug = slug)
    comments = get_list_or_404(BlogComment, post = post)
    return render(request, 'blog/post_details_template.html', {'post' : post, 'comments' : comments, 'form' : form})
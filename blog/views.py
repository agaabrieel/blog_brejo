from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .forms import CreateAccountForm, LoginForm, CommentForm
from .models import BlogPost, BlogComment

# Create your views here.

def index(request):
    posts = BlogPost.objects.all()
    
    return render(request, 'blog/homepage_template.html', {'posts' : posts})

def login_user(request):
    
    if request.method == 'POST':
        
        form = LoginForm(request.POST, user = request.user)
        
        if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username = username, password = password)    
                login(request, user)
                return render(request, 'blog/homepage_template.html')
        else:
            context = {'response' : form.errors}
            return render(request, 'blog/user_login_template.html')           
    else:
        form = LoginForm(user = request.user)
        context = {'form' : form}
        return render(request, 'blog/user_login_template.html', context)

def create_user_account(request):
    
    if request.method == 'POST':
        
        form = CreateAccountForm(request.POST, user = request.user)
        
        if form.is_valid():
            username = request.POST['username']
            user_password = request.POST['user_password']
            user_email = request.POST['user_email']
            user = User.objects.create_user(username = username, email = user_email, password = user_password)
            user.save()
            authenticated_user = authenticate(username = username, password = user_password)
            login(request, authenticated_user)
            return render(request, 'blog/homepage_template.html')
        else:
            context = {'response' : form.errors}
            return render(request, 'blog/create_account_template.html', context)
    else:
        form = CreateAccountForm(user = request.user)
        context = {'form' : form}
        return render(request, 'blog/create_account_template.html', context)
    
def post_details(request, slug):
    
    if request.method == 'POST':
        form = CommentForm(request.POST, user = request.user)
        if form.is_valid():
            form_body = form.cleaned_data['body']
            post = BlogPost.objects.get(slug = slug)
            comment = BlogComment.objects.create(owner = request.user, body = form_body, post = post)
            comment.save()
            
    form = CommentForm(user = request.user)
    post = get_object_or_404(BlogPost, slug = slug)
    comments = get_list_or_404(BlogComment, post = post)
    return render(request, 'blog/post_details_template.html', {'post' : post, 'comments' : comments, 'form' : form})
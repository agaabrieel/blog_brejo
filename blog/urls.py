from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create_account', views.create_user_account, name = 'create_account'),
    path('login', views.login_user, name = 'login'),
    path('<slug:slug>/', views.post_details, name = 'post_detail')
]
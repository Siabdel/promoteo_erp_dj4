"""
-- refact src compatibilite django4

"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as core_auth_views

name = "authorize"

urlpatterns = [
    path('users/', core_auth_views.user_list, name='user_list'),
    path('users/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='user_login'),
    path('users/logged/', core_auth_views.user_logged, name='user_logged'),
    path('users/logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    path('users/add/', core_auth_views.user_add, name='user_add'),
    path('users/<str:username>/', core_auth_views.user_detail, name='user_detail'),
    path('users/<str:username>/edit/', core_auth_views.user_edit, name='user_edit'),
    path('users/<str:username>/delete/', core_auth_views.user_delete, name='user_delete'),
    #path('comments/<int:id>/delete/', core_auth_views.comment_delete, name='comment_delete'),
]


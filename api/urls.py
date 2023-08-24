from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('users/', views.UserProfilesView.as_view(), name='users'),
    path('users/<str:pk>/', views.UserDetailApiView.as_view(), name='user-detail'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.allowed_urls, name='home')
]

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('current-user/', views.current_user, name='current-user'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check-permission/', views.check_permission, name='check-permission'),
]

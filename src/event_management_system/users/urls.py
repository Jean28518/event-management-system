from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('api/create/', views.api_create, name='api_create'),
    path('api/get/', views.api_get, name='api_get'),
    path('api/delete/', views.api_delete, name='api_delete'),
    path('api/update/', views.api_update, name='api_update'),
    path('api/reset-password/', views.api_reset_password, name='api_reset_password'),
    path('api/change-password/', views.api_change_password, name='api_change_password'),
    path('api/login/', views.login, name='api_login'),
    
    path('', views.user_overview, name='user_overview'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('create/', views.user_create, name='user_create'),
    path('edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('<int:user_id>/reset_password/', views.user_reset_password, name='user_reset_password'),

    
]
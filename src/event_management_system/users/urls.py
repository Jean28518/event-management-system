from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.user_overview, name='user_overview'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('create/', views.user_create, name='user_create'),
    path('edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('<int:user_id>/reset_password/', views.user_reset_password, name='user_reset_password'),

    
]
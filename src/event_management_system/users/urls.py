from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.user_overview, name='user_overview'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('create/', views.user_create, name='user_create'),
    path('register/', views.user_register, name='user_register'),
    path('edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('view/<int:user_id>/', views.user_view, name='user_view'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('reset_password/', views.user_reset_password, name='user_reset_password'),
    path('change_password/', views.user_change_password, name='user_change_password'),
    path('edit_profile/', views.user_edit_profile, name='user_edit_profile'),
    path('export_csv/', views.user_export_csv, name='user_export_csv'),

    
]
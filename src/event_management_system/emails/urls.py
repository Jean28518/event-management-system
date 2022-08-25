from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.email_overview, name='email_overview'),
    path('create/', views.email_create, name='email_create'),
    path('edit/<int:email_id>/', views.email_edit, name='email_edit'),
    path('delete/<int:email_id>/', views.email_delete, name='email_delete'),

    path('send_mail/<int:user_id>/<int:lecture_id>/', views.email_send, name='email_send'),

    path('send_mass_user/', views.email_send_mass_user, name='email_send_mass_user'),
    path('email_send_mass_user_select_all/', views.email_send_mass_user_select_all, name='email_send_mass_user_select_all'),
    path('email_send_mass_user_deselect_all/', views.email_send_mass_user_deselect_all, name='email_send_mass_user_deselect_all'),
    
    path('send_mass_lecture/<int:event_id>/', views.email_send_mass_lecture, name='email_send_mass_lecture'),
    path('email_send_mass_user_select_all/<int:event_id>/', views.email_send_mass_lecture_select_all, name='email_send_mass_lecture_select_all'),
    path('email_send_mass_user_deselect_all/<int:event_id>/', views.email_send_mass_lecture_deselect_all, name='email_send_mass_lecture_deselect_all'),
]
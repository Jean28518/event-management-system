from django.urls import path

from . import views

urlpatterns = [ 
    # Events
    path('', views.email_overview, name='email_overview'),
    path('create/', views.email_create, name='email_create'),
    path('edit/<int:email_id>/', views.email_edit, name='email_edit'),
    path('delete/<int:email_id>/', views.email_delete, name='email_delete'),
]
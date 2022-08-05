from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('get/', views.get, name='get'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
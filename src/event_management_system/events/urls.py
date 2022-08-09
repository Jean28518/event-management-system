from django.urls import path

from . import views

urlpatterns = [ 
    path('event/', views.event_overview, name='event_overview'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/edit/<int:event_id>', views.event_edit, name='event_edit'),
    path('event/delete/<int:event_id>', views.event_delete, name='event_delete'),
]
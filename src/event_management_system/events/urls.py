from django.urls import path

from . import views

urlpatterns = [ 
    # Events
    path('event/', views.event_overview, name='event_overview'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/edit/<int:event_id>/', views.event_edit, name='event_edit'),
    path('event/delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('event/archive/<int:event_id>/', views.event_archive, name='event_archive'),
    path('event/enable_call_for_papers/<int:event_id>/', views.enable_call_for_papers, name='enable_call_for_papers'),
    path('event/disable_call_for_papers/<int:event_id>/', views.disable_call_for_papers, name='disable_call_for_papers'),
    path('event/<int:event_id>/scheduler/', views.event_scheduler, name='event_scheduler'),

    # Timeslots
    path('event/<int:event_id>/timeslot/', views.event_timeslot, name='event_timeslot'),
    path('event/<int:event_id>/timeslot/add/', views.event_timeslot_add, name='event_timeslot_add'),
    path('event/<int:event_id>/timeslot/remove/<int:index>/', views.event_timeslot_remove, name='event_timeslot_remove'),

    # Custom Questions
    path('event/<int:event_id>/custom_questions/', views.event_custom_questions, name='event_custom_questions'),
    path('event/<int:event_id>/custom_questions/add/', views.event_custom_questions_add, name='event_custom_questions_add'),
    path('event/<int:event_id>/custom_questions/remove/<int:id>', views.event_custom_questions_remove, name='event_custom_questions_remove'),

    # Field Activation
    path('event/<int:event_id>/field_activation/', views.event_field_activation, name='event_field_activation'),

    # Rooms
    path('room/', views.room_overview, name='room_overview'),
    path('room/create/', views.room_create, name='room_create'),
    path('room/edit/<int:room_id>/', views.room_edit, name='room_edit'),
    path('room/delete/<int:room_id>/', views.room_delete, name='room_delete'),

    # Lectures
    path('<int:event_id>/lecture/public/create/entry/', views.lecture_public_create_entry, name = 'lecture_public_create_entry'),
    path('<int:event_id>/lecture/public/create/', views.lecture_public_create, name = 'lecture_public_create'),
    path('<int:event_id>/lecture/public/created_success', views.lecture_public_created_successfully, name = 'lecture_public_created_successfully'),
    path('<int:event_id>/lecture/overview/', views.lecture_overview, name = 'lecture_overview'),
    path('<int:event_id>/lecture/create/', views.lecture_create, name = 'lecture_create'),
    path('lecture/edit/<int:lecture_id>/', views.lecture_edit, name = 'lecture_edit'),
    path('lecture/view/<int:lecture_id>/', views.lecture_view, name = 'lecture_view'),
    path('lecture/delete/<int:lecture_id>/', views.lecture_delete, name = 'lecture_delete'),
    path('lecture/export_csv/', views.lecture_export_csv, name = 'lecture_export_csv'),
    path('<int:event_id>/timetable/', views.timetable, name = 'timetable'),
    path('<int:event_id>/current_running/<int:room_id>/', views.lecture_current_running, name = 'lecture_current_running'),

    # Lectures (contact specific)
    path('lecture/contact/overview', views.lecture_contact_overview, name = 'lecture_contact_overview'),
    path('lecture/contact/create_entry', views.lecture_contact_create_entry, name = 'lecture_contact_create_entry'),
    path('lecture/contact/edit/<int:lecture_id>', views.lecture_contact_edit, name = 'lecture_contact_edit'),
    path('lecture/contact/view/<int:lecture_id>', views.lecture_contact_view, name = 'lecture_contact_view'),

    # Get all Lectures of an event over api:
    path('api/<int:event_id>/', views.api_event_data, name = "api_event_data"),


]
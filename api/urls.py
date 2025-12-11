from django.urls import path
from . import views

urlpatterns = [
    # Page Views
    path('', views.home, name='home'),
    
    # Authentication Views (These match the 'action' in your HTML forms)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('guidelines/', views.guidelines_view, name='guidelines'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),

    path('events/', views.event_list, name='events'),
    path('events/<int:event_id>/rsvp/', views.toggle_rsvp, name='toggle_rsvp'),

    path('tutors/', views.tutor_list, name='tutors'),
    path('tutors/<int:tutor_id>/request/', views.request_session, name='request_session'),

    path('network/', views.network, name='network'),

    # Groups List Page
    path('groups/', views.groups, name='groups'),

    # Single Group Detail Page (MISSING in your snippet)
    # This allows links like /groups/1/ to work
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),

]
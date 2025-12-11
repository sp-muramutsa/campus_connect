from django.urls import path
from . import views

urlpatterns = [
    # Core & Static Pages
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('guidelines/', views.guidelines_view, name='guidelines'),
    path('contact/', views.contact_view, name='contact'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User Profile
    path('profile/', views.profile_view, name='profile'), 
    path('profile/<str:username>/', views.profile_view, name='profile_view'),

    # Tutors
    path('tutors/', views.tutor_list, name='tutors'),
    path('tutors/<int:tutor_id>/request/', views.request_session, name='request_session'),

    # Network 
    path('network/', views.network, name='network'),
    path('connect/<int:target_user_id>/', views.connect_student, name='connect_student'),
    
    # Groups
    path('groups/', views.groups, name='groups'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),

    # Events 
    path('events/', views.event_list, name='events'),
    path('events/<int:event_id>/rsvp/', views.toggle_rsvp, name='toggle_rsvp'),
]
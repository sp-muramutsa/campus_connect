from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q
from .models import Profile, Event, RSVP, SessionRequest, Group


def home(request):
    now = timezone.now()
    # Fetch 3 Upcoming Events
    recent_events = Event.objects.filter(date__gte=now).order_by('date')[:3]
    # Fetch 3 Tutors
    featured_tutors = Profile.objects.filter(is_tutor=True)[:3]

    context = {
        'events': recent_events,
        'tutors': featured_tutors,
    }
    return render(request, 'index.html', context)

def about_view(request):
    return render(request, 'about.html')

def guidelines_view(request):
    return render(request, 'guidelines.html')

def contact_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        sender = request.user.email if request.user.is_authenticated else 'Anonymous Guest'
        full_body = f"Message from: {sender}\n\n{message}"

        try:
            send_mail(
                subject=f"Contact Form: {subject}",
                message=full_body,
                from_email='noreply@campusconnect.com',
                recipient_list=['paccysan@gmail.com'], 
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            print(e)
            return redirect('contact')

    return render(request, 'contact.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Account with this email already exists.')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name 
            user.save()
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'register.html')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_view(request, username=None):
    # If a username is provided, view that user's profile.
    # Otherwise, view the current logged-in user's profile.
    if username:
        target_user = get_object_or_404(User, username=username)
    else:
        target_user = request.user

    profile, created = Profile.objects.get_or_create(user=target_user)

    # Only allow editing if it is YOUR profile
    if request.method == 'POST' and target_user == request.user:
        request.user.first_name = request.POST.get('name')
        request.user.save()

        profile.phone = request.POST.get('phone')
        profile.bio = request.POST.get('bio')
        profile.skills = request.POST.get('skills')
        profile.is_tutor = request.POST.get('is_tutor') == 'on'
        profile.hourly_rate = request.POST.get('hourly_rate')
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile, 'is_own_profile': (target_user == request.user)})

def tutor_list(request):
    tutors = Profile.objects.filter(is_tutor=True)
    return render(request, 'tutors.html', {'tutors': tutors})

@login_required(login_url='login')
def request_session(request, tutor_id):
    tutor = get_object_or_404(User, id=tutor_id)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        SessionRequest.objects.create(
            student=request.user,
            tutor=tutor,
            subject=subject,
            message=message
        )
        messages.success(request, f"Request sent to {tutor.first_name}!")
        return redirect('tutors')

    return render(request, 'requests.html', {'tutor': tutor})

def network(request):
    suggested_tutors = Profile.objects.filter(is_tutor=True).select_related('user')[:3]
    suggested_groups = Group.objects.all()[:3]
    
    context = {
        'tutors': suggested_tutors,
        'groups': suggested_groups,
    }
    return render(request, 'network.html', context)

@login_required(login_url='login')
def connect_student(request, target_user_id):
    target_user = get_object_or_404(User, id=target_user_id)
    
    # Create a new private study group
    new_group = Group.objects.create(
        name=f"Study Session: {request.user.first_name} & {target_user.first_name}",
        description="A private study group created via Network."
    )
    
    # Add both users
    new_group.members.add(request.user, target_user)
    
    messages.success(request, f"You are now connected with {target_user.first_name}!")
    return redirect('groups')

def groups(request):
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'groups.html', context)

def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    context = {'group': group}
    return render(request, 'group.html', context)

def event_list(request):
    now = timezone.now()
    query = request.GET.get('q')
    
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')
    past_events = Event.objects.filter(date__lt=now).order_by('-date')
    
    if query:
        search_filter = Q(title__icontains=query) | \
                        Q(description__icontains=query) | \
                        Q(location__icontains=query)       
        upcoming_events = upcoming_events.filter(search_filter)
        past_events = past_events.filter(search_filter)

    attending_ids = []
    if request.user.is_authenticated:
        attending_ids = RSVP.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'attending_ids': attending_ids,
        'query': query,
    })

@login_required(login_url='login')
def toggle_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp = RSVP.objects.filter(user=request.user, event=event)
    
    if rsvp.exists():
        rsvp.delete()
    else:
        RSVP.objects.create(user=request.user, event=event)
        
    return redirect('events')
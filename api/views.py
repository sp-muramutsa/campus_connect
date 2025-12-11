from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.mail import send_mail
from .models import Profile

# 1. HOME PAGE
def home(request):
    # 1. Fetch 3 Upcoming Events
    now = timezone.now()
    recent_events = Event.objects.filter(date__gte=now).order_by('date')[:3]
    
    # 2. Fetch 3 Tutors
    featured_tutors = Profile.objects.filter(is_tutor=True)[:3]

    context = {
        'events': recent_events,
        'tutors': featured_tutors,
    }
    return render(request, 'index.html', context)

# 2. REGISTER
def register_view(request):
    if request.method == 'POST':
        # Get data from the HTML form inputs
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validation: Check if email/username already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Account with this email already exists.')
            return render(request, 'register.html')

        try:
            # SERVER-SIDE SECURITY: create_user hashes the password automatically
            # We use email as the username to keep it simple
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name 
            user.save()
            
            # Auto-login after registration (User convenience)
            login(request, user)
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return render(request, 'register.html')

    # If GET request, just show the page
    return render(request, 'register.html')

# 3. LOGIN
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # SECURITY: Authenticate checks the hashed password securely
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user) # Creates the session cookie
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

# 4. LOGOUT
def logout_view(request):
    logout(request) # Destroys the session
    return redirect('login')

def contact_view(request):
    if request.method == 'POST':
        # 1. Get the data from the form
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # 2. Construct the email content
        # We assume "Anonymous" if they aren't logged in
        sender = request.user.email if request.user.is_authenticated else 'Anonymous Guest'
        full_body = f"Message from: {sender}\n\n{message}"

        # 3. Send it (prints to terminal because of settings.py)
        try:
            send_mail(
                subject=f"Contact Form: {subject}",
                message=full_body,
                from_email='noreply@campusconnect.com',
                recipient_list=['paccysan@gmail.com'], 
                fail_silently=False,
            )
            # 4. Success! Show a green message
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            print(e) # Print exact error to terminal for debugging
            return redirect('contact')

    # If GET request, just show the form
    return render(request, 'contact.html')

def guidelines_view(request):
    return render(request, 'guidelines.html')

def about_view(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('name')
        request.user.save()

        profile.phone = request.POST.get('phone')
        profile.bio = request.POST.get('bio')
        profile.skills = request.POST.get('skills')
        
        # NEW: Handle the Checkbox
        # Checkboxes don't send "False", they send nothing if unchecked.
        profile.is_tutor = request.POST.get('is_tutor') == 'on'
        profile.hourly_rate = request.POST.get('hourly_rate')
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile})

# 2. NEW: TUTOR LIST VIEW
def tutor_list(request):
    # Filter: Get profiles where is_tutor is True
    tutors = Profile.objects.filter(is_tutor=True)
    return render(request, 'tutors.html', {'tutors': tutors})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event, RSVP

# views.py
from django.db.models import Q  # Import this at the top!
from django.shortcuts import render, redirect, get_object_or_404

def event_list(request):
    now = timezone.now()
    query = request.GET.get('q') # Get the text from the search box
    
    # 1. Start with ALL events sorted correctly
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')
    past_events = Event.objects.filter(date__lt=now).order_by('-date')
    
    # 2. If user searched for something, filter the results
    if query:
        # Search Title OR Description OR Location
        search_filter = Q(title__icontains=query) | \
                        Q(description__icontains=query) | \
                        Q(location__icontains=query)
                        
        upcoming_events = upcoming_events.filter(search_filter)
        past_events = past_events.filter(search_filter)

    # 3. Get RSVP status (Same as before)
    attending_ids = []
    if request.user.is_authenticated:
        attending_ids = RSVP.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'attending_ids': attending_ids,
        'query': query, # Pass the query back so we can keep it in the input box
    })

# 2. THE INVISIBLE ACTION (Toggle RSVP)
@login_required(login_url='login')
def toggle_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if RSVP exists
    rsvp = RSVP.objects.filter(user=request.user, event=event)
    
    if rsvp.exists():
        rsvp.delete() # Leave
    else:
        RSVP.objects.create(user=request.user, event=event) # Join
        
    return redirect('events') # Stay on the list page

from .models import SessionRequest, Profile # Ensure SessionRequest is imported

# ... existing views ...

@login_required(login_url='login')
def request_session(request, tutor_id):
    # 1. Get the tutor's User object (not Profile)
    tutor = get_object_or_404(User, id=tutor_id)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # 2. Save the request
        SessionRequest.objects.create(
            student=request.user,
            tutor=tutor,
            subject=subject,
            message=message
        )
        
        # 3. Success! Redirect to Tutors list or Home
        messages.success(request, f"Request sent to {tutor.first_name}!")
        return redirect('tutors')

    return render(request, 'requests.html', {'tutor': tutor})

from .models import Event, Group # Assuming you have these models
from django.contrib.auth import get_user_model

from .models import Group, Event, Profile # Import Profile here
def network(request):
    # Fetch Tutors (Profiles with is_tutor=True)
    suggested_tutors = Profile.objects.filter(is_tutor=True).select_related('user')[:3]
    
    # Fetch Events & Groups
    suggested_events = Event.objects.all()[:3]
    suggested_groups = Group.objects.all()[:3]

    context = {
        'tutors': suggested_tutors,
        'events': suggested_events,
        'groups': suggested_groups,
    }
    return render(request, 'network.html', context)

# 2. Groups List View
def groups(request):
    # Fetch all groups from the DB
    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'groups.html', context)

# 3. Single Group Detail View
def group_detail(request, pk):
    # Fetch specific group by ID (pk) or show 404 error
    group = get_object_or_404(Group, pk=pk)
    context = {'group': group}
    return render(request, 'group.html', context)
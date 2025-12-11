from django.db import models
from django.contrib.auth.models import User

# TABLE 1: Built-in

# TABLE 2: Event (One-to-Many with User who created it)
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    
    def __str__(self):
        return self.title

# TABLE 3: RSVP (Many-to-Many)
class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event') # Prevents double RSVPing

# models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    is_tutor = models.BooleanField(default=False) # Checkbox: "I want to be a tutor"

    def __str__(self):
        return f"{self.user.username}'s Profile"

class SessionRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.student} to {self.tutor}"


class Group(models.Model):
    name = models.CharField(max_length=200)
    focus = models.CharField(max_length=100, help_text="e.g. Computer Science, Math, Design")
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='joined_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # Helper method to get count in template easily
    def members_count(self):
        return self.members.count()

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"Post by {self.author} in {self.group}"
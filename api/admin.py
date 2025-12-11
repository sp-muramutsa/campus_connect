from django.contrib import admin
from .models import Event, RSVP, Group, GroupPost  # Import your models

# This line makes them show up in the Admin Dashboard
admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(Group)
admin.site.register(GroupPost)
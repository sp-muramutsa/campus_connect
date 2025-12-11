from django.contrib import admin
from .models import Event, RSVP, Group, GroupPost  

admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(Group)
admin.site.register(GroupPost)
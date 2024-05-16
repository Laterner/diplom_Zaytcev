from django.contrib import admin
from .models import *


admin.site.register(Post)
admin.site.register(Event)
admin.site.register(EventMembers)
admin.site.register(UserSubscribe)

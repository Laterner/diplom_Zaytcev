from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Event (models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    event_date = models.DateTimeField(default=timezone.now)
    event_price = models.IntegerField(default=1000)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})
    

class EventMembers(models.Model):
    event_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    enjoy_date = models.DateTimeField(default=timezone.now)
    
    user_prof = models.ForeignKey(
        User, 
        blank=True,
        null=True, 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.event_id.__str__()
    
class UserSubscribe (models.Model):
    user_id = models.IntegerField(primary_key=True)
    # username = models.CharField(default='', max_length=150)
    purchase_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=None)
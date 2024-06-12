from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(default='event_default.png', upload_to='post_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        img = Image.open(self.image.path)
        img.save(self.image.path)
    
class Event (models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    event_date = models.DateTimeField(default=timezone.now)
    event_price = models.IntegerField(default=1000)
    
    image = models.ImageField(default='event_default.png', upload_to='event_pics')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        
        img = Image.open(self.image.path)
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)

class EventMembers(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.IntegerField(default=1, blank=True, null=True)
    enjoy_date = models.DateTimeField(default=timezone.now)
    
    user_prof = models.ForeignKey(
        User, 
        blank=True,
        null=True, 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.event.__str__()
    
class UserSubscribe (models.Model):
    user_id = models.ForeignKey(
        User, 
        blank=True,
        null=True, 
        on_delete=models.CASCADE
    )
    
    purchase_date = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=None)
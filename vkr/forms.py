from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Event

# class EventForm(forms.ModelForm):
#    class Meta:
#         model = Event
#         fields = ['title', 'content', 'date_posted', 'event_date', 'event_price']
#         widgets = {'blog_post': SummernoteWidget()}

class PostUpdateForm(forms.ModelForm):
    title = forms.CharField(label="Название")
    content = forms.CharField(label="Содержание")
    image = forms.ImageField(label="Изображение", required=False)

    class Meta:
        model = Event
        fields = ['title', 'content']

class EventUpdateForm(forms.ModelForm):
    title = forms.CharField(label="Название", required=False)
    content = forms.CharField(label="Содержание", required=False)
    event_date = forms.DateTimeField(label="Дата проведения")
    event_price = forms.CharField(label="Цена", required=False)
    image = forms.ImageField(label="Изображение", required=False)

    class Meta:
        model = Event
        fields = ['title', 'content', 'event_date', 'event_price', 'image'] # 
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Event

# class EventForm(forms.ModelForm):
#    class Meta:
#         model = Event
#         fields = ['title', 'content', 'date_posted', 'event_date', 'event_price']
#         widgets = {'blog_post': SummernoteWidget()}


class EventUpdateForm(forms.ModelForm):
    image = forms.ImageField(label="Изображение", required=False)
    title = forms.CharField(label="Название")
    content = forms.CharField(label="Содержание")
    event_date = forms.CharField(label="Дата проведения")
    event_price = forms.CharField(label="Цена")

    class Meta:
        model = Event
        fields = ['title', 'content', 'event_date', 'event_price']
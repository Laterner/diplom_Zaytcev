from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Event, UserSubscribe, EventMembers
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta

from django.http import Http404

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'vkr/home.html', context)


class EventListView(ListView):
    model = Event
    template_name = 'vkr/events.html'  
    context_object_name = 'events'
    ordering = ['-date_posted']
    # paginate_by = 5

class EventDetailView(DetailView):
    model = Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = [
        'title', 
        'content', 
        'event_date', 
        'event_price'
        ]

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostListView(ListView):
    model = Post
    template_name = 'vkr/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'vkr/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')    


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        post = self.get_object()
        form.instance.author = post.author # self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False


def about(request):
    return render(request, 'vkr/about.html', {'title': 'О нашей организации'})

def subs(request):
    return render(request, 'vkr/subscription-sale.html')


@login_required
def admin_control(request):
    if request.user.is_superuser:
        return render(request, 'vkr/admin_urls.html')
    else: redirect('/')


def view_all_subs(request):
    subbers = UserSubscribe.objects.all().order_by('purchase_date')
    event_pack = []
    
    for el in subbers:
        event_pack.append({
            'purchase_date': el.purchase_date,
            'username': User.objects.get(id=el.user_id).username,
            'valid_until': el.valid_until, 
            })
        
    return render(request, 'vkr/subbers.html', {'event_pack': event_pack})

def view_event_members(request):
    members = EventMembers.objects.all().order_by('enjoy_date')
    event_pack = []
    
    for el in members:
        try:
            event_pack.append({
                'event_id': el.event,
                'enjoy_date': el.enjoy_date,
                'event_name': Event.objects.get(id=el.event).title, 
                'event_member': User.objects.get(id=el.user).username,
                'user_prof': el.user_prof,
            })
        except:
            print(el.event, el.enjoy_date)
        
    return render(request, 'vkr/event_members.html', {'event_pack': event_pack})


""" API links """
def active_sub(request, sub_type):
    sub_types = {
        'start':91,
        'middle':182,
        'pro':365,
    }

    if sub_type == None:
        return HttpResponse('incorrect request')
    
    days = sub_types.get(sub_type)
    if days == None:
        return HttpResponse('incorrect type')
    
    user_id = request.user.id
    username = request.user.username
    
    if user_id == None or username == None:
        return HttpResponse('incorrect user')
    
    try:
        if current_sub := UserSubscribe.objects.get(user_id=user_id):
            return HttpResponse(f'Уже куплен. Действует до ({current_sub.valid_until})')
    except:
        pass
    
    purchase_date = datetime.today()
    valid_until = datetime.today() + timedelta(days=days)
    UserSubscribe.objects.create(user_id=user_id, purchase_date=purchase_date, valid_until=valid_until)
    return HttpResponse(f'Оплата прошла успешно!') # TODO Добавить страницу оплаты

def enjoy_event(request, event_id):
    user_id = request.user.id
    
    if not request.user.is_authenticated:
        return HttpResponse('Для записи необходимо авторизоваться')

    
       
    if Event.objects.filter(id=event_id).exists():
        if EventMembers.objects.filter(event=event_id, user=user_id).exists():
                return HttpResponse('Вы уже записаны на данное мероприятие')
        
        em = EventMembers(event=event_id, user=user_id)
        em.save()
    else:
        return HttpResponse('Такого мероприятия нет')
    
    if not UserSubscribe.objects.filter(user_id=user_id).exists():
        return HttpResponse('Вы успешно записались, необходимо оплатить вход')
    
    return HttpResponse('Вы успешно записались')

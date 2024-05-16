from django.shortcuts import render, get_object_or_404, HttpResponse
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
    paginate_by = 5

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
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'vkr/about.html', {'title': 'О клубе Python Bites'})

def subs(request):
    return render(request, 'vkr/subscription-sale.html')

@login_required
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

def view_all_subs(request):
    subbers = UserSubscribe.objects.all().order_by('purchase_date')
    return render(request, 'vkr/subbers.html', {'subbers': subbers})

def view_event_members(request):
    members = EventMembers.objects.all().order_by('enjoy_date')
    return render(request, 'vkr/subbers.html', {'members': members})

@login_required
def enjoy_event(request, event_id):
    user_id = request.user.id

    try:
      if current_event := Event.objects.get(id=event_id):
            try:
                if user := EventMembers.objects.get(user_id=user_id):
                    return HttpResponse('Вы уже записаны на данное мероприятие')
            except:
                pass
            
            em = EventMembers(event_id=event_id, user_id=user_id)
            em.save()
    except:
      return HttpResponse('Такого мероприятия нет')

    return HttpResponse('Вы успешно записались')
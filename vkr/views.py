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

from django.core.mail import send_mail
from django.conf import settings

from datetime import datetime, timedelta

from django.http import Http404

import json


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'vkr/home.html', context)


class EventListView(ListView):
    queryset = Event.objects.filter(is_active=True)
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
        form.instance.author = post.author
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


def send_mail_form(subject, message, recipients):
	send_mail(
    		subject=subject,
    		message=message,
    		from_email=settings.EMAIL_HOST_USER,
    		recipient_list=recipients)

def get_date_postfix(days_remind: int) -> str:    
    if days_remind % 10 == 0:
        return ' дней'
    elif days_remind % 10 == 1:
        return ' день'
    elif 2 >= days_remind % 10 >= 4:
        return ' дня'
    elif 5 >= days_remind % 10 >= 9:
        return ' дней'
    else:
        return ' дней'

def notify_users_subs():
    users = UserSubscribe.objects.all()

    d1 = datetime.today().date()

    email_list = []

    for user in users:
        d2 = user.purchase_date.date()
        days: int = (d1 - d2).days

        if days < 4:
            print('days remind:', days)
            email_list.append(user.user_id.email)

    print('email_list:', email_list)

    print(len(email_list))

    if len(email_list) > 0:
        try:
            send_mail_form(
                'Напоминание о подписке', 
                f'Уважаемый подписчик, напоминаетм Вам, что завтра \
                    Ваша подписка закончится, не забудьте продлить её', 
                [email_list]
            )
        except:
            print('Invalid address', email_list)
            return {'email_list:': 'Invalid address'}

    if email_list.__len__() < 1:
        return {'email_list:': 'Некого оповещать'}
    else:
        return {'email_list:': email_list}
    
def get_active_events():    
    evs = Event.objects.filter(is_active=True)
    
    response_data = {}
    
    d1 = datetime.today().date()

    for i, ev in enumerate(evs):
        # print(i, ev)

        d2 = ev.event_date.date()
        
        i = str(i)
        response_data[i] = {}
        response_data[i]['title'] = ev.title
        response_data[i]['event_date'] = d2.__str__()
        response_data[i]['today'] = d1.__str__()    

        days = d1 - d2

        if d1 <= d2:
            email_list = []
            # response_data[i]['is_not_today'] = 'yes'
            event_members = EventMembers.objects.filter(event=ev.pk)

            for key, member in enumerate(event_members):
                print(member.user_prof.email)
                email_list.append(member.user_prof.email)

            days_remind = days.days * -1
            days_remind_s = str(days_remind) + get_date_postfix(days_remind)

            send_mail_form(
                'Напоминание об эвенте', 
                f'Уважаемый подписчик, напоминаетм Вам, что через {days_remind_s} \
                    дней пройдёт мероприятие[{ev.title}] на которое Вы зависались', 
                email_list
            )

        else:
            # response_data[i]['is_not_today'] = 'no'
            Event.objects.filter(pk=ev.pk).update(is_active=False)

        response_data[i]['days'] = days.days
        
    # print('finish:', response_data)

    return json.dumps(response_data)

def send_notification_sub(request):
    response_data = notify_users_subs()
    return HttpResponse(response_data, content_type="application/json")

def send_notification_event(request):
    response_data = get_active_events()
    return HttpResponse(response_data, content_type="application/json")

def get_url_response(request):
    # response_data = get_active_events()
    # response_data = 'get_active_events()'
    # send_mail_form('subject', 'message',[settings.EMAIL_HOST_USER])
    response_data = notify_users_subs()
    return HttpResponse(response_data, content_type="application/json")

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
            'username': el.user_id.username,
            'valid_until': el.valid_until, 
            'profile': el.user_id
            })
        
    return render(request, 'vkr/subbers.html', {'event_pack': event_pack})

def view_event_members(request):
    members = EventMembers.objects.all().order_by('enjoy_date')
    event_pack = {}

    for el in members:
        event_pack[el.event] = {
            'title': Event.objects.get(id=el.event).title, 
            'data': []
            }
    
    for el in members:
        try:
            event_pack[el.event]['data'].append({
                'event_id': el.event,
                'enjoy_date': el.enjoy_date,
                'event_name': Event.objects.get(id=el.event).title, 
                'event_member': el.user_prof.username,
                'user_prof': el.user_prof,
            })
        except:
            print("error ------------------ error")
    # print(evesnt_pack)
    return render(request, 'vkr/event_members.html', {'event_pack': event_pack})


""" API links """
def active_sub(request, sub_type):
    user_id = request.user.id
    username = request.user.username
    
    if user_id == None or username == None:
        return HttpResponse('incorrect user')
    
    try:
        if current_sub := UserSubscribe.objects.get(user_id=user_id):
            return HttpResponse(f'Уже куплен. Действует до ({current_sub.valid_until})')
    except:
        pass
    
    return HttpResponse('pay_page')

def enjoy_event(request, event_id):
    user_id = request.user.id
    
    if not request.user.is_authenticated:
        return HttpResponse('Для записи необходимо авторизоваться')

       
    if Event.objects.filter(id=event_id).exists():
        if EventMembers.objects.filter(event=event_id, user_prof_id=user_id).exists():
                return HttpResponse('Вы уже записаны на данное мероприятие')
        
        em = EventMembers(event=event_id, user_prof_id=user_id)
        em.save()
    else:
        return HttpResponse('Такого мероприятия нет')

    if not UserSubscribe.objects.filter(user_id=user_id).exists():
        return HttpResponse('Вы успешно записались, необходимо оплатить вход')
    
    return HttpResponse('Вы успешно записались')

def get_pay(request):
    pass

def fake_pay(request, sub_type='middle'):
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

    purchase_date = datetime.today()
    valid_until = datetime.today() + timedelta(days=days)

    user_sub = UserSubscribe(user_id=request.user, purchase_date=purchase_date, valid_until=valid_until)
    user_sub.save()
    # return HttpResponse(f'Оплата прошла успешно!')
    return render(request, 'vkr/fake_pay.html') 

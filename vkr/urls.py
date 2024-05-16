from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    EventCreateView,
    EventListView,
    EventDetailView,
)
from . import views

urlpatterns = [
    path('', views.about, name='vkr-about'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),   
    path('news/', PostListView.as_view(), name='vkr-home'),
    path('news/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('news/new/', PostCreateView.as_view(), name='post-create'),
    path('news/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('subs/', views.subs, name='vkr-subs'),
    path('active_sub/<str:sub_type>/', views.active_sub, name='vkr-active_sub'),

    path('events/', EventListView.as_view(), name='vkr-events'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/new/', EventCreateView.as_view(), name='events-create'),
    path('view_all_subs/', views.view_all_subs, name='vkr-view_all_subs'),
    path('enjoy_event/<int:event_id>/', views.enjoy_event, name='vkr-enjoy_event'),
    path('view_event_members/', views.view_event_members, name='vkr-view_event_members'),
    
    path('admin_control/', views.admin_control, name='vkr-admin_control'),
]
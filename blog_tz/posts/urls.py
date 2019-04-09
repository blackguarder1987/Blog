from django.urls import path
from .views import *

from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', MainTestView.as_view(), name = 'base-view'),
    path('post/<str:slug>', PostDetailView.as_view(), name='detail-post'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/update/<str:slug>', PostUpdateView.as_view(), name = 'post-update'),
    path('post/delete/<int:pk>', BookDeleteView.as_view(), name = 'post-delete'),

    path('search', SearchView.as_view(), name = 'search-view'),
    path('user_reaction/', UserReactionView.as_view(), name = 'user_reaction'),
]
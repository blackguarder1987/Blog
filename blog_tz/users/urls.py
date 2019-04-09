from django.urls import path
from .views import *

from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView


app_name = 'users'
urlpatterns = [

    # users
    path('login/', LoginView.as_view(), name ='login-view'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('posts:base-view')), name ='logout-view'),

    # registration
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # profile and actions
    path('profile/<pk>', Profile.as_view(), name = 'profile'),
    path('delete-profile/<pk>', ProfileDeleteView.as_view(), name = 'delete-profile'),

    path('update-prof/<pk>', GeneralUpdateView.as_view(), name = 'update-prof'),
    path('update-prof-personal/<pk>', PersonalUpdateView.as_view(), name = 'update-prof-pers'),
]




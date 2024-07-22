from django.urls import path
from . views import *
app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
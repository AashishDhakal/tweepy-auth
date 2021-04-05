from django.urls import path
from .views import login, home, call_back, user_profile, logout_user


urlpatterns = [
    path('', home, name="home-view"),
    path('login/', login, name="login-view"),
    path('callback/', call_back, name="call-back"),
    path('profile/', user_profile, name="profile"),
    path('logout/', logout_user, name="logout"),
]

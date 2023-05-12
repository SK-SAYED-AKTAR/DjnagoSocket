from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('complete_profile/', views.complete_profile, name="complete_profile"),
    path('change_online_status/', views.change_online_status, name="change_online_status"),
    path('chat_window/', views.chat_window, name="chat_window"),
]
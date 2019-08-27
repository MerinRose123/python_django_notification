from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="base.html"), name='base'),
    path('register/', views.register, name='home'),
    path('login/', views.loginview, name='loginview'),
    path('logout/', views.logoutview, name='logoutview'),
    path('home/', views.homeview),
    path('edit/', views.edit),
    path('delete/', views.delete),
    path('passwordchange/', views.passwordchange),
    path('like', views.like),
    path('lobby/', views.room, name='room'),
    path('serializer/', views.UserCreate.as_view(), name='user-create'),
]

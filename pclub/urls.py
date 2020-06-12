from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_homepage, name='get_homepage'),
    path('get_events/', views.get_events, name='get_events'),

]

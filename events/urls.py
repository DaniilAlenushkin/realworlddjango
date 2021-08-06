from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('list/', views.event_list),
    path('detail/<int:pk>/', views.event_detail, name='event_detail'),
]

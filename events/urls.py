from django.urls import path
from django.views.decorators.http import require_POST
from . import views

app_name = 'events'

urlpatterns = [
    path('event_list/', views.EventListView.as_view(), name='event_list'),
    path('event_detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event_update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('event_delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
    path('event_create/', views.EventCreateView.as_view(), name='event_create'),
    path('event_enroll/',  require_POST(views.EnrollCreateView.as_view()), name='enroll_create'),
    path('event_add_to_favorite/', require_POST(views.EventAddToFavoriteView.as_view()), name='event_add_to_favorite'),
]

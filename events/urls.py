from django.urls import path
from django.views.decorators.http import require_POST

from . import views

app_name = 'events'

urlpatterns = [
    path('list/', views.EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event_update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('event_delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
    path('enroll_delete/<int:pk>/', views.EnrollDeleteView.as_view(), name='enroll_delete'),
    path('review_delete/<int:pk>/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('favorite_delete/<int:pk>/', views.FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('event_create/', views.EventCreateView.as_view(), name='event_create'),
    path('event_enroll/',  require_POST(views.EnrollCreateView.as_view()), name='enroll_create'),
    path('event_add_to_favorite/', require_POST(views.EventAddToFavoriteView.as_view()), name='event_add_to_favorite'),
]

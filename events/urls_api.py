from django.urls import path

from . import views, views_api

app_name = 'api_events'

urlpatterns = [
    path('reviews/create/', views.create_review, name='create_review'),
    path('list/', views_api.EventViewSet.as_view({'get': 'list'}), name='events_list_api'),
    path('detail/<int:pk>/', views_api.EventViewSet.as_view({'get': 'retrieve'}), name='event_detail_api'),
    path('event_delete/<int:pk>/', views_api.EventViewSet.as_view({'delete': 'destroy'}), name='event_delete_api'),
    path('event_update/<int:pk>/', views_api.EventViewSet.as_view({'patch': 'partial_update'}),
         name='event_update_api'),
    path('event_create/', views_api.EventViewSet.as_view({'post': 'create'}), name='event_create_api'),
]

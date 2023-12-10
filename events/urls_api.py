from django.urls import path

from . import views, views_api

app_name = 'api_events'

urlpatterns = [
    path('reviews/create/', views.create_review, name='create_review'),
    path('', views_api.EventViewSet.as_view({'get': 'list', 'post': 'create'}), name='events_list_api'),
    path('<int:pk>/', views_api.EventViewSet.as_view({'get': 'retrieve',
                                                      'delete': 'destroy',
                                                      'patch': 'partial_update'}), name='event_detail_api'),
]

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Category, Feature, Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        GET

        Example:
            http://127.0.0.1:8000/api/events/list/?title=Субб&category=3
        """
        queryset = Event.objects_event_qs.event_qs()
        filter_category = request.query_params.get('category')
        filter_features = request.GET.getlist('features')
        filter_start = request.query_params.get('date_start')
        filter_end = request.query_params.get('date_end')
        filter_private = request.query_params.get('is_private')
        filter_available = request.query_params.get('is_available')
        filter_title = request.query_params.get('title')

        if filter_title:
            queryset = queryset.filter(title__icontains=filter_title)
        if filter_category:
            queryset = queryset.filter(category=filter_category)
        if filter_features:
            for feature in filter_features:
                queryset = queryset.filter(features__in=[feature])
        if filter_start:
            queryset = queryset.filter(date_start__gt=filter_start)
        if filter_end:
            queryset = queryset.filter(date_start__lt=filter_end)
        if filter_private == 'on':
            queryset = queryset.filter(is_private=True)
        elif filter_private == 'off':
            queryset = queryset.filter(is_private=False)
        if filter_available:
            queryset = queryset.filter(places_left__gt=0)

        serializer = EventSerializer(queryset.order_by('-pk'), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        GET

        Example:
            http://127.0.0.1:8000/api/events/detail/1/
        """
        queryset = Event.objects_event_qs.event_qs()
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        DELETE

        Example:
            http://127.0.0.1:8000/api/events/event_delete/37/
        """
        event = Event.objects_event_qs.event_qs().filter(id=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        """
        PATCH

        EXAMPLE:
            http://127.0.0.1:8000/api/events/event_update/37/

        {"title": "TEST_TITLE_2",
        "date_start": "2034-04-23T18:25:43.511Z"}
        """
        event = Event.objects_event_qs.event_qs().get(id=pk)
        serializer = EventSerializer(event, data=request.data,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST

        EXAMPLE:
            http://127.0.0.1:8000/api/events/event_create/

        {"title": "TEST_TITLE",
        "date_start": "2032-04-23T18:25:43.511Z",
        "category": 1,
        "participants_number": 12,
        "features": [{"id": 1}, {"id": 2}]}
        """
        try:
            new_event = Event.objects.create(title=request.data['title'],
                                             description=request.data['description'] if request.data.get(
                                                 'description') else '',
                                             date_start=request.data['date_start'],
                                             participants_number=request.data['participants_number'],
                                             is_private=request.data['is_private'] if request.data.get(
                                                 'is_private') else False,
                                             category=Category.objects.get(pk=request.data['category']))

            if request.data.get('features'):
                new_event.features.set(Feature.objects.filter(id__in=[i['id'] for i in request.data['features']]))
            new_event.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

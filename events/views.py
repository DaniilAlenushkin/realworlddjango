from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from events.models import Event, Review, Category, Feature
import datetime


def event_list(request):
    template_name = 'events/event_list.html'
    event_objects = Event.objects.all()
    category_objects = Category.objects.all()
    feature_objects = Feature.objects.all()
    context = {
        'event_objects': event_objects,
        'category_objects': category_objects,
        'feature_objects': feature_objects,
    }
    return render(request, template_name, context)


def event_detail(request, pk):
    template_name = 'events/event_detail.html'
    event = get_object_or_404(Event, pk=pk)
    places_left = event.participants_number - event.enrolls.count()
    fullness_percent = int((event.enrolls.count() / event.participants_number) * 100)
    context = {
        'event': event,
        'places_left': places_left,
        'fullness_percent': fullness_percent,

    }
    return render(request, template_name, context)


@require_POST
def create_review(request):
    data = {
        'ok': True,
        'msg': '',
        'rate': request.POST.get('rate'),
        'text': request.POST.get('text'),
        'created': datetime.date.today().strftime('%d.%m.%Y'),
        'user_name': ''
    }
    event = Event.objects.get(pk=request.POST.get('event_id'))

    if Review.objects.filter(user=request.user, event=event).exists():
        data['msg'] = 'Вы уже отправляли отзыв к этому событию'
        data['ok'] = False

    elif data['text'] == '' or data['rate'] == '':
        data['msg'] = 'Оценка и текст отзыва - обязательные поля'
        data['ok'] = False

    elif not request.user.is_authenticated:
        data['msg'] = 'Отзывы могут отправлять только зарегистрированные пользователи'
        data['ok'] = False

    else:
        data['user_name'] = request.user.__str__()

        new_review = Review(
            user=request.user,
            event=event,
            rate=data['rate'],
            text=data['text'],
            created=data['created'],
            updated=data['created']
        )

        new_review.save()

    return JsonResponse(data)

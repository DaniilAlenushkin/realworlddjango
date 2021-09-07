import datetime

from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

from events.forms import (EventUpdateForm, EventCreationForm, EnrollCreationForm,
                          EventAddToFavoriteForm, EventFilterForm)
from events.models import Event, Review, Enroll, Favorite


class LoginRequiredMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('accounts:sign_in'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('accounts:sign_in'))
        return super().post(request, *args, **kwargs)


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list/html'
    paginate_by = 50
    context_object_name = 'event_objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Cобытия'
        context['filter_form'] = EventFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Event.objects_event_qs.event_qs()
        form = EventFilterForm(self.request.GET)
        if form.is_valid():
            filter_category = form.cleaned_data['category']
            filter_features = form.cleaned_data['features']
            filter_start = form.cleaned_data['date_start']
            filter_end = form.cleaned_data['date_end']
            filter_private = form.cleaned_data['is_private']
            filter_available = form.cleaned_data['is_available']
            filter_title = form.cleaned_data['title']
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
            if filter_private:
                queryset = queryset.filter(is_private=filter_private)
            if filter_available:
                queryset = queryset.filter(places_left__gt=0)

        return queryset.order_by('-pk')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventUpdateForm

    def get_queryset(self):
        queryset = Event.objects_event_qs.event_qs()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Редактирование события'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Cобытие {form.cleaned_data["title"]} успешно изменено')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = {
            'user': self.request.user,
            'event': self.object,
        }
        context['enroll_form'] = EnrollCreationForm(initial=initial)
        context['favorite_form'] = EventAddToFavoriteForm(initial=initial)
        context['heading'] = 'Cобытие'
        return context

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = Event.objects_event_qs.event_qs().filter(pk=pk)
        return queryset


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_update.html'
    success_url = reverse_lazy('events:event_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Событие {self.object} удалено')
        return result


class EnrollDeleteView(LoginRequiredMixin,DeleteView):
    model = Enroll
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Запись на событие {self.object.event} удалена')
        return result


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Отзыв на событие {self.object.event} удален')
        return result


class FavoriteDeleteView(LoginRequiredMixin, DeleteView):
    model = Favorite
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'Событие {self.object.event} удалено из избранного')
        return result


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_update.html'
    form_class = EventCreationForm
    success_url = reverse_lazy('events:event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Добавление события'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Новое событие {form.cleaned_data["title"]} создано успешно')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class EnrollCreateView(LoginRequiredMixin, CreateView):
    model = Enroll
    form_class = EnrollCreationForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, f'Вы успешно записались на {form.cleaned_data["event"]}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)
        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))

        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)


class EventAddToFavoriteView(LoginRequiredMixin, CreateView):
    model = Favorite
    form_class = EventAddToFavoriteForm

    def get_success_url(self):
        return self.object.event.get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, f'Событие {form.cleaned_data["event"]} добавлено в избранное')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        event = form.cleaned_data.get('event', None)

        if not event:
            event = get_object_or_404(Event, pk=form.data.get('event'))
        redirect_url = event.get_absolute_url() if event else reverse_lazy('events:event_list')
        return HttpResponseRedirect(redirect_url)


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

    pk = request.POST.get('event_id', '')
    if not pk:
        data['msg'] = 'Событие не найдено'
        data['ok'] = False
        return JsonResponse(data)

    else:
        event = Event.objects.get(pk=pk)

        if not request.user.is_authenticated:
            data['msg'] = 'Отзывы могут отправлять только зарегистрированные пользователи'
            data['ok'] = False
            return JsonResponse(data)

        data['user_name'] = request.user.__str__()

        if Review.objects.filter(user=request.user, event=event).exists():
            data['msg'] = 'Вы уже отправляли отзыв к этому событию'
            data['ok'] = False

        elif data['text'] == '' or data['rate'] == '':
            data['msg'] = 'Оценка и текст отзыва - обязательные поля'
            data['ok'] = False

        else:
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

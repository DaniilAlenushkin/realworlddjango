from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from mail.forms import SubscriberCreateForm, LetterCreateForm
from mail.models import Subscriber
from events.views import PermissionRequiredMixin


class SubscriberCreateView(PermissionRequiredMixin, CreateView):
    model = Subscriber
    form_class = SubscriberCreateForm
    success_url = reverse_lazy('mail:subscriber_list')

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        messages.success(self.request, 'Подписчик успешно создан')
        return super().form_valid(form)


class SubscriberListView(PermissionRequiredMixin, ListView):
    model = Subscriber
    template_name = 'mail/subscribers_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['heading'] = 'Отправка писем'
        context['subscriber_form'] = SubscriberCreateForm()
        context['letter_form'] = LetterCreateForm()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.with_counts()

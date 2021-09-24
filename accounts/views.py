from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView

from accounts.forms import (ProfileUpdateForm, CustomPasswordResetForm, CustomSetPasswordForm)
from accounts.models import Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_objects'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        self.kwargs['pk'] = pk
        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.select_related('user').prefetch_related(
            'user__enrolls__event',
            'user__reviews__event',
            'user__favorites__event'
        )
        profile = super().get_object(queryset)
        return profile

    def get(self, request, *args, **kwargs):
        if self.request.user.id is None:
            redirect_url = reverse_lazy('account_login')
            return HttpResponseRedirect(redirect_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Профаил'
        user = Profile.objects.filter(pk=self.kwargs['pk']).first().user
        context['verified'] = EmailAddress.objects.filter(user=user).first().verified
        context['social_account'] = SocialAccount.objects.filter(user=user).exists()
        return context

    def form_valid(self, form):
        cd = form.cleaned_data
        user_update = Profile.objects.filter(pk=self.kwargs['pk']).first().user
        username = cd.get('username', '')
        full_name = cd.get('full_name', '')

        if username:
            user_update.username = username
        if full_name:
            first_name = full_name[0]
            last_name = full_name[1]
            user_update.first_name = first_name
            user_update.last_name = last_name
        user_update.save()
        messages.success(self.request, f'Данные успешно обновлены')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/registration/password_reset_email.txt'
    subject_template_name = 'accounts/registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    html_email_template_name = 'accounts/registration/password_reset_email.html'

    def form_valid(self, form):
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')
        return context


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'

from accounts.forms import (CustomUserCreationForm, ProfileUpdateForm, CustomAuthenticationForm,
                            CustomPasswordResetForm, CustomSetPasswordForm)
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from accounts.models import Profile


class CustomSignUpView(CreateView):
    model = User
    template_name = 'accounts/registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        if user is not None:
            login(self.request, user)
        return result

    def get(self, request, *args, **kwargs):
        if self.request.user.id :
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)
        return super().get(request, *args, **kwargs)


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_objects'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        self.kwargs['pk'] = pk
        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.select_related('user').prefetch_related('user__enrolls__event', 'user__reviews__event')
        profile = super().get_object(queryset)
        return profile

    def get(self, request, *args, **kwargs):
        if self.request.user.id is None:
            redirect_url = reverse_lazy('accounts:sign_in')
            return HttpResponseRedirect(redirect_url)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Профаил'
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Данные успешно обновлены')
        return super().form_valid(form)


class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/signin.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.id :
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)
        return super().get(request, *args, **kwargs)


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

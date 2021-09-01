from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from .forms import CustomPasswordChangeForm
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', views.CustomSignUpView.as_view(), name='sign_up'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign-in/', views.CustomLoginView.as_view(), name='sign_in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/',
         PasswordChangeView.as_view(
             template_name='accounts/registration/password_change.html',
             form_class=CustomPasswordChangeForm,
             success_url=reverse_lazy('accounts:password_change_done')
         ),
         name='password_change'),
    path('password-change-done/',
         PasswordChangeDoneView.as_view(
             template_name='accounts/registration/password_change_done.html'
         ),
         name='password_change_done'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<str:uidb64>/<str:token>', views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

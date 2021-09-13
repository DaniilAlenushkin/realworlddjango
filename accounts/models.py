from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    USER_ROLE_USER = 'u'
    USER_ROLE_MANAGER = 'm'
    USER_ROLE_ADMIN = 'a'

    USER_ROLE_CHOICES = [
        (USER_ROLE_USER, 'user'),
        (USER_ROLE_MANAGER, 'manager'),
        (USER_ROLE_ADMIN, 'admin')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(null=True, blank=True, upload_to='accounts/profiles/avatar', verbose_name='Аватар')
    role = models.CharField(max_length=1, null=True, choices=USER_ROLE_CHOICES,
                            default=USER_ROLE_USER, verbose_name='Роль')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'

    def get_absolute_url(self):
        return reverse('accounts:profile')

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else f'{settings.STATIC_URL}images/users/profile.svg '

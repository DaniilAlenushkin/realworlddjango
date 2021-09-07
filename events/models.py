from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from events.managers import EventQuerySet


class Category(models.Model):
    title = models.CharField(max_length=90, default='', verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.title

    def display_event_count(self):
        return self.events.count()

    display_event_count.short_description = 'Количество событий для категории'


class Feature(models.Model):
    title = models.CharField(max_length=255, default='', verbose_name='Свойства события')

    class Meta:
        verbose_name_plural = 'Свойства событий'
        verbose_name = 'Свойства события'

    def __str__(self):
        return self.title


class Event(models.Model):
    FULLNESS_EMPTY = '0'
    FULLNESS_MIDDLE = '1'
    FULLNESS_FULL = '2'

    FULLNESS_LEGEND_EMPTY = '<= 50%'
    FULLNESS_LEGEND_MIDDLE = '> 50%'
    FULLNESS_LEGEND_FULL = 'sold-out'

    FULLNESS_VARIANTS = (
        (FULLNESS_EMPTY, FULLNESS_LEGEND_EMPTY),
        (FULLNESS_MIDDLE, FULLNESS_LEGEND_MIDDLE),
        (FULLNESS_FULL, FULLNESS_LEGEND_FULL),
    )

    objects = models.Manager()
    objects_event_qs = EventQuerySet.as_manager()
    logo = models.ImageField(upload_to='events/event', blank=True, null=True,)
    title = models.CharField(max_length=200, default='', verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000), MinValueValidator(1)],
                                                           verbose_name='Количество участников')
    is_private = models.BooleanField(default=False,  verbose_name='Частное')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='events',
                                 verbose_name='Категория')
    features = models.ManyToManyField(Feature, verbose_name='Свойства событий')

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.pk)])

    def get_update_url(self):
        return reverse('events:event_update', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('events:event_delete', args=[str(self.pk)])

    def display_enroll_count(self):
        return self.enrolls.count()

    display_enroll_count.short_description = 'Количество записей'

    def display_places_left(self):
        places_left = self.participants_number - self.enrolls.count()
        if places_left == 0:
            fullness = self.FULLNESS_LEGEND_FULL
        elif self.enrolls.count() >= places_left:
            fullness = self.FULLNESS_LEGEND_MIDDLE
        else:
            fullness = self.FULLNESS_LEGEND_EMPTY
        return f'{places_left} ({fullness})'

    display_places_left.short_description = 'Осталось мест'

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/svg-icon/event.svg'


class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolls', verbose_name='Пользователь')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='enrolls', verbose_name='Событие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.event} - {self.user}'

    class Meta:
        verbose_name_plural = 'Записи на события'
        verbose_name = 'Запись на событие'

    def get_delete_url(self):
        return reverse('events:enroll_delete', args=[str(self.pk)])


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews', verbose_name='Событие')
    rate = models.PositiveSmallIntegerField(null=True, verbose_name='Оценка пользователя')
    text = models.TextField(default='', verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def get_delete_url(self):
        return reverse('events:review_delete', args=[str(self.pk)])


class Favorite(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='favorites',
                             verbose_name='Пользователь')
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE, related_name='favorites',
                              verbose_name='Событие')

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'

    class Meta:
        verbose_name_plural = 'Избранные события '
        verbose_name = 'Избранное событие'

    def get_delete_url(self):
        return reverse('events:favorite_delete', args=[str(self.pk)])

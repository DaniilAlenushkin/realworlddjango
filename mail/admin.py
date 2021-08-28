from django.contrib import admin
from . import models


@admin.register(models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Letter)
class LetterAdmin(admin.ModelAdmin):
    pass

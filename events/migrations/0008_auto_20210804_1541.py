# Generated by Django 3.2.5 on 2021-08-04 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0007_alter_enroll_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enroll',
            options={'verbose_name': 'Запись на событие', 'verbose_name_plural': 'Записи на события'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Событие', 'verbose_name_plural': 'События'},
        ),
        migrations.AddField(
            model_name='event',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='events/event'),
        ),
        migrations.AlterField(
            model_name='enroll',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='enroll',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolls', to='events.event', verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='enroll',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolls', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='event',
            name='features',
            field=models.ManyToManyField(to='events.Feature', verbose_name='Свойства событий'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='review',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='events.event', verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Изменено'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
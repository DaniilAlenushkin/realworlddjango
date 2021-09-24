from allauth.account.models import EmailAddress
from django import forms
from events.models import Event, Enroll, Favorite, Category, Feature


class EventCreateUpdateForm(forms.ModelForm):
    date_start = forms.DateTimeField(
                    label='Дата начала',
                    widget=forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['description'].widget.attrs.update({'rows': 3})
        self.fields['is_private'].widget.attrs.update({'class': 'custom_check'})


class EventCreationForm(EventCreateUpdateForm):

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if Event.objects.filter(title=title).exists():
            raise forms.ValidationError(f'Такое событие: {title} уже существует')
        return cleaned_data


class EventUpdateForm(EventCreateUpdateForm):
    pass


class EnrollCreationForm(forms.ModelForm):
    class Meta:
        model = Enroll
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        event = cleaned_data.get('event')

        if Enroll.objects.filter(event=event).count() == event.participants_number:
            raise forms.ValidationError(f'Места на {event} кончились, увы')

        if event.is_private and not user.profile.access_to_private_events:
            raise forms.ValidationError(f'Cобытие {event} приватное')

        if Enroll.objects.filter(user=user, event=event).exists():
            raise forms.ValidationError(f'Вы уже записаны на это событие. Отменить запись можно в профиле.')

        if not EmailAddress.objects.filter(user=user).first().verified:
            raise forms.ValidationError(f'Подтвердите свой email-адресс')

        return cleaned_data


class EventAddToFavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        event = cleaned_data.get('event')
        if Favorite.objects.filter(user=user, event=event).exists():
            raise forms.ValidationError(f'Событие уже добавлено в избранное. Изменить это можно в профиле.')
        return cleaned_data


class EventFilterForm(forms.Form):
    title = forms.CharField(label='Название', required=False)
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), required=False)
    features = forms.ModelMultipleChoiceField(label='Свойства', queryset=Feature.objects.all(), required=False)
    date_start = forms.DateTimeField(label='Дата начала',
                                     widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
                                     required=False)
    date_end = forms.DateTimeField(label='Дата Конца',
                                   widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
                                   required=False)
    is_private = forms.BooleanField(label='Приватное',
                                    widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                                    required=False)
    is_available = forms.BooleanField(label='Есть места',
                                      widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
                                      required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['features'].widget.attrs.update({'class': 'form-select', 'multiple': True})
        self.fields['date_start'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_end'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})

from django import forms
from events.models import Event, Enroll, Favorite


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
            field.widget.attrs.update({'class': 'special'})

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
        if Enroll.objects.filter(user=user, event=event).exists():
            raise forms.ValidationError(f'Вы уже записаны на это событие: ')
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
            raise forms.ValidationError(f'Событие уже добавлено в избранное')
        return cleaned_data

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # динамически задаем плейсхолдеры и класс хтмл-ки
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():  # тут мы нужный класс подставляем
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # динамически задаем плейсхолдеры и класс хтмл-ки\
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилиё'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():  # тут мы нужный класс подставляем
            field.widget.attrs['class'] = 'form-control py-4'


class UserProfileForm(UserChangeForm):

    image = forms.ImageField(widget=forms.FileInput, required=False)  # required=False - поле может быть пустым

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():  # тут мы нужный класс подставляем всем полям
            field.widget.attrs['class'] = 'form-control py-4'

        self.fields['image'].widget.attrs['class'] = 'custom-file-input'  # изображение д.быть другого класса

    # валидация поля
    def clean_image(self):
        data = self.cleaned_data['image']
        if data.size > 1024000:
            raise forms.ValidationError('Размер изображения не должен превышать 1024 КБ')
        return data

    # def clean_last_name(self): Это для тренировки
    #     data = self.cleaned_data['last_name']
    #     if not any(c.isupper() for c in data):
    #         self.add_error('last_name', 'last_name should contain an upper character')
    #     return data


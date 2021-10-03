from django import forms

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

class UserAdminRegisterForm(UserRegisterForm):

    image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # тут мы нужный класс подставляем
            if field_name == 'image':  # переопределяем так как классы съехали
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProfileForm(UserProfileForm):
    # класс мета нам не нужен тут потому что тут нет новых полей, работаем со старыми
    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'first_name', 'last_name', 'image')

    def __init__(self,*args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


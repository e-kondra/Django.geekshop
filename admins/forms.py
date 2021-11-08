from django import forms

from mainapp.models import ProductCategory, Product
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

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class CategoryAdminCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super(CategoryAdminCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        for field_name, field in self.fields.items():  # подставляем всем полям нужный класс
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-inline'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class CategoryAdminUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super(CategoryAdminUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():  # подставляем всем полям нужный класс
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-inline'
            else:
                field.widget.attrs['class'] = 'form-control py-4'



class ProductAdminRegisterForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    category = forms.ModelChoiceField(widget=forms.Select(), queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category','is_active')

    def __init__(self, *args, **kwargs):
        super(ProductAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['select'] = ProductCategory.objects.all()
        for field_name, field in self.fields.items():  # подставляем всем полям нужный класс
            if field_name == 'image':
                field.widget.attrs['class'] = 'custom-file-input'
            elif field_name == 'category':
                field.widget.attrs['class'] = 'custom-select'
            elif field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-inline'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class ProductAdminUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    category = forms.ModelChoiceField(widget=forms.Select(), queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category', 'is_active')

    def __init__(self, *args, **kwargs):
        super(ProductAdminUpdateForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == 'image':  # переопределяем так как классы съехали
                field.widget.attrs['class'] = 'custom-file-input'
            elif field_name == 'category':
                field.widget.attrs['class'] = 'custom-select'
            elif field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-inline'
            else:
                field.widget.attrs['class'] = 'form-control py-4'

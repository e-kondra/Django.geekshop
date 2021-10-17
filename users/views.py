from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse, reverse_lazy
import django.contrib.messages as messages
from django.utils.decorators import method_decorator
from django.views.generic.edit import (
FormView, UpdateView,
)

# Create your views here.
from geekshop.mixin import BaseClassContextMixin, LoginsRequiredMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from baskets.models import Basket
from users.models import User


class UserLoginView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Geekshop - Авторизация'


#
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)  # авторизовываем
#                 return HttpResponseRedirect(
#                     reverse('index'))  # перенаправление :reverse('index') - путь до страницы сайта index
#     else:
#         form = UserLoginForm()  # если форма невалидна, возвращаем пустую форму в контекст
#
#     context = {
#         'title': 'Geekshop - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


class UserRegisterView(FormView, BaseClassContextMixin):

    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Geekshop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_link(user):
                messages.success(request, 'Вы успешно зарегистрировались! Необходимо активировать профиль: на указанный mail Вам была отправлена ссылка для активации.')
                return redirect(self.success_url)
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        #return redirect(self.success_url)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация успешна!')
#             return HttpResponseRedirect(
#                 reverse('users:login'))  # перенаправление :reverse('index') - путь до страницы сайта входа пользователя
#         # else:
#         #     print(form.errors)  # ошибки формы теперь обрабатываем в html через динамич.шаблоны
#     else:
#         form = UserRegisterForm()  # если форма невалидна, возвращаем пустую форму в контекст
#     context = {
#         'title': 'Geekshop - Регистрация',
#         'form': form
#     }
#     return render(request, 'users/register.html', context)

class UserProfileView(UpdateView, BaseClassContextMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop - Профайл'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


# @login_required
# def profile(request):
#     if request.method == 'POST':  # пост-запрос на сохранение измененных данных
#         form = UserProfileForm(data=request.POST,
#                                instance=request.user,  # в параметре instance передаем какого юзера обновлять
#                                files=request.FILES)  # указываем, что необходимо сохранять и файлы
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Данные успешно изменены!')
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             messages.error(request, form.errors)
#
#     baskets = Basket.objects.filter(user=request.user)
#     context = {
#         'title': 'Geekshop - Профайл',
#         'form': UserProfileForm(instance=request.user),  # параметр instance позволяет передать данные из пользователя
#         'baskets': baskets,
#         # Это способ для подсчет сумм из view (но лучше из baskets.model.py, так как память надо во вью экономить, поэтому этот оставляю как пример)
#         # 'total_quantity': sum(basket.quantity for basket in baskets),
#         # 'total_sum': sum(basket.sum() for basket in baskets)
#     }
#     return render(request, 'users/profile.html', context)


# @login_required
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

class UserLogoutView(LogoutView):
    template_name = 'mainapp/index.html'


def send_verify_link(user):
    verify_link = reverse('users:verify',args=[user.email, user.activation_key]) # сделали ссылку
    subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
    message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''  # сбрасываем ключ активации и дату/время, они больше не нужен, чтоб память не занимали
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user) # авторизуем юзера
        return render(request, 'users/verification.html') # перенаправляем на страницу верификации, там ему скажут успешно или нет
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
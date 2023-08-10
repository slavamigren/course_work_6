from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from django.contrib.auth.base_user import BaseUserManager

from conf import settings
from users.forms import RegisterForm, LoginViewForm, UserForm
from users.models import User

class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = LoginViewForm
    success_url = reverse_lazy('catalog:index')


class LogoutView(BaseLogoutView):
    pass


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request):  # отправляет на почту пользователю новый пароль
    new_password = BaseUserManager().make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    send_mail(subject='Смена пароля',
              message=f'Ваш пароль на платформе Рассылки был изменён на {new_password}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[request.user.email])
    return redirect(reverse('users:login'))


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        verification_code = BaseUserManager().make_random_password()
        self.object.verification_code = verification_code
        self.object.save(update_fields=['verification_code'])
        send_mail(subject='Регистрация на платформе Рассылки',
                  message=f'Ваш код для верификации: {verification_code}',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[self.object.email])
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('users:verification_new_user', args=[self.object.pk])


def verification_new_user(request, pk):  # верифицирует пользователя по коду с почты
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        try:
            new_user = User.objects.get(verification_code=verification_code)
        except:
            context = {
                'first_trial': False,
                'pk': pk,
            }
            return render(request, 'users/verification.html', context)
        else:
            new_user.is_active = True
            new_user.verification_code = ''
            new_user.save(update_fields=['is_active', 'verification_code'])
            login(request, new_user)  # авторизуем пользователя и отправляем на главную страницу
            return redirect(reverse('mailing:mailing_list'))
            # return redirect(reverse('users:login')) #  если не авторизовать сразу, можно отправить на авторизацию
    else:
        context = {
            'first_trial': True,
            'pk': pk
        }
        return render(request, 'users/verification.html', context)


def send_new_verification_code(request, pk):  # отправляет новый код верификации на почту
    try:
        new_user = User.objects.get(pk=pk)
        user_email = new_user.email
        verification_code = BaseUserManager().make_random_password()
        new_user.verification_code = verification_code
        new_user.save(update_fields=['verification_code'])

        send_mail(subject='Регистрация на платформе Skystore',
                  message=f'Ваш код для верификации: {verification_code}',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[user_email])
        return redirect(reverse('users:verification_new_user', args=[pk]))

    except:
        return redirect(reverse('users:verification_new_user', args=[pk]))
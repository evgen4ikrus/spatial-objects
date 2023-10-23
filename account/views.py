from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'У вас нет доступа к сайту')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, template_name='login.html', context={'form': form})
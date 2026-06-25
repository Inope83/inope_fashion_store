from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import Kliente, Notifikasaun
from .forms import LoginForm, RegistForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                kliente = Kliente.objects.get(email=email)
                if kliente.check_password(password):
                    kliente.last_login = timezone.now()
                    kliente.save(update_fields=['last_login'])
                    request.session['kliente_id'] = kliente.id
                    request.session['kliente_naran'] = kliente.naran
                    messages.success(request, f'Benvingudu, {kliente.naran}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Email ka password la los')
            except Kliente.DoesNotExist:
                messages.error(request, 'Email ka password la los')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def regist_view(request):
    if request.method == 'POST':
        form = RegistForm(request.POST)
        if form.is_valid():
            kliente = form.save()
            messages.success(request, 'Registrasaun suksesu! Ita bele login agora.')
            return redirect('login')
    else:
        form = RegistForm()
    return render(request, 'users/regist.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Ita sai ona.')
    return redirect('home')


def perfil_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('login')
    kliente = Kliente.objects.get(id=kliente_id)
    return render(request, 'users/perfil.html', {'kliente': kliente})


def notifikasaun_list_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('login')
    notifikasauns = Notifikasaun.objects.filter(kliente_id=kliente_id).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifikasauns': notifikasauns})

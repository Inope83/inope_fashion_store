from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.utils import timezone
from .models import Kliente, Notifikasaun, Admin
from .forms import LoginForm, RegistForm, PerfilForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            kliente = None
            try:
                admin = Admin.objects.get(username=email)
                if admin.check_password(password):
                    kliente, _ = Kliente.objects.get_or_create(
                        email=admin.username,
                        defaults={'naran': admin.username, 'is_staff': True},
                    )
                    if kliente.password != admin.password or not kliente.is_staff:
                        kliente.password = admin.password
                        kliente.is_staff = True
                        kliente.save()
            except Admin.DoesNotExist:
                try:
                    kliente = Kliente.objects.get(email=email)
                except Kliente.DoesNotExist:
                    pass
            if kliente and kliente.check_password(password):
                kliente.last_login = timezone.now()
                kliente.save(update_fields=['last_login'])
                request.session['kliente_id'] = kliente.id
                request.session['kliente_naran'] = kliente.naran
                if kliente.is_staff:
                    request.session['admin_id'] = kliente.id
                    request.session['admin_username'] = kliente.naran
                    messages.success(request, f'Bemvindu, {kliente.naran}!')
                    next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard:dashboard_home'
                    return redirect(next_url)
                messages.success(request, f'Bemvindu, {kliente.naran}!')
                next_url = request.POST.get('next') or request.GET.get('next') or 'home'
                return redirect(next_url)
            messages.error(request, 'Email ka password la los')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def regist_view(request):
    if request.method == 'POST':
        form = RegistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrasaun suksesu! Ita bele tama agora.')
            next_url = request.POST.get('next') or request.GET.get('next') or 'kliente_login'
            return redirect(next_url)
    else:
        form = RegistForm()
    return render(request, 'users/regist.html', {'form': form})


def logout_view(request):
    request.session.pop('kliente_id', None)
    request.session.pop('kliente_naran', None)
    request.session.pop('admin_id', None)
    request.session.pop('admin_username', None)
    messages.info(request, 'Ita sai ona.')
    return redirect('home')


def django_logout_view(request):
    request.session.pop('kliente_id', None)
    request.session.pop('kliente_naran', None)
    request.session.pop('admin_id', None)
    request.session.pop('admin_username', None)
    auth_logout(request)
    messages.info(request, 'Ita sai ona.')
    return redirect('home')


def perfil_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('kliente_login')
    kliente = get_object_or_404(Kliente, id=kliente_id)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=kliente)
        if form.is_valid():
            form.save()
            request.session['kliente_naran'] = kliente.naran
            messages.success(request, 'Perfil atualiza ona!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=kliente)
    return render(request, 'users/perfil.html', {'kliente': kliente, 'form': form})


def notifikasaun_list_view(request):
    kliente_id = request.session.get('kliente_id')
    if not kliente_id:
        return redirect('kliente_login')
    if not Kliente.objects.filter(id=kliente_id).exists():
        request.session.flush()
        return redirect('kliente_login')
    notifikasauns = Notifikasaun.objects.filter(kliente_id=kliente_id).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifikasauns': notifikasauns})

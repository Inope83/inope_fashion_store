from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.db.models import Sum
from django.contrib import messages
from apps.products.models import Produtu, Kategoria
from apps.orders.models import Pedidu, DetalloPedidu, Pagamentu
from apps.users.models import Kliente, Notifikasaun
from apps.users.models import Admin
from .forms import DashboardKlienteForm, DashboardAdminForm, DashboardProdutuForm


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        kliente_id = request.session.get('kliente_id')
        if not kliente_id and request.user.is_authenticated:
            kliente, _ = Kliente.objects.get_or_create(
                email=request.user.email,
                defaults={
                    'naran': request.user.get_full_name() or request.user.username,
                    'is_staff': True,
                },
            )
            if not kliente.is_staff and (request.user.is_superuser or request.user.is_staff):
                kliente.is_staff = True
                kliente.save(update_fields=['is_staff'])
            if kliente.is_staff:
                kliente_id = kliente.id
                request.session['kliente_id'] = kliente.id
                request.session['kliente_naran'] = kliente.naran
                request.session['admin_id'] = kliente.id
                request.session['admin_username'] = kliente.naran
        if not kliente_id:
            return redirect(f"{reverse('kliente_login')}?next={request.path}")
        if not Kliente.objects.filter(id=kliente_id, is_staff=True).exists():
            return redirect(f"{reverse('kliente_login')}?next={request.path}")
        return super().dispatch(request, *args, **kwargs)


class DashboardMixin(AdminRequiredMixin):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active'] = self.active_page
        ctx['title'] = self.page_title
        ctx['cancel_url'] = self.cancel_url
        return ctx


class DashboardHome(AdminRequiredMixin, ListView):
    template_name = 'dashboard/home.html'
    context_object_name = 'recent_pedidus'
    queryset = Pedidu.objects.select_related('kliente').order_by('-created_at')[:5]
    active_page = 'home'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active'] = 'home'
        ctx['total_produtu'] = Produtu.objects.count()
        ctx['total_pedidu'] = Pedidu.objects.count()
        ctx['total_kliente'] = Kliente.objects.count()
        ctx['total_receita'] = Pagamentu.objects.filter(status='pagu').aggregate(Sum('total'))['total__sum'] or 0
        return ctx


# ─── Kategoria CRUD ───

class KategoriaList(DashboardMixin, ListView):
    model = Kategoria
    template_name = 'dashboard/kategoria_list.html'
    active_page = 'product'
    page_title = 'Kategoria'
    cancel_url = reverse_lazy('dashboard:kategoria_list')


class KategoriaCreate(DashboardMixin, CreateView):
    model = Kategoria
    fields = ['naran', 'deskrisaun']
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Kategoria Foun'
    cancel_url = reverse_lazy('dashboard:kategoria_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:kategoria_list')


class KategoriaUpdate(DashboardMixin, UpdateView):
    model = Kategoria
    fields = ['naran', 'deskrisaun']
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Edita Kategoria'
    cancel_url = reverse_lazy('dashboard:kategoria_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:kategoria_list')


class KategoriaDelete(DashboardMixin, DeleteView):
    model = Kategoria
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'product'
    page_title = 'Hamos Kategoria'
    cancel_url = reverse_lazy('dashboard:kategoria_list')
    success_url = reverse_lazy('dashboard:kategoria_list')


# ─── Produtu CRUD ───

class ProdutuList(DashboardMixin, ListView):
    model = Produtu
    template_name = 'dashboard/produtu_list.html'
    active_page = 'produtu'
    page_title = 'Produtu'
    cancel_url = reverse_lazy('dashboard:produtu_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['kategorias'] = Kategoria.objects.all()
        return ctx


class ProdutuCreate(DashboardMixin, CreateView):
    model = Produtu
    form_class = DashboardProdutuForm
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Produtu Foun'
    cancel_url = reverse_lazy('dashboard:produtu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:produtu_list')


class ProdutuUpdate(DashboardMixin, UpdateView):
    model = Produtu
    form_class = DashboardProdutuForm
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Edita Produtu'
    cancel_url = reverse_lazy('dashboard:produtu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:produtu_list')


class ProdutuDelete(DashboardMixin, DeleteView):
    model = Produtu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'product'
    page_title = 'Hamos Produtu'
    cancel_url = reverse_lazy('dashboard:produtu_list')
    success_url = reverse_lazy('dashboard:produtu_list')


# ─── Kliente CRUD ───

class KlienteList(DashboardMixin, ListView):
    model = Kliente
    template_name = 'dashboard/kliente_list.html'
    active_page = 'kliente'
    page_title = 'Kliente'
    cancel_url = reverse_lazy('dashboard:kliente_list')


class KlienteCreate(DashboardMixin, CreateView):
    model = Kliente
    form_class = DashboardKlienteForm
    template_name = 'dashboard/crud_form.html'
    active_page = 'kliente'
    page_title = 'Kliente Foun'
    cancel_url = reverse_lazy('dashboard:kliente_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:kliente_list')


class KlienteUpdate(DashboardMixin, UpdateView):
    model = Kliente
    form_class = DashboardKlienteForm
    template_name = 'dashboard/crud_form.html'
    active_page = 'kliente'
    page_title = 'Edita Kliente'
    cancel_url = reverse_lazy('dashboard:kliente_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:kliente_list')


class KlienteDelete(DashboardMixin, DeleteView):
    model = Kliente
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'kliente'
    page_title = 'Hamos Kliente'
    cancel_url = reverse_lazy('dashboard:kliente_list')
    success_url = reverse_lazy('dashboard:kliente_list')


# ─── Notifikasaun CRUD ───

class NotifikasaunList(DashboardMixin, ListView):
    model = Notifikasaun
    template_name = 'dashboard/notifikasaun_list.html'
    active_page = 'notifikasaun'
    page_title = 'Notifikasaun'
    cancel_url = reverse_lazy('dashboard:notifikasaun_list')


class NotifikasaunCreate(DashboardMixin, CreateView):
    model = Notifikasaun
    fields = ['kliente', 'mensajen', 'tipu', 'pedidu']
    template_name = 'dashboard/crud_form.html'
    active_page = 'notifikasaun'
    page_title = 'Notifikasaun Foun'
    cancel_url = reverse_lazy('dashboard:notifikasaun_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:notifikasaun_list')


class NotifikasaunUpdate(DashboardMixin, UpdateView):
    model = Notifikasaun
    fields = ['kliente', 'mensajen', 'tipu', 'pedidu']
    template_name = 'dashboard/crud_form.html'
    active_page = 'notifikasaun'
    page_title = 'Edita Notifikasaun'
    cancel_url = reverse_lazy('dashboard:notifikasaun_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:notifikasaun_list')


class NotifikasaunDelete(DashboardMixin, DeleteView):
    model = Notifikasaun
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'notifikasaun'
    page_title = 'Hamos Notifikasaun'
    cancel_url = reverse_lazy('dashboard:notifikasaun_list')
    success_url = reverse_lazy('dashboard:notifikasaun_list')


# ─── Pedidu CRUD ───

class PediduList(DashboardMixin, ListView):
    model = Pedidu
    template_name = 'dashboard/pedidu_list.html'
    active_page = 'pedidu'
    page_title = 'Pedidu'
    cancel_url = reverse_lazy('dashboard:pedidu_list')


class PediduCreate(DashboardMixin, CreateView):
    model = Pedidu
    fields = ['kliente', 'status', 'total', 'enderesu']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Pedidu Foun'
    cancel_url = reverse_lazy('dashboard:pedidu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:pedidu_list')


class PediduUpdate(DashboardMixin, UpdateView):
    model = Pedidu
    fields = ['kliente', 'status', 'total', 'enderesu']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Edita Pedidu'
    cancel_url = reverse_lazy('dashboard:pedidu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:pedidu_list')


class PediduDelete(DashboardMixin, DeleteView):
    model = Pedidu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'order'
    page_title = 'Hamos Pedidu'
    cancel_url = reverse_lazy('dashboard:pedidu_list')
    success_url = reverse_lazy('dashboard:pedidu_list')


# ─── DetalloPedidu CRUD ───

class DetalloPediduList(DashboardMixin, ListView):
    model = DetalloPedidu
    template_name = 'dashboard/detallopedidu_list.html'
    active_page = 'detallu'
    page_title = 'Detallu Pedidu'
    cancel_url = reverse_lazy('dashboard:detallopedidu_list')


class DetalloPediduCreate(DashboardMixin, CreateView):
    model = DetalloPedidu
    fields = ['pedidu', 'produtu', 'kantidade', 'subtotal']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Detallu Foun'
    cancel_url = reverse_lazy('dashboard:detallopedidu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:detallopedidu_list')


class DetalloPediduUpdate(DashboardMixin, UpdateView):
    model = DetalloPedidu
    fields = ['pedidu', 'produtu', 'kantidade', 'subtotal']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Edita Detallu'
    cancel_url = reverse_lazy('dashboard:detallopedidu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:detallopedidu_list')


class DetalloPediduDelete(DashboardMixin, DeleteView):
    model = DetalloPedidu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'order'
    page_title = 'Hamos Detallu'
    cancel_url = reverse_lazy('dashboard:detallopedidu_list')
    success_url = reverse_lazy('dashboard:detallopedidu_list')


# ─── Pagamentu CRUD ───

class PagamentuList(DashboardMixin, ListView):
    model = Pagamentu
    template_name = 'dashboard/pagamentu_list.html'
    active_page = 'pagamentu'
    page_title = 'Pagamentu'
    cancel_url = reverse_lazy('dashboard:pagamentu_list')


class PagamentuCreate(DashboardMixin, CreateView):
    model = Pagamentu
    fields = ['pedidu', 'metodu', 'total', 'status']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Pagamentu Foun'
    cancel_url = reverse_lazy('dashboard:pagamentu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:pagamentu_list')


class PagamentuUpdate(DashboardMixin, UpdateView):
    model = Pagamentu
    fields = ['pedidu', 'metodu', 'total', 'status']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Edita Pagamentu'
    cancel_url = reverse_lazy('dashboard:pagamentu_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:pagamentu_list')


class PagamentuDelete(DashboardMixin, DeleteView):
    model = Pagamentu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'order'
    page_title = 'Hamos Pagamentu'
    cancel_url = reverse_lazy('dashboard:pagamentu_list')
    success_url = reverse_lazy('dashboard:pagamentu_list')


# ─── Admin CRUD ───

class AdminList(DashboardMixin, ListView):
    model = Admin
    template_name = 'dashboard/admin_list.html'
    active_page = 'admin'
    page_title = 'Administrador'
    cancel_url = reverse_lazy('dashboard:admin_list')


class AdminCreate(DashboardMixin, CreateView):
    model = Admin
    form_class = DashboardAdminForm
    template_name = 'dashboard/crud_form.html'
    active_page = 'admin'
    page_title = 'Administrador Foun'
    cancel_url = reverse_lazy('dashboard:admin_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:admin_list')


class AdminUpdate(DashboardMixin, UpdateView):
    model = Admin
    form_class = DashboardAdminForm
    template_name = 'dashboard/crud_form.html'
    active_page = 'admin'
    page_title = 'Edita Administrador'
    cancel_url = reverse_lazy('dashboard:admin_list')

    def get_success_url(self):
        return reverse_lazy('dashboard:admin_list')


class AdminDelete(DashboardMixin, DeleteView):
    model = Admin
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'admin'
    page_title = 'Hamos Administrador'
    cancel_url = reverse_lazy('dashboard:admin_list')
    success_url = reverse_lazy('dashboard:admin_list')


# ─── Dashboard Auth ───

def dashboard_login_view(request):
    if request.session.get('kliente_id'):
        return redirect('dashboard:dashboard_home')
    return redirect('kliente_login')


def dashboard_logout_view(request):
    request.session.pop('admin_id', None)
    request.session.pop('admin_username', None)
    request.session.pop('kliente_id', None)
    request.session.pop('kliente_naran', None)
    messages.info(request, 'Ita sai ona.')
    return redirect('dashboard:dashboard_login')

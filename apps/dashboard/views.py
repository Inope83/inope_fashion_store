from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from apps.products.models import Produtu, Kategoria
from apps.orders.models import Pedidu, DetalloPedidu, Pagamentu
from apps.users.models import Kliente, Notifikasaun
from apps.users.models import Admin


class DashboardMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active'] = self.active_page
        ctx['title'] = self.page_title
        ctx['cancel_url'] = self.cancel_url
        return ctx


class DashboardHome(ListView):
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
        ctx['total_receita'] = Pagamentu.objects.filter(estado='pagu').aggregate(Sum('total'))['total__sum'] or 0
        return ctx


# ─── Kategoria CRUD ───

class KategoriaList(DashboardMixin, ListView):
    model = Kategoria
    template_name = 'dashboard/kategoria_list.html'
    active_page = 'product'
    page_title = 'Kategoria'
    cancel_url = reverse_lazy('kategoria_list')


class KategoriaCreate(DashboardMixin, CreateView):
    model = Kategoria
    fields = ['naran', 'deskrisaun']
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Kategoria Foun'
    cancel_url = reverse_lazy('kategoria_list')

    def get_success_url(self):
        return reverse_lazy('kategoria_list')


class KategoriaUpdate(DashboardMixin, UpdateView):
    model = Kategoria
    fields = ['naran', 'deskrisaun']
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Edita Kategoria'
    cancel_url = reverse_lazy('kategoria_list')

    def get_success_url(self):
        return reverse_lazy('kategoria_list')


class KategoriaDelete(DashboardMixin, DeleteView):
    model = Kategoria
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'product'
    page_title = 'Hamos Kategoria'
    cancel_url = reverse_lazy('kategoria_list')
    success_url = reverse_lazy('kategoria_list')


# ─── Produtu CRUD ───

class ProdutuList(DashboardMixin, ListView):
    model = Produtu
    template_name = 'dashboard/produtu_list.html'
    active_page = 'produtu'
    page_title = 'Produtu'
    cancel_url = reverse_lazy('produtu_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['kategorias'] = Kategoria.objects.all()
        return ctx


class ProdutuCreate(DashboardMixin, CreateView):
    model = Produtu
    fields = ['naran', 'deskrisaun', 'preco', 'stok', 'imagem', 'kategoria']
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Produtu Foun'
    cancel_url = reverse_lazy('produtu_list')

    def get_success_url(self):
        return reverse_lazy('produtu_list')


class ProdutuUpdate(DashboardMixin, UpdateView):
    model = Produtu
    fields = ['naran', 'deskrisaun', 'preco', 'stok', 'imagem', 'kategoria']
    template_name = 'dashboard/crud_form.html'
    active_page = 'product'
    page_title = 'Edita Produtu'
    cancel_url = reverse_lazy('produtu_list')

    def get_success_url(self):
        return reverse_lazy('produtu_list')


class ProdutuDelete(DashboardMixin, DeleteView):
    model = Produtu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'product'
    page_title = 'Hamos Produtu'
    cancel_url = reverse_lazy('produtu_list')
    success_url = reverse_lazy('produtu_list')


# ─── Kliente CRUD ───

class KlienteList(DashboardMixin, ListView):
    model = Kliente
    template_name = 'dashboard/kliente_list.html'
    active_page = 'kliente'
    page_title = 'Kliente'
    cancel_url = reverse_lazy('kliente_list')


class KlienteCreate(DashboardMixin, CreateView):
    model = Kliente
    fields = ['naran', 'email', 'password']
    template_name = 'dashboard/crud_form.html'
    active_page = 'kliente'
    page_title = 'Kliente Foun'
    cancel_url = reverse_lazy('kliente_list')

    def get_success_url(self):
        return reverse_lazy('kliente_list')


class KlienteUpdate(DashboardMixin, UpdateView):
    model = Kliente
    fields = ['naran', 'email', 'password']
    template_name = 'dashboard/crud_form.html'
    active_page = 'kliente'
    page_title = 'Edita Kliente'
    cancel_url = reverse_lazy('kliente_list')

    def get_success_url(self):
        return reverse_lazy('kliente_list')


class KlienteDelete(DashboardMixin, DeleteView):
    model = Kliente
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'kliente'
    page_title = 'Hamos Kliente'
    cancel_url = reverse_lazy('kliente_list')
    success_url = reverse_lazy('kliente_list')


# ─── Notifikasaun CRUD ───

class NotifikasaunList(DashboardMixin, ListView):
    model = Notifikasaun
    template_name = 'dashboard/notifikasaun_list.html'
    active_page = 'notifikasaun'
    page_title = 'Notifikasaun'
    cancel_url = reverse_lazy('notifikasaun_list')


class NotifikasaunCreate(DashboardMixin, CreateView):
    model = Notifikasaun
    fields = ['kliente', 'mensajen', 'tipu', 'pedidu']
    template_name = 'dashboard/crud_form.html'
    active_page = 'notifikasaun'
    page_title = 'Notifikasaun Foun'
    cancel_url = reverse_lazy('notifikasaun_list')

    def get_success_url(self):
        return reverse_lazy('notifikasaun_list')


class NotifikasaunUpdate(DashboardMixin, UpdateView):
    model = Notifikasaun
    fields = ['kliente', 'mensajen', 'tipu', 'pedidu']
    template_name = 'dashboard/crud_form.html'
    active_page = 'notifikasaun'
    page_title = 'Edita Notifikasaun'
    cancel_url = reverse_lazy('notifikasaun_list')

    def get_success_url(self):
        return reverse_lazy('notifikasaun_list')


class NotifikasaunDelete(DashboardMixin, DeleteView):
    model = Notifikasaun
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'notifikasaun'
    page_title = 'Hamos Notifikasaun'
    cancel_url = reverse_lazy('notifikasaun_list')
    success_url = reverse_lazy('notifikasaun_list')


# ─── Pedidu CRUD ───

class PediduList(DashboardMixin, ListView):
    model = Pedidu
    template_name = 'dashboard/pedidu_list.html'
    active_page = 'pedidu'
    page_title = 'Pedidu'
    cancel_url = reverse_lazy('pedidu_list')


class PediduCreate(DashboardMixin, CreateView):
    model = Pedidu
    fields = ['kliente', 'estado', 'total', 'endeereco_entrega']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Pedidu Foun'
    cancel_url = reverse_lazy('pedidu_list')

    def get_success_url(self):
        return reverse_lazy('pedidu_list')


class PediduUpdate(DashboardMixin, UpdateView):
    model = Pedidu
    fields = ['kliente', 'estado', 'total', 'endeereco_entrega']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Edita Pedidu'
    cancel_url = reverse_lazy('pedidu_list')

    def get_success_url(self):
        return reverse_lazy('pedidu_list')


class PediduDelete(DashboardMixin, DeleteView):
    model = Pedidu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'order'
    page_title = 'Hamos Pedidu'
    cancel_url = reverse_lazy('pedidu_list')
    success_url = reverse_lazy('pedidu_list')


# ─── DetalloPedidu CRUD ───

class DetalloPediduList(DashboardMixin, ListView):
    model = DetalloPedidu
    template_name = 'dashboard/detallopedidu_list.html'
    active_page = 'detallu'
    page_title = 'Detallu Pedidu'
    cancel_url = reverse_lazy('detallopedidu_list')


class DetalloPediduCreate(DashboardMixin, CreateView):
    model = DetalloPedidu
    fields = ['pedidu', 'produtu', 'kantidade', 'subtotal']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Detallu Foun'
    cancel_url = reverse_lazy('detallopedidu_list')

    def get_success_url(self):
        return reverse_lazy('detallopedidu_list')


class DetalloPediduUpdate(DashboardMixin, UpdateView):
    model = DetalloPedidu
    fields = ['pedidu', 'produtu', 'kantidade', 'subtotal']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Edita Detallu'
    cancel_url = reverse_lazy('detallopedidu_list')

    def get_success_url(self):
        return reverse_lazy('detallopedidu_list')


class DetalloPediduDelete(DashboardMixin, DeleteView):
    model = DetalloPedidu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'order'
    page_title = 'Hamos Detallu'
    cancel_url = reverse_lazy('detallopedidu_list')
    success_url = reverse_lazy('detallopedidu_list')


# ─── Pagamentu CRUD ───

class PagamentuList(DashboardMixin, ListView):
    model = Pagamentu
    template_name = 'dashboard/pagamentu_list.html'
    active_page = 'pagamentu'
    page_title = 'Pagamentu'
    cancel_url = reverse_lazy('pagamentu_list')


class PagamentuCreate(DashboardMixin, CreateView):
    model = Pagamentu
    fields = ['pedidu', 'metodu', 'total', 'estado']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Pagamentu Foun'
    cancel_url = reverse_lazy('pagamentu_list')

    def get_success_url(self):
        return reverse_lazy('pagamentu_list')


class PagamentuUpdate(DashboardMixin, UpdateView):
    model = Pagamentu
    fields = ['pedidu', 'metodu', 'total', 'estado']
    template_name = 'dashboard/crud_form.html'
    active_page = 'order'
    page_title = 'Edita Pagamentu'
    cancel_url = reverse_lazy('pagamentu_list')

    def get_success_url(self):
        return reverse_lazy('pagamentu_list')


class PagamentuDelete(DashboardMixin, DeleteView):
    model = Pagamentu
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'order'
    page_title = 'Hamos Pagamentu'
    cancel_url = reverse_lazy('pagamentu_list')
    success_url = reverse_lazy('pagamentu_list')


# ─── Admin CRUD ───

class AdminList(DashboardMixin, ListView):
    model = Admin
    template_name = 'dashboard/admin_list.html'
    active_page = 'admin'
    page_title = 'Admin'
    cancel_url = reverse_lazy('admin_list')


class AdminCreate(DashboardMixin, CreateView):
    model = Admin
    fields = ['username', 'password']
    template_name = 'dashboard/crud_form.html'
    active_page = 'admin'
    page_title = 'Admin Foun'
    cancel_url = reverse_lazy('admin_list')

    def get_success_url(self):
        return reverse_lazy('admin_list')


class AdminUpdate(DashboardMixin, UpdateView):
    model = Admin
    fields = ['username', 'password']
    template_name = 'dashboard/crud_form.html'
    active_page = 'admin'
    page_title = 'Edita Admin'
    cancel_url = reverse_lazy('admin_list')

    def get_success_url(self):
        return reverse_lazy('admin_list')


class AdminDelete(DashboardMixin, DeleteView):
    model = Admin
    template_name = 'dashboard/crud_confirm_delete.html'
    active_page = 'admin'
    page_title = 'Hamos Admin'
    cancel_url = reverse_lazy('admin_list')
    success_url = reverse_lazy('admin_list')

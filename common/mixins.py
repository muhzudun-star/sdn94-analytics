"""
Base view generik untuk CRUD di semua app data master
(kepegawaian, akademik, siswa, penilaian).

Disatukan di sini (bukan di masing-masing app) supaya keempat app
tidak duplikat kode dan tetap konsisten tampilannya.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages


class AdminRequiredMixin(UserPassesTestMixin):
    """Hanya user dengan role ADMIN (atau superuser) yang boleh mengelola data master."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        profile = getattr(user, 'profile', None)
        return bool(user.is_superuser or (profile and profile.is_admin_role))

    def handle_no_permission(self):
        messages.error(self.request, "Anda tidak memiliki akses untuk mengelola data ini.")
        from django.shortcuts import redirect
        return redirect('analitik:dashboard')


class BaseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    paginate_by = 15
    template_name = 'crud/list.html'
    title = ''
    columns = []       # list of header string
    row_builder = None  # function(obj) -> list of cell string
    create_url_name = ''
    edit_url_name = ''
    delete_url_name = ''
    icon = 'bi-table'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        rows = []
        for obj in ctx['object_list']:
            rows.append({
                'pk': obj.pk,
                'cells': self.row_builder(obj) if self.row_builder else [str(obj)],
            })
        ctx.update({
            'title': self.title,
            'columns': self.columns,
            'rows': rows,
            'create_url_name': self.create_url_name,
            'edit_url_name': self.edit_url_name,
            'delete_url_name': self.delete_url_name,
            'icon': self.icon,
        })
        return ctx


class BaseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = 'crud/form.html'
    title = ''
    icon = 'bi-plus-circle'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tambah {self.title}"
        ctx['icon'] = self.icon
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"{self.title} berhasil ditambahkan.")
        return super().form_valid(form)


class BaseUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = 'crud/form.html'
    title = ''
    icon = 'bi-pencil-square'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Ubah {self.title}"
        ctx['icon'] = self.icon
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"{self.title} berhasil diperbarui.")
        return super().form_valid(form)


class BaseDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    template_name = 'crud/confirm_delete.html'
    title = ''

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"{self.title} berhasil dihapus.")
        return super().form_valid(form)

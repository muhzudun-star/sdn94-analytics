from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginTerpaduForm, RegisterUserForm


class LoginTerpaduView(LoginView):
    """Satu halaman login untuk Admin dan User.

    Setelah autentikasi berhasil, sistem membaca role dari Profile pengguna
    lalu mengarahkan ke dashboard yang sesuai (admin -> dashboard lengkap,
    user -> dashboard analisis saja / read-only).
    """
    template_name = 'accounts/login.html'
    authentication_form = LoginTerpaduForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Selamat datang, {self.request.user.get_full_name() or self.request.user.username}!")
        return response

    def get_success_url(self):
        user = self.request.user
        profile = getattr(user, 'profile', None)
        if user.is_superuser or (profile and profile.is_admin_role):
            return reverse_lazy('analitik:dashboard_admin')
        return reverse_lazy('analitik:dashboard_user')


class RegisterUserView(CreateView):
    """Pendaftaran akun mandiri untuk role Pengguna (Guru/Wali Kelas).

    Setelah berhasil daftar, user langsung login otomatis dan diarahkan
    ke dashboard user (bukan dashboard admin).
    """
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('analitik:dashboard_user')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('analitik:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        messages.success(self.request, f"Akun berhasil dibuat. Selamat datang, {self.object.first_name or self.object.username}!")
        return response


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Anda telah keluar dari sistem.")
    return redirect('accounts:login')

import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .services import bangun_analisis_lengkap


def _is_admin(user):
    profile = getattr(user, 'profile', None)
    return bool(user.is_superuser or (profile and profile.is_admin_role))


@login_required
def dashboard_redirect(request):
    """Titik masuk /analitik/ -> arahkan ke dashboard sesuai role."""
    if _is_admin(request.user):
        return redirect('analitik:dashboard_admin')
    return redirect('analitik:dashboard_user')


class DashboardAdminView(LoginRequiredMixin, TemplateView):
    template_name = 'analitik/dashboard_admin.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not _is_admin(request.user):
            return redirect('analitik:dashboard_user')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        analisis = bangun_analisis_lengkap()
        ctx['analisis'] = analisis
        ctx['analisis_json'] = json.dumps(analisis)
        return ctx


class DashboardUserView(LoginRequiredMixin, TemplateView):
    """Dashboard read-only untuk Guru/Wali Kelas: hanya menampilkan analisis,
    tanpa akses ke menu pengelolaan data master."""
    template_name = 'analitik/dashboard_user.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        analisis = bangun_analisis_lengkap()
        ctx['analisis'] = analisis
        ctx['analisis_json'] = json.dumps(analisis)
        return ctx

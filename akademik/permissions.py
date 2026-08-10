from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsInternalOrAuthenticated(BasePermission):
    """
    Mengizinkan akses API jika:
    - request membawa header X-API-KEY yang valid (dipakai oleh modul analitik
      untuk menarik data lewat pandas dari dalam server sendiri), ATAU
    - user sudah login (session) untuk operasi CRUD lewat dashboard/DRF browsable API.

    Untuk method aman (GET/HEAD/OPTIONS) yang membawa API key internal, akses
    langsung diizinkan tanpa login, karena ini adalah komunikasi
    server-ke-server (Django -> API -> Pandas), bukan akses publik.
    """

    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY') or request.META.get('HTTP_X_API_KEY')
        if api_key and api_key == settings.INTERNAL_API_KEY:
            return True
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            # operasi tulis (POST/PUT/PATCH/DELETE) lewat API hanya untuk admin
            profile = getattr(request.user, 'profile', None)
            return bool(request.user.is_superuser or (profile and profile.is_admin_role))
        return False

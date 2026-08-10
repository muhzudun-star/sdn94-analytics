from django.conf import settings


def role_context(request):
    """Menyediakan variabel role & nama sekolah ke semua template."""
    is_admin = False
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        is_admin = request.user.is_superuser or (profile and profile.is_admin_role)
    return {
        'IS_ADMIN_ROLE': is_admin,
        'NAMA_SEKOLAH': getattr(settings, 'NAMA_SEKOLAH', 'SDN 94 Buton'),
        'user_profile': profile,
    }

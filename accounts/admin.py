from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil (Role)'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'get_role')

    def get_role(self, obj):
        return getattr(obj.profile, 'get_role_display', lambda: '-')()
    get_role.short_description = 'Role'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

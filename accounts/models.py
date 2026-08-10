from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_ADMIN = 'ADMIN'
    ROLE_USER = 'USER'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin (Operator Sekolah)'),
        (ROLE_USER, 'Pengguna (Guru / Wali Kelas)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    jabatan = models.CharField(max_length=100, blank=True, default='')
    no_hp = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        verbose_name = 'Profil Pengguna'
        verbose_name_plural = 'Profil Pengguna'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN or self.user.is_superuser


@receiver(post_save, sender=User)
def buat_atau_simpan_profile(sender, instance, created, **kwargs):
    """Otomatis membuat Profile saat User baru dibuat (mis. lewat createsuperuser)."""
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={'role': Profile.ROLE_ADMIN if instance.is_superuser else Profile.ROLE_USER}
        )
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

from django.db import models


class Guru(models.Model):
    JK_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]

    nip = models.CharField('NIP', max_length=25, unique=True)
    nama = models.CharField('Nama Lengkap', max_length=150)
    jenis_kelamin = models.CharField('Jenis Kelamin', max_length=1, choices=JK_CHOICES)
    no_hp = models.CharField('No. HP', max_length=20, blank=True, default='')
    alamat = models.CharField('Alamat', max_length=255, blank=True, default='')
    tanggal_bergabung = models.DateField('Tanggal Bergabung', null=True, blank=True)

    class Meta:
        verbose_name = 'Guru'
        verbose_name_plural = 'Guru'
        ordering = ['nama']

    def __str__(self):
        return self.nama

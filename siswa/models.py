from django.db import models


class Siswa(models.Model):
    JK_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    STATUS_CHOICES = [('AKTIF', 'Aktif'), ('LULUS', 'Lulus'), ('PINDAH', 'Pindah')]

    nis = models.CharField('NIS', max_length=20, unique=True)
    nisn = models.CharField('NISN', max_length=20, unique=True)
    nama = models.CharField('Nama Lengkap', max_length=150)
    jenis_kelamin = models.CharField('Jenis Kelamin', max_length=1, choices=JK_CHOICES)
    tempat_lahir = models.CharField('Tempat Lahir', max_length=100, blank=True, default='')
    tanggal_lahir = models.DateField('Tanggal Lahir', null=True, blank=True)
    alamat = models.CharField('Alamat', max_length=255, blank=True, default='')
    nama_ortu = models.CharField('Nama Orang Tua/Wali', max_length=150, blank=True, default='')
    kelas = models.ForeignKey(
        'akademik.Kelas', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='siswa', verbose_name='Kelas'
    )
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='AKTIF')

    class Meta:
        verbose_name = 'Siswa'
        verbose_name_plural = 'Siswa'
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.nis})"

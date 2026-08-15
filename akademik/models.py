from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Kelas(models.Model):
    nama_kelas = models.CharField('Nama Kelas', max_length=20)  # contoh: 1A, 4B
    tingkat = models.PositiveSmallIntegerField('Tingkat', validators=[MinValueValidator(1), MaxValueValidator(6)])
    tahun_ajaran = models.CharField('Tahun Ajaran', max_length=15, default='2025/2026')
    wali_kelas = models.ForeignKey(
        'kepegawaian.Guru', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='kelas_diampu', verbose_name='Wali Kelas'
    )

    class Meta:
        verbose_name = 'Kelas'
        verbose_name_plural = 'Kelas'
        ordering = ['tingkat', 'nama_kelas']
        unique_together = ('nama_kelas', 'tahun_ajaran')

    def __str__(self):
        return f"{self.nama_kelas} ({self.tahun_ajaran})"


class MataPelajaran(models.Model):
    kode_mapel = models.CharField('Kode', max_length=10, unique=True)
    nama_mapel = models.CharField('Nama Mata Pelajaran', max_length=100)
    kkm = models.PositiveSmallIntegerField('KKM', default=70)

    class Meta:
        verbose_name = 'Mata Pelajaran'
        verbose_name_plural = 'Mata Pelajaran'
        ordering = ['nama_mapel']

    def __str__(self):
        return self.nama_mapel

from django.db import models


class Nilai(models.Model):
    JENIS_CHOICES = [
        ('HARIAN', 'Ulangan Harian'),
        ('UTS', 'Ujian Tengah Semester'),
        ('UAS', 'Ujian Akhir Semester'),
        ('TUGAS', 'Tugas'),
    ]
    SEMESTER_CHOICES = [('GANJIL', 'Ganjil'), ('GENAP', 'Genap')]

    siswa = models.ForeignKey('siswa.Siswa', on_delete=models.CASCADE, related_name='nilai', verbose_name='Siswa')
    mapel = models.ForeignKey('akademik.MataPelajaran', on_delete=models.CASCADE, related_name='nilai', verbose_name='Mata Pelajaran')
    jenis_nilai = models.CharField('Jenis Nilai', max_length=10, choices=JENIS_CHOICES, default='HARIAN')
    nilai = models.DecimalField('Nilai', max_digits=5, decimal_places=2)
    semester = models.CharField('Semester', max_length=10, choices=SEMESTER_CHOICES, default='GANJIL')
    tahun_ajaran = models.CharField('Tahun Ajaran', max_length=15, default='2025/2026')
    tanggal_input = models.DateField('Tanggal Input', auto_now_add=True)

    class Meta:
        verbose_name = 'Nilai'
        verbose_name_plural = 'Nilai'
        ordering = ['-tanggal_input']

    def __str__(self):
        return f"{self.siswa.nama} - {self.mapel.nama_mapel}: {self.nilai}"


class Kehadiran(models.Model):
    STATUS_CHOICES = [
        ('HADIR', 'Hadir'),
        ('SAKIT', 'Sakit'),
        ('IZIN', 'Izin'),
        ('ALPA', 'Alpa/Tanpa Keterangan'),
    ]

    siswa = models.ForeignKey('siswa.Siswa', on_delete=models.CASCADE, related_name='kehadiran', verbose_name='Siswa')
    tanggal = models.DateField('Tanggal')
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='HADIR')
    keterangan = models.CharField('Keterangan', max_length=255, blank=True, default='')

    class Meta:
        verbose_name = 'Kehadiran'
        verbose_name_plural = 'Kehadiran'
        ordering = ['-tanggal']
        unique_together = ('siswa', 'tanggal')

    def __str__(self):
        return f"{self.siswa.nama} - {self.tanggal} ({self.get_status_display()})"


class Prestasi(models.Model):
    TINGKAT_CHOICES = [
        ('SEKOLAH', 'Sekolah'),
        ('KECAMATAN', 'Kecamatan'),
        ('KABUPATEN', 'Kabupaten/Kota'),
        ('PROVINSI', 'Provinsi'),
        ('NASIONAL', 'Nasional'),
    ]

    siswa = models.ForeignKey('siswa.Siswa', on_delete=models.CASCADE, related_name='prestasi', verbose_name='Siswa')
    nama_prestasi = models.CharField('Nama Prestasi/Lomba', max_length=200)
    tingkat = models.CharField('Tingkat', max_length=15, choices=TINGKAT_CHOICES, default='SEKOLAH')
    tahun = models.PositiveIntegerField('Tahun')
    keterangan = models.CharField('Keterangan', max_length=255, blank=True, default='')

    class Meta:
        verbose_name = 'Prestasi'
        verbose_name_plural = 'Prestasi'
        ordering = ['-tahun']

    def __str__(self):
        return f"{self.siswa.nama} - {self.nama_prestasi} ({self.tahun})"

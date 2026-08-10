from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Kelas(models.Model):
    nama_kelas = models.CharField('Nama Kelas', max_length=20)  # contoh: 1A, 4B
    tingkat = models.PositiveSmallIntegerField('Tingkat', validators=[MinValueValidator(1), MaxValueValidator(6)])
    tahun_ajaran = models.CharField('Tahun Ajaran', max_length=15, default='2025/2026')
    wali_kelas = models.ForeignKey(
        Guru, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='kelas_diampu', verbose_name='Wali Kelas'
    )

    class Meta:
        verbose_name = 'Kelas'
        verbose_name_plural = 'Kelas'
        ordering = ['tingkat', 'nama_kelas']
        unique_together = ('nama_kelas', 'tahun_ajaran')

    def __str__(self):
        return f"{self.nama_kelas} ({self.tahun_ajaran})"


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
        Kelas, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='siswa', verbose_name='Kelas'
    )
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='AKTIF')

    class Meta:
        verbose_name = 'Siswa'
        verbose_name_plural = 'Siswa'
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.nis})"


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


class Nilai(models.Model):
    JENIS_CHOICES = [
        ('HARIAN', 'Ulangan Harian'),
        ('UTS', 'Ujian Tengah Semester'),
        ('UAS', 'Ujian Akhir Semester'),
        ('TUGAS', 'Tugas'),
    ]
    SEMESTER_CHOICES = [('GANJIL', 'Ganjil'), ('GENAP', 'Genap')]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='nilai', verbose_name='Siswa')
    mapel = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='nilai', verbose_name='Mata Pelajaran')
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

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='kehadiran', verbose_name='Siswa')
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

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='prestasi', verbose_name='Siswa')
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

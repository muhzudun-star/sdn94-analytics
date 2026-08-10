"""
Perintah untuk mengisi data contoh (dummy) yang realistis untuk
SDN 94 Buton, mencakup 7 tabel yang saling terintegrasi:
Guru, Kelas, Siswa, Mata Pelajaran, Nilai, Kehadiran, dan Prestasi.

Jalankan dengan:
    python manage.py seed_data
"""
import random
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from accounts.models import Profile
from akademik.models import Guru, Kelas, Siswa, MataPelajaran, Nilai, Kehadiran, Prestasi

random.seed(94)

NAMA_DEPAN_L = [
    "Muhammad", "Ahmad", "Rizky", "Fajar", "Andi", "La Ode", "Wa Ode", "Aditya", "Bagas",
    "Dimas", "Rafi", "Farhan", "Gilang", "Ilham", "Yusuf", "Zaki", "Reza", "Arif", "Dedi", "Doni"
]
NAMA_DEPAN_P = [
    "Siti", "Nur", "Putri", "Ayu", "Wa Ode", "Fitri", "Dewi", "Indah", "Rani", "Salsa",
    "Aulia", "Bunga", "Citra", "Dinda", "Intan", "Kirana", "Melati", "Nabila", "Sari", "Yuni"
]
NAMA_BELAKANG = [
    "Saputra", "Pratama", "Ramadhan", "Setiawan", "Wijaya", "Kusuma", "Nugraha",
    "Firmansyah", "Gunawan", "Haryanto", "Iskandar", "Jamaluddin", "Kadir", "Laoli",
    "Mansur", "Nurdin", "Oktavianus", "Pratiwi", "Rahman", "Syarif", "Tamrin", "Usman"
]
NAMA_GURU_L = ["Sardin", "Basri", "La Ode Arman", "Muslimin", "Sahrul", "Amiruddin", "Wayan Sudira", "Herman", "Sudirman"]
NAMA_GURU_P = ["Hasnawati", "Wa Ode Ratna", "Nurhayati", "Marlina", "Suryani", "Ramlah", "Yuliana", "Asnah", "Nirmala"]
ALAMAT_LINGKUNGAN = [
    "Kelurahan Wameo", "Kelurahan Baruga", "Kelurahan Wolio", "Kelurahan Kadolokatapi",
    "Kelurahan Bone-Bone", "Kelurahan Lipu", "Desa Waangu-angu", "Kelurahan Melai"
]
NAMA_PRESTASI = [
    ("Juara 1 Lomba Cerdas Cermat", "KECAMATAN"),
    ("Juara 2 Olimpiade Matematika", "KABUPATEN"),
    ("Juara 1 Lomba Menggambar", "SEKOLAH"),
    ("Juara 3 Lomba Pidato Bahasa Indonesia", "KABUPATEN"),
    ("Juara 1 Festival Tari Daerah", "PROVINSI"),
    ("Juara 2 Lomba Sains SD", "PROVINSI"),
    ("Juara 1 Lomba Menyanyi Solo", "SEKOLAH"),
    ("Juara Harapan 1 O2SN Renang", "KABUPATEN"),
    ("Juara 1 Lomba Tahfidz", "KECAMATAN"),
    ("Juara 1 O2SN Catur", "NASIONAL"),
    ("Juara 2 Lomba Mewarnai", "SEKOLAH"),
    ("Juara 1 FLS2N Menulis Cerpen", "PROVINSI"),
]


def nama_acak(jk):
    depan = random.choice(NAMA_DEPAN_L if jk == 'L' else NAMA_DEPAN_P)
    belakang = random.choice(NAMA_BELAKANG)
    return f"{depan} {belakang}"


class Command(BaseCommand):
    help = "Mengisi data contoh (siswa, guru, kelas, nilai, kehadiran, prestasi) untuk SDN 94 Buton"

    def add_arguments(self, parser):
        parser.add_argument('--siswa-per-kelas', type=int, default=18)
        parser.add_argument('--hari-kehadiran', type=int, default=30)
        parser.add_argument('--reset', action='store_true', help="Hapus semua data lama sebelum mengisi ulang")

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write("Menghapus data lama...")
            Prestasi.objects.all().delete()
            Kehadiran.objects.all().delete()
            Nilai.objects.all().delete()
            Siswa.objects.all().delete()
            Kelas.objects.all().delete()
            MataPelajaran.objects.all().delete()
            Guru.objects.all().delete()

        self.stdout.write(self.style.MIGRATE_HEADING("1) Membuat akun login (Admin & Guru)..."))
        self._buat_akun()

        self.stdout.write(self.style.MIGRATE_HEADING("2) Membuat data Guru..."))
        daftar_guru = self._buat_guru()

        self.stdout.write(self.style.MIGRATE_HEADING("3) Membuat data Kelas..."))
        daftar_kelas = self._buat_kelas(daftar_guru)

        self.stdout.write(self.style.MIGRATE_HEADING("4) Membuat Mata Pelajaran..."))
        daftar_mapel = self._buat_mapel()

        self.stdout.write(self.style.MIGRATE_HEADING("5) Membuat data Siswa..."))
        daftar_siswa = self._buat_siswa(daftar_kelas, options['siswa_per_kelas'])

        self.stdout.write(self.style.MIGRATE_HEADING("6) Membuat data Nilai..."))
        self._buat_nilai(daftar_siswa, daftar_mapel)

        self.stdout.write(self.style.MIGRATE_HEADING("7) Membuat data Kehadiran..."))
        self._buat_kehadiran(daftar_siswa, options['hari_kehadiran'])

        self.stdout.write(self.style.MIGRATE_HEADING("8) Membuat data Prestasi..."))
        self._buat_prestasi(daftar_siswa)

        self.stdout.write(self.style.SUCCESS(
            f"\nSelesai! {len(daftar_siswa)} siswa, {len(daftar_kelas)} kelas, "
            f"{len(daftar_guru)} guru, {len(daftar_mapel)} mata pelajaran berhasil dibuat.\n"
            "Login dengan:\n"
            "  Admin -> username: admin  | password: admin12345\n"
            "  Guru  -> username: guru   | password: guru12345\n"
        ))

    # ------------------------------------------------------------------
    def _buat_akun(self):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@sdn94buton.sch.id', 'admin12345')
            admin.first_name = 'Admin'
            admin.last_name = 'Operator'
            admin.save()
            Profile.objects.filter(user=admin).update(role=Profile.ROLE_ADMIN, jabatan='Operator Sekolah')
        else:
            self.stdout.write("  User 'admin' sudah ada, dilewati.")

        if not User.objects.filter(username='guru').exists():
            guru_user = User.objects.create_user('guru', 'guru@sdn94buton.sch.id', 'guru12345')
            guru_user.first_name = 'Hasnawati'
            guru_user.last_name = 'Wali Kelas'
            guru_user.save()
            Profile.objects.filter(user=guru_user).update(role=Profile.ROLE_USER, jabatan='Wali Kelas')
        else:
            self.stdout.write("  User 'guru' sudah ada, dilewati.")

    def _buat_guru(self):
        if Guru.objects.exists():
            return list(Guru.objects.all())
        daftar = []
        for i, nama in enumerate(NAMA_GURU_L + NAMA_GURU_P, start=1):
            jk = 'L' if nama in NAMA_GURU_L else 'P'
            daftar.append(Guru(
                nip=f"19800{i:03d}20250{i:02d}1001",
                nama=nama,
                jenis_kelamin=jk,
                no_hp=f"08{random.randint(10000000,99999999)}",
                alamat=random.choice(ALAMAT_LINGKUNGAN) + ", Kota Baubau",
                tanggal_bergabung=datetime.date(2015 + i % 8, random.randint(1, 12), random.randint(1, 28)),
            ))
        Guru.objects.bulk_create(daftar)
        return list(Guru.objects.all())

    def _buat_kelas(self, daftar_guru):
        if Kelas.objects.exists():
            return list(Kelas.objects.select_related('wali_kelas').all())
        daftar = []
        guru_idx = 0
        for tingkat in range(1, 7):
            for rombel in ['A', 'B']:
                wali = daftar_guru[guru_idx % len(daftar_guru)]
                guru_idx += 1
                daftar.append(Kelas(
                    nama_kelas=f"{tingkat}{rombel}",
                    tingkat=tingkat,
                    tahun_ajaran="2025/2026",
                    wali_kelas=wali,
                ))
        Kelas.objects.bulk_create(daftar)
        return list(Kelas.objects.select_related('wali_kelas').all())

    def _buat_mapel(self):
        if MataPelajaran.objects.exists():
            return list(MataPelajaran.objects.all())
        data = [
            ("PAI", "Pendidikan Agama & Budi Pekerti", 70),
            ("PPKN", "Pendidikan Pancasila", 70),
            ("BINA", "Bahasa Indonesia", 70),
            ("MTK", "Matematika", 65),
            ("IPAS", "Ilmu Pengetahuan Alam & Sosial", 70),
            ("SBDP", "Seni Budaya & Prakarya", 75),
            ("PJOK", "Pendidikan Jasmani, Olahraga & Kesehatan", 75),
            ("BING", "Bahasa Inggris", 70),
        ]
        daftar = [MataPelajaran(kode_mapel=k, nama_mapel=n, kkm=kkm) for k, n, kkm in data]
        MataPelajaran.objects.bulk_create(daftar)
        return list(MataPelajaran.objects.all())

    def _buat_siswa(self, daftar_kelas, jumlah_per_kelas):
        if Siswa.objects.exists():
            return list(Siswa.objects.select_related('kelas').all())
        daftar = []
        nis_counter = 2210001
        for kelas in daftar_kelas:
            for _ in range(jumlah_per_kelas):
                jk = random.choice(['L', 'P'])
                tahun_lahir = 2026 - (kelas.tingkat + 6)  # perkiraan usia sesuai tingkat SD
                daftar.append(Siswa(
                    nis=str(nis_counter),
                    nisn=f"00{nis_counter}",
                    nama=nama_acak(jk),
                    jenis_kelamin=jk,
                    tempat_lahir="Baubau",
                    tanggal_lahir=datetime.date(tahun_lahir, random.randint(1, 12), random.randint(1, 28)),
                    alamat=random.choice(ALAMAT_LINGKUNGAN) + ", Kota Baubau",
                    nama_ortu=nama_acak(random.choice(['L', 'P'])),
                    kelas=kelas,
                    status='AKTIF',
                ))
                nis_counter += 1
        Siswa.objects.bulk_create(daftar)
        return list(Siswa.objects.select_related('kelas').all())

    def _buat_nilai(self, daftar_siswa, daftar_mapel):
        if Nilai.objects.exists():
            return
        periode_list = [("2024/2025", "GENAP"), ("2025/2026", "GANJIL")]
        batch = []
        for siswa in daftar_siswa:
            for mapel in daftar_mapel:
                for tahun_ajaran, semester in periode_list:
                    # distribusi nilai realistis: sebagian besar baik, sebagian kecil di bawah KKM
                    dasar = random.gauss(82, 9)
                    nilai_akhir = max(35, min(100, round(dasar, 1)))
                    for jenis in ['UTS', 'UAS']:
                        variasi = random.uniform(-4, 4)
                        nilai_final = max(30, min(100, round(nilai_akhir + variasi, 1)))
                        batch.append(Nilai(
                            siswa=siswa, mapel=mapel, jenis_nilai=jenis,
                            nilai=nilai_final, semester=semester, tahun_ajaran=tahun_ajaran,
                        ))
            if len(batch) >= 4000:
                Nilai.objects.bulk_create(batch)
                batch = []
        if batch:
            Nilai.objects.bulk_create(batch)

    def _buat_kehadiran(self, daftar_siswa, jumlah_hari):
        if Kehadiran.objects.exists():
            return
        hari_ini = datetime.date.today()
        tanggal_list = []
        d = hari_ini
        while len(tanggal_list) < jumlah_hari:
            d -= datetime.timedelta(days=1)
            if d.weekday() < 5:  # senin-jumat saja
                tanggal_list.append(d)

        batch = []
        for siswa in daftar_siswa:
            for tanggal in tanggal_list:
                r = random.random()
                if r < 0.88:
                    status = 'HADIR'
                elif r < 0.94:
                    status = 'SAKIT'
                elif r < 0.98:
                    status = 'IZIN'
                else:
                    status = 'ALPA'
                batch.append(Kehadiran(siswa=siswa, tanggal=tanggal, status=status))
            if len(batch) >= 4000:
                Kehadiran.objects.bulk_create(batch)
                batch = []
        if batch:
            Kehadiran.objects.bulk_create(batch)

    def _buat_prestasi(self, daftar_siswa):
        if Prestasi.objects.exists():
            return
        jumlah_prestasi = max(30, len(daftar_siswa) // 6)
        siswa_terpilih = random.sample(daftar_siswa, min(jumlah_prestasi, len(daftar_siswa)))
        batch = []
        for siswa in siswa_terpilih:
            nama_prestasi, tingkat = random.choice(NAMA_PRESTASI)
            batch.append(Prestasi(
                siswa=siswa,
                nama_prestasi=nama_prestasi,
                tingkat=tingkat,
                tahun=random.choice([2024, 2025, 2026]),
                keterangan="Diselenggarakan oleh Dinas Pendidikan setempat.",
            ))
        Prestasi.objects.bulk_create(batch)

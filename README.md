# Sistem Analisis Data Siswa — SDN 94 Buton

Proyek **UTS/UAS Big Data** berbasis **Django**: sistem informasi & analisis data
siswa dengan basis data yang saling terintegrasi (7 tabel), diakses melalui
**REST API internal**, lalu dianalisis menggunakan **Pandas**, dan ditampilkan
lewat **dashboard interaktif** (bukan sekadar output analisis biasa).

## Arsitektur

```
┌─────────────────────┐     ┌──────────────────────┐     ┌───────────────────────┐     ┌─────────────────────────┐
│  Database (SQLite)  │ --> │  REST API (Django    │ --> │  Modul Analisis        │ --> │  Dashboard Interaktif    │
│  7 tabel terintegrasi│     │  REST Framework)     │     │  (requests + Pandas)   │     │  (Bootstrap + Chart.js)  │
│  Guru, Kelas, Siswa, │     │  /api/siswa/         │     │  groupby, mean, rank,  │     │  Grafik, tabel, kartu    │
│  MataPelajaran,      │     │  /api/nilai/ dst.     │     │  distribusi, dsb.      │     │  statistik               │
│  Nilai, Kehadiran,   │     │                      │     │                        │     │                          │
│  Prestasi            │     │                      │     │                        │     │                          │
└─────────────────────┘     └──────────────────────┘     └───────────────────────┘     └─────────────────────────┘
```

Poin penting: modul analisis (`analitik/services.py`) **tidak** melakukan query
ORM langsung ke database untuk perhitungan statistik. Semua data ditarik lewat
endpoint REST API (`/api/...`) menggunakan `requests`, baru kemudian diproses
dengan `pandas` (groupby, mean, ranking, distribusi, dsb).

## Fitur

- **7 tabel terintegrasi**: Guru, Kelas, Siswa, Mata Pelajaran, Nilai, Kehadiran, Prestasi (berelasi lewat ForeignKey).
- **REST API** lengkap (Django REST Framework) untuk seluruh tabel — CRUD via API.
- **Analisis data dengan Pandas**: rata-rata nilai per kelas/mapel/semester, ranking siswa terbaik, siswa di bawah KKM, persentase kehadiran, distribusi status kehadiran, siswa kehadiran rendah, prestasi per tingkat, dsb.
- **Dashboard interaktif** dengan grafik (Chart.js): bar chart, doughnut chart, line chart, serta tabel ranking.
- **Login terpadu (satu pintu)** untuk Admin dan User (Guru/Wali Kelas) — role ditentukan otomatis setelah login.
  - **Admin**: akses penuh dashboard analisis + kelola seluruh data master (CRUD Siswa, Guru, Kelas, Mapel, Nilai, Kehadiran, Prestasi).
  - **User (Guru/Wali Kelas)**: dashboard analisis read-only saja.
- **Data contoh siap pakai** (seed data) yang realistis untuk SDN 94 Buton (± 200+ siswa, ratusan nilai & data kehadiran).
- Tampilan modern & rapi (Bootstrap 5 + Chart.js + desain custom).

## Struktur Proyek

```
sdn94_analytics/
├── config/            # Pengaturan proyek Django (settings, urls)
├── accounts/          # Login terpadu (Admin & User) + Profile/role
├── akademik/          # Model 7 tabel, API (DRF), CRUD dashboard admin
├── analitik/          # Modul analisis Pandas + dashboard admin & user
├── templates/         # Template dasar (base.html, sidebar)
├── static/            # CSS kustom
├── manage.py
└── requirements.txt
```

## Cara Menjalankan

### 1. Buat & aktifkan virtual environment (disarankan)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Migrasi database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Isi data contoh (seed data)
Perintah ini akan otomatis membuat 2 akun login (admin & guru) sekaligus
data Guru, Kelas, Siswa, Mata Pelajaran, Nilai, Kehadiran, dan Prestasi:
```bash
python manage.py seed_data
```
Opsi tambahan:
```bash
python manage.py seed_data --siswa-per-kelas 20 --hari-kehadiran 40
python manage.py seed_data --reset   # hapus data lama lalu isi ulang
```

### 5. Jalankan server
```bash
python manage.py runserver
```
Buka browser ke: **http://127.0.0.1:8000/**

### 6. Login
Sistem menggunakan **satu halaman login** untuk Admin maupun User:

| Peran | Username | Password           |
|-------|----------|---------------------|
| Admin | `admin`  | `admin12345`        |
| Guru / Wali Kelas (User) | `guru` | `guru12345` |

> Setelah login, sistem otomatis mengarahkan ke dashboard sesuai peran.
> Admin bisa membuat akun tambahan lewat Django Admin (`/django-admin/`) dan
> mengatur *role* pengguna pada bagian **Profil (Role)**.

## Endpoint API (contoh)

| Endpoint            | Keterangan                     |
|----------------------|---------------------------------|
| `GET /api/siswa/`    | Daftar seluruh siswa            |
| `GET /api/guru/`     | Daftar seluruh guru             |
| `GET /api/kelas/`    | Daftar seluruh kelas            |
| `GET /api/mapel/`    | Daftar mata pelajaran           |
| `GET /api/nilai/`    | Daftar nilai siswa              |
| `GET /api/kehadiran/`| Daftar kehadiran siswa          |
| `GET /api/prestasi/` | Daftar prestasi siswa           |

API dapat diakses dengan login session (lewat dashboard/browsable API DRF),
atau lewat header `X-API-KEY` (dipakai secara internal oleh modul analisis
Pandas — lihat `config/settings.py` -> `INTERNAL_API_KEY`).

## Catatan Pengembangan Lanjutan

- Untuk produksi, ganti `DEBUG = False`, atur `ALLOWED_HOSTS`, ganti `SECRET_KEY`
  dan `INTERNAL_API_KEY` lewat environment variable, serta gunakan database
  seperti PostgreSQL/MySQL (tinggal ganti `DATABASES` di `config/settings.py`).
- Tambahan tabel/analisis baru cukup: (1) tambah model di `akademik/models.py`,
  (2) daftarkan di `akademik/serializers.py` & `akademik/api_views.py`,
  (3) tambahkan fungsi analisis baru di `analitik/services.py`.

---
*Dibuat untuk keperluan tugas Big Data — Pengembangan Analisis Data Siswa Sekolah Dasar SDN 94 Buton.*

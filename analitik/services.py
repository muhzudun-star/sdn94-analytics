"""
Modul Analisis Data (Big Data Project - SDN 94 Buton)
======================================================
Seluruh proses analisis di sini TIDAK mengakses database Django secara
langsung (tidak memakai ORM query untuk perhitungan). Sebagai gantinya,
data ditarik melalui REST API internal (`akademik.api_urls`) menggunakan
library `requests`, kemudian diolah sepenuhnya dengan `pandas`.

Alur:
    Database (7 tabel) -> REST API (Django REST Framework)
        -> requests.get() -> pandas.DataFrame -> Analisis & Statistik
"""
import logging
import requests
import pandas as pd
from django.conf import settings

logger = logging.getLogger(__name__)


def _headers():
    return {'X-API-KEY': settings.INTERNAL_API_KEY}


def ambil_dataframe(endpoint: str) -> pd.DataFrame:
    """Menarik data dari endpoint API internal dan mengubahnya menjadi DataFrame."""
    url = f"{settings.API_BASE_URL}/api/{endpoint}/"
    try:
        resp = requests.get(url, headers=_headers(), timeout=8)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and 'results' in data:
            data = data['results']
        return pd.DataFrame(data)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Gagal mengambil data dari API %s: %s", url, exc)
        return pd.DataFrame()


def _safe_round(value, digits=1):
    try:
        if pd.isna(value):
            return 0
        return round(float(value), digits)
    except (TypeError, ValueError):
        return 0


def bangun_analisis_lengkap() -> dict:
    """Mengambil seluruh tabel via API lalu menghasilkan satu paket analisis
    siap-pakai untuk ditampilkan di dashboard (admin maupun user)."""

    df_siswa = ambil_dataframe('siswa')
    df_guru = ambil_dataframe('guru')
    df_kelas = ambil_dataframe('kelas')
    df_mapel = ambil_dataframe('mapel')
    df_nilai = ambil_dataframe('nilai')
    df_kehadiran = ambil_dataframe('kehadiran')
    df_prestasi = ambil_dataframe('prestasi')

    hasil = {
        'ringkasan': _analisis_ringkasan(df_siswa, df_guru, df_kelas, df_mapel),
        'nilai': _analisis_nilai(df_nilai),
        'kehadiran': _analisis_kehadiran(df_kehadiran),
        'prestasi': _analisis_prestasi(df_prestasi),
        'siswa_per_kelas': _siswa_per_kelas(df_siswa),
    }
    return hasil


def _analisis_ringkasan(df_siswa, df_guru, df_kelas, df_mapel):
    total_siswa = len(df_siswa)
    laki = perempuan = 0
    if not df_siswa.empty and 'jenis_kelamin' in df_siswa.columns:
        laki = int((df_siswa['jenis_kelamin'] == 'L').sum())
        perempuan = int((df_siswa['jenis_kelamin'] == 'P').sum())

    return {
        'total_siswa': total_siswa,
        'total_guru': len(df_guru),
        'total_kelas': len(df_kelas),
        'total_mapel': len(df_mapel),
        'siswa_laki': laki,
        'siswa_perempuan': perempuan,
    }


def _analisis_nilai(df_nilai: pd.DataFrame) -> dict:
    kosong = {
        'rata_rata_keseluruhan': 0,
        'per_kelas_labels': [], 'per_kelas_values': [],
        'per_mapel_labels': [], 'per_mapel_values': [],
        'per_semester_labels': [], 'per_semester_values': [],
        'top_siswa': [], 'perlu_perhatian': [],
    }
    if df_nilai.empty:
        return kosong

    df = df_nilai.copy()
    df['nilai'] = pd.to_numeric(df['nilai'], errors='coerce')
    df = df.dropna(subset=['nilai'])
    if df.empty:
        return kosong

    rata_rata_keseluruhan = _safe_round(df['nilai'].mean())

    # Rata-rata per kelas
    per_kelas = pd.Series(dtype=float)
    if 'kelas_nama' in df.columns:
        per_kelas = df.groupby('kelas_nama')['nilai'].mean().sort_values(ascending=False)

    # Rata-rata per mapel
    per_mapel = pd.Series(dtype=float)
    if 'mapel_nama' in df.columns:
        per_mapel = df.groupby('mapel_nama')['nilai'].mean().sort_values(ascending=False)

    # Rata-rata per semester (tren)
    per_semester = pd.Series(dtype=float)
    if 'semester' in df.columns and 'tahun_ajaran' in df.columns:
        df['periode'] = df['tahun_ajaran'].astype(str) + ' - ' + df['semester'].astype(str)
        per_semester = df.groupby('periode')['nilai'].mean().sort_index()

    # Ranking siswa terbaik (rata-rata nilai per siswa)
    top_siswa = []
    perlu_perhatian = []
    if 'siswa_nama' in df.columns:
        rata_per_siswa = df.groupby('siswa_nama').agg(
            rata_rata=('nilai', 'mean'),
            kelas=('kelas_nama', 'first') if 'kelas_nama' in df.columns else ('nilai', 'count'),
        ).reset_index()
        rata_per_siswa['rata_rata'] = rata_per_siswa['rata_rata'].round(1)

        top_siswa = (
            rata_per_siswa.sort_values('rata_rata', ascending=False)
            .head(10)
            .to_dict('records')
        )

        # Siswa dengan nilai di bawah KKM (perlu perhatian khusus)
        if 'kkm' in df.columns:
            df_kkm = df.copy()
            df_kkm['kkm'] = pd.to_numeric(df_kkm['kkm'], errors='coerce').fillna(70)
            df_dibawah = df_kkm[df_kkm['nilai'] < df_kkm['kkm']]
            if not df_dibawah.empty:
                agg = df_dibawah.groupby('siswa_nama').agg(
                    jumlah_dibawah_kkm=('nilai', 'count'),
                    rata_rata=('nilai', 'mean'),
                ).reset_index()
                agg['rata_rata'] = agg['rata_rata'].round(1)
                perlu_perhatian = (
                    agg.sort_values('jumlah_dibawah_kkm', ascending=False)
                    .head(10)
                    .to_dict('records')
                )

    return {
        'rata_rata_keseluruhan': rata_rata_keseluruhan,
        'per_kelas_labels': list(per_kelas.index),
        'per_kelas_values': [_safe_round(v) for v in per_kelas.values],
        'per_mapel_labels': list(per_mapel.index),
        'per_mapel_values': [_safe_round(v) for v in per_mapel.values],
        'per_semester_labels': list(per_semester.index),
        'per_semester_values': [_safe_round(v) for v in per_semester.values],
        'top_siswa': top_siswa,
        'perlu_perhatian': perlu_perhatian,
    }


def _analisis_kehadiran(df_kehadiran: pd.DataFrame) -> dict:
    kosong = {
        'distribusi_labels': [], 'distribusi_values': [],
        'per_kelas_labels': [], 'per_kelas_values': [],
        'kehadiran_rendah': [], 'persentase_hadir_keseluruhan': 0,
    }
    if df_kehadiran.empty:
        return kosong

    df = df_kehadiran.copy()
    distribusi = df['status'].value_counts()
    total = len(df)
    persentase_hadir = _safe_round((df['status'] == 'HADIR').sum() / total * 100) if total else 0

    per_kelas_pct = pd.Series(dtype=float)
    if 'kelas_nama' in df.columns:
        def pct_hadir(g):
            return (g == 'HADIR').sum() / len(g) * 100 if len(g) else 0
        per_kelas_pct = df.groupby('kelas_nama')['status'].apply(pct_hadir).sort_values(ascending=False)

    kehadiran_rendah = []
    if 'siswa_nama' in df.columns:
        def pct_hadir_siswa(g):
            return round((g == 'HADIR').sum() / len(g) * 100, 1) if len(g) else 0
        per_siswa = df.groupby('siswa_nama')['status'].apply(pct_hadir_siswa).reset_index()
        per_siswa.columns = ['siswa_nama', 'persentase_hadir']
        kehadiran_rendah = (
            per_siswa.sort_values('persentase_hadir', ascending=True)
            .head(10)
            .to_dict('records')
        )

    label_map = {'HADIR': 'Hadir', 'SAKIT': 'Sakit', 'IZIN': 'Izin', 'ALPA': 'Alpa'}
    return {
        'distribusi_labels': [label_map.get(k, k) for k in distribusi.index],
        'distribusi_values': [int(v) for v in distribusi.values],
        'per_kelas_labels': list(per_kelas_pct.index),
        'per_kelas_values': [_safe_round(v) for v in per_kelas_pct.values],
        'kehadiran_rendah': kehadiran_rendah,
        'persentase_hadir_keseluruhan': persentase_hadir,
    }


def _analisis_prestasi(df_prestasi: pd.DataFrame) -> dict:
    kosong = {
        'total_prestasi': 0,
        'per_tingkat_labels': [], 'per_tingkat_values': [],
        'top_siswa_prestasi': [],
    }
    if df_prestasi.empty:
        return kosong

    df = df_prestasi.copy()
    label_map = {
        'SEKOLAH': 'Sekolah', 'KECAMATAN': 'Kecamatan', 'KABUPATEN': 'Kabupaten/Kota',
        'PROVINSI': 'Provinsi', 'NASIONAL': 'Nasional',
    }
    per_tingkat = df['tingkat'].value_counts()

    top_siswa_prestasi = []
    if 'siswa_nama' in df.columns:
        agg = df.groupby('siswa_nama').size().reset_index(name='jumlah_prestasi')
        top_siswa_prestasi = (
            agg.sort_values('jumlah_prestasi', ascending=False).head(10).to_dict('records')
        )

    return {
        'total_prestasi': len(df),
        'per_tingkat_labels': [label_map.get(k, k) for k in per_tingkat.index],
        'per_tingkat_values': [int(v) for v in per_tingkat.values],
        'top_siswa_prestasi': top_siswa_prestasi,
    }


def _siswa_per_kelas(df_siswa: pd.DataFrame) -> dict:
    if df_siswa.empty or 'kelas_nama' not in df_siswa.columns:
        return {'labels': [], 'values': []}
    jumlah = df_siswa.groupby('kelas_nama').size().sort_index()
    return {'labels': list(jumlah.index), 'values': [int(v) for v in jumlah.values]}

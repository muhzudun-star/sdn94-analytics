import os
import django
import sqlite3
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction

from kepegawaian.models import Guru
from akademik.models import Kelas, MataPelajaran
from siswa.models import Siswa
from penilaian.models import Nilai, Kehadiran, Prestasi


DB_LAMA = "db_lama.sqlite3"


def parse_date(value):
    if not value:
        return None

    if isinstance(value, datetime):
        return value.date()

    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return None


def get_connection():
    if not os.path.exists(DB_LAMA):
        raise FileNotFoundError(
            f"Database lama tidak ditemukan: {DB_LAMA}"
        )

    conn = sqlite3.connect(DB_LAMA)
    conn.row_factory = sqlite3.Row
    return conn


@transaction.atomic
def migrasi():
    conn = get_connection()
    cur = conn.cursor()

    print("=" * 60)
    print("MIGRASI DATA DARI db_lama.sqlite3")
    print("=" * 60)

    # =========================================================
    # 1. GURU
    # =========================================================
    print("\n[1/7] Memindahkan Guru...")

    guru_map = {}

    rows = cur.execute("""
        SELECT
            id,
            nip,
            nama,
            jenis_kelamin,
            no_hp,
            alamat,
            tanggal_bergabung
        FROM akademik_guru
        ORDER BY id
    """).fetchall()

    for row in rows:
        guru, created = Guru.objects.update_or_create(
            nip=row["nip"],
            defaults={
                "nama": row["nama"],
                "jenis_kelamin": row["jenis_kelamin"],
                "no_hp": row["no_hp"] or "",
                "alamat": row["alamat"] or "",
                "tanggal_bergabung": parse_date(row["tanggal_bergabung"]),
            }
        )

        guru_map[row["id"]] = guru

    print(f"   ✓ Guru dipindahkan: {len(guru_map)}")

    # =========================================================
    # 2. KELAS
    # =========================================================
    print("\n[2/7] Memindahkan Kelas...")

    kelas_map = {}

    rows = cur.execute("""
        SELECT
            id,
            nama_kelas,
            tingkat,
            tahun_ajaran,
            wali_kelas_id
        FROM akademik_kelas
        ORDER BY id
    """).fetchall()

    for row in rows:

        wali = guru_map.get(row["wali_kelas_id"])

        kelas, created = Kelas.objects.update_or_create(
            nama_kelas=row["nama_kelas"],
            tahun_ajaran=row["tahun_ajaran"],
            defaults={
                "tingkat": row["tingkat"],
                "wali_kelas": wali,
            }
        )

        kelas_map[row["id"]] = kelas

    print(f"   ✓ Kelas dipindahkan: {len(kelas_map)}")

    # =========================================================
    # 3. MATA PELAJARAN
    # =========================================================
    print("\n[3/7] Memindahkan Mata Pelajaran...")

    mapel_map = {}

    rows = cur.execute("""
        SELECT
            id,
            kode_mapel,
            nama_mapel,
            kkm
        FROM akademik_matapelajaran
        ORDER BY id
    """).fetchall()

    for row in rows:

        mapel, created = MataPelajaran.objects.update_or_create(
            kode_mapel=row["kode_mapel"],
            defaults={
                "nama_mapel": row["nama_mapel"],
                "kkm": row["kkm"],
            }
        )

        mapel_map[row["id"]] = mapel

    print(f"   ✓ Mata pelajaran dipindahkan: {len(mapel_map)}")

    # =========================================================
    # 4. SISWA
    # =========================================================
    print("\n[4/7] Memindahkan Siswa...")

    siswa_map = {}

    rows = cur.execute("""
        SELECT
            id,
            nis,
            nisn,
            nama,
            jenis_kelamin,
            tempat_lahir,
            tanggal_lahir,
            alamat,
            nama_ortu,
            status,
            kelas_id
        FROM akademik_siswa
        ORDER BY id
    """).fetchall()

    for row in rows:

        kelas = kelas_map.get(row["kelas_id"])

        siswa, created = Siswa.objects.update_or_create(
            nis=row["nis"],
            defaults={
                "nisn": row["nisn"],
                "nama": row["nama"],
                "jenis_kelamin": row["jenis_kelamin"],
                "tempat_lahir": row["tempat_lahir"] or "",
                "tanggal_lahir": parse_date(row["tanggal_lahir"]),
                "alamat": row["alamat"] or "",
                "nama_ortu": row["nama_ortu"] or "",
                "kelas": kelas,
                "status": row["status"],
            }
        )

        siswa_map[row["id"]] = siswa

    print(f"   ✓ Siswa dipindahkan: {len(siswa_map)}")

    # =========================================================
    # 5. NILAI
    # =========================================================
    print("\n[5/7] Memindahkan Nilai...")

    rows = cur.execute("""
        SELECT
            id,
            jenis_nilai,
            nilai,
            semester,
            tahun_ajaran,
            tanggal_input,
            mapel_id,
            siswa_id
        FROM akademik_nilai
        ORDER BY id
    """).fetchall()

    nilai_count = 0

    for row in rows:

        siswa = siswa_map.get(row["siswa_id"])
        mapel = mapel_map.get(row["mapel_id"])

        if not siswa or not mapel:
            print(
                f"   ! Nilai ID {row['id']} dilewati "
                f"karena siswa/mapel tidak ditemukan."
            )
            continue

        nilai_obj, created = Nilai.objects.update_or_create(
            id=row["id"],
            defaults={
                "siswa": siswa,
                "mapel": mapel,
                "jenis_nilai": row["jenis_nilai"],
                "nilai": row["nilai"],
                "semester": row["semester"],
                "tahun_ajaran": row["tahun_ajaran"],
                "tanggal_input": parse_date(row["tanggal_input"]),
            }
        )

        nilai_count += 1

    print(f"   ✓ Nilai dipindahkan: {nilai_count}")

    # =========================================================
    # 6. KEHADIRAN
    # =========================================================
    print("\n[6/7] Memindahkan Kehadiran...")

    rows = cur.execute("""
        SELECT
            id,
            tanggal,
            status,
            keterangan,
            siswa_id
        FROM akademik_kehadiran
        ORDER BY id
    """).fetchall()

    kehadiran_count = 0

    for row in rows:

        siswa = siswa_map.get(row["siswa_id"])

        if not siswa:
            print(
                f"   ! Kehadiran ID {row['id']} dilewati "
                f"karena siswa tidak ditemukan."
            )
            continue

        Kehadiran.objects.update_or_create(
            siswa=siswa,
            tanggal=parse_date(row["tanggal"]),
            defaults={
                "status": row["status"],
                "keterangan": row["keterangan"] or "",
            }
        )

        kehadiran_count += 1

    print(f"   ✓ Kehadiran dipindahkan: {kehadiran_count}")

    # =========================================================
    # 7. PRESTASI
    # =========================================================
    print("\n[7/7] Memindahkan Prestasi...")

    rows = cur.execute("""
        SELECT
            id,
            nama_prestasi,
            tingkat,
            tahun,
            keterangan,
            siswa_id
        FROM akademik_prestasi
        ORDER BY id
    """).fetchall()

    prestasi_count = 0

    for row in rows:

        siswa = siswa_map.get(row["siswa_id"])

        if not siswa:
            print(
                f"   ! Prestasi ID {row['id']} dilewati "
                f"karena siswa tidak ditemukan."
            )
            continue

        Prestasi.objects.update_or_create(
            id=row["id"],
            defaults={
                "siswa": siswa,
                "nama_prestasi": row["nama_prestasi"],
                "tingkat": row["tingkat"],
                "tahun": row["tahun"],
                "keterangan": row["keterangan"] or "",
            }
        )

        prestasi_count += 1

    print(f"   ✓ Prestasi dipindahkan: {prestasi_count}")

    conn.close()

    # =========================================================
    # HASIL AKHIR
    # =========================================================
    print("\n" + "=" * 60)
    print("HASIL MIGRASI")
    print("=" * 60)

    print("Guru       :", Guru.objects.count())
    print("Kelas      :", Kelas.objects.count())
    print("Mapel      :", MataPelajaran.objects.count())
    print("Siswa      :", Siswa.objects.count())
    print("Nilai      :", Nilai.objects.count())
    print("Kehadiran  :", Kehadiran.objects.count())
    print("Prestasi   :", Prestasi.objects.count())

    print("=" * 60)
    print("MIGRASI SELESAI")
    print("=" * 60)


if __name__ == "__main__":
    migrasi()
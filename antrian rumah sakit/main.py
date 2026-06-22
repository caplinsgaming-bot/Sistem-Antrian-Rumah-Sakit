"""
main.py
SISTEM ANTRIAN RUMAH SAKIT - Antarmuka Command Line (CLI)

Ringkasan implementasi:
- Struktur data 1 : Queue berbasis Linked List (linked_queue.py) -> antrian pasien
- Struktur data 2 : Hash Map / dict (database.py)                -> index cepat by ID
- Sorting         : Insertion Sort (algorithms.py)                -> urutkan by prioritas
- Searching       : Linear Search & Binary Search (algorithms.py) -> cari pasien
- Basis data      : file CSV (data/pasien.csv)
- CRUD            : Create, Read, Update, Delete tersedia lewat menu CLI
"""

import os

from database import DatabasePasien
from models import Pasien
from algorithms import insertion_sort_prioritas, linear_search_nama

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pasien.csv")


def cetak_header(judul):
    print("\n" + "=" * 78)
    print(judul.center(78))
    print("=" * 78)


def cetak_daftar(daftar_pasien):
    if not daftar_pasien:
        print("(Tidak ada data pasien.)")
        return
    for i, p in enumerate(daftar_pasien, start=1):
        print(f"{i}. {p}")


def input_id_baru(db):
    while True:
        id_baru = input("Masukkan ID Pasien baru (contoh: P001): ").strip()
        if not id_baru:
            print("ID tidak boleh kosong.")
            continue
        if db.cari_by_id(id_baru):
            print("ID sudah digunakan, gunakan ID lain.")
            continue
        return id_baru


def input_usia():
    while True:
        nilai = input("Usia: ").strip()
        if nilai.isdigit():
            return int(nilai)
        print("Usia harus berupa angka bulat positif.")


def pilih_prioritas(default="Normal"):
    print("Pilihan prioritas: 1) Darurat   2) Mendesak   3) Normal")
    pilihan = input(f"Pilih prioritas [1-3] (kosongkan = {default}): ").strip()
    return {"1": "Darurat", "2": "Mendesak", "3": "Normal"}.get(pilihan, default if pilihan == "" else "Normal")


# ---------------------- CREATE ----------------------
def menu_tambah(db):
    cetak_header("TAMBAH PASIEN BARU  (CREATE)")
    id_pasien = input_id_baru(db)
    nama = input("Nama pasien: ").strip()
    usia = input_usia()
    keluhan = input("Keluhan: ").strip()
    prioritas = pilih_prioritas()

    pasien_baru = Pasien(id_pasien, nama, usia, keluhan, prioritas)
    db.tambah_pasien(pasien_baru)
    print(f"\n✔ Pasien '{nama}' berhasil ditambahkan ke antrian dengan ID {id_pasien}.")


# ---------------------- READ ----------------------
def menu_lihat_semua(db):
    cetak_header("DAFTAR ANTRIAN PASIEN AKTIF  (READ)")
    cetak_daftar(db.semua_pasien())


def menu_lihat_riwayat(db):
    cetak_header("RIWAYAT SELURUH PASIEN  (READ)")
    cetak_daftar(db.semua_riwayat())


def menu_cari(db):
    cetak_header("CARI PASIEN  (READ / SEARCHING)")
    print("1. Cari berdasarkan ID    -> Hash Map, O(1)")
    print("2. Cari berdasarkan Nama  -> Linear Search, O(n)")
    pilihan = input("Pilih metode [1-2]: ").strip()
    if pilihan == "1":
        id_pasien = input("Masukkan ID: ").strip()
        hasil = db.cari_by_id(id_pasien)
        cetak_daftar([hasil] if hasil else [])
    else:
        kata_kunci = input("Masukkan nama / sebagian nama: ").strip()
        hasil = linear_search_nama(db.semua_pasien(), kata_kunci)
        cetak_daftar(hasil)


# ---------------------- UPDATE ----------------------
def menu_update(db):
    cetak_header("UPDATE DATA PASIEN  (UPDATE)")
    id_pasien = input("Masukkan ID pasien yang ingin diupdate: ").strip()
    p = db.cari_by_id(id_pasien)
    if not p:
        print("✘ Pasien tidak ditemukan.")
        return

    print(f"Data saat ini -> {p}")
    nama = input(f"Nama baru (Enter = tetap '{p.nama}'): ").strip()
    keluhan = input(f"Keluhan baru (Enter = tetap '{p.keluhan}'): ").strip()
    print("Prioritas: 1) Darurat  2) Mendesak  3) Normal  (Enter = tetap)")
    pilihan_prioritas = input("Pilih: ").strip()
    prioritas = {"1": "Darurat", "2": "Mendesak", "3": "Normal"}.get(pilihan_prioritas)
    print("Status: 1) Menunggu  2) Dipanggil  3) Selesai  (Enter = tetap)")
    pilihan_status = input("Pilih: ").strip()
    status = {"1": "Menunggu", "2": "Dipanggil", "3": "Selesai"}.get(pilihan_status)

    perubahan = {}
    if nama:
        perubahan["nama"] = nama
    if keluhan:
        perubahan["keluhan"] = keluhan
    if prioritas:
        perubahan["prioritas"] = prioritas
    if status:
        perubahan["status"] = status

    if db.update_pasien(id_pasien, **perubahan):
        print("✔ Data pasien berhasil diperbarui.")
    else:
        print("✘ Gagal memperbarui data.")


# ---------------------- DELETE ----------------------
def menu_hapus(db):
    cetak_header("HAPUS PASIEN  (DELETE)")
    id_pasien = input("Masukkan ID pasien yang ingin dihapus: ").strip()
    p = db.hapus_pasien(id_pasien)
    if p:
        print(f"✔ Pasien '{p.nama}' (ID {p.id_pasien}) berhasil dihapus.")
    else:
        print("✘ Pasien tidak ditemukan.")


# ---------------------- SORTING & QUEUE ----------------------
def menu_urutkan(db):
    cetak_header("URUTKAN ANTRIAN BERDASARKAN PRIORITAS  (SORTING)")
    data_terurut = insertion_sort_prioritas(db.semua_pasien())
    db.urutkan_dan_simpan(data_terurut)
    print("Antrian berhasil diurutkan ulang (Darurat > Mendesak > Normal, lalu waktu daftar):")
    cetak_daftar(db.semua_pasien())


def menu_panggil_berikutnya(db):
    cetak_header("PANGGIL PASIEN BERIKUTNYA  (DEQUEUE)")
    p = db.selesaikan_pasien_terdepan()
    if p:
        print(f"📢 Memanggil pasien: {p.nama} (ID {p.id_pasien}) - Keluhan: {p.keluhan}")
        print("Status pasien diubah menjadi 'Selesai' dan tersimpan di riwayat.")
    else:
        print("Antrian kosong, tidak ada pasien untuk dipanggil.")


def tampilkan_menu():
    cetak_header("SISTEM ANTRIAN RUMAH SAKIT")
    print(" 1. Tambah Pasien                          (Create)")
    print(" 2. Lihat Antrian Aktif                     (Read)")
    print(" 3. Lihat Riwayat Seluruh Pasien            (Read)")
    print(" 4. Cari Pasien                             (Searching)")
    print(" 5. Update Data Pasien                      (Update)")
    print(" 6. Hapus Pasien                            (Delete)")
    print(" 7. Urutkan Antrian Berdasarkan Prioritas   (Sorting)")
    print(" 8. Panggil Pasien Berikutnya               (Dequeue)")
    print(" 9. Keluar")


def main():
    db = DatabasePasien(CSV_PATH)
    aksi = {
        "1": menu_tambah,
        "2": menu_lihat_semua,
        "3": menu_lihat_riwayat,
        "4": menu_cari,
        "5": menu_update,
        "6": menu_hapus,
        "7": menu_urutkan,
        "8": menu_panggil_berikutnya,
    }
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu [1-9]: ").strip()
        if pilihan == "9":
            print(f"\nTerima kasih. Semua data tersimpan di: {CSV_PATH}")
            break
        fungsi = aksi.get(pilihan)
        if fungsi:
            try:
                fungsi(db)
            except Exception as e:
                print(f"⚠ Terjadi kesalahan: {e}")
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()

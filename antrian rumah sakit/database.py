"""
database.py
Lapisan penyimpanan data aplikasi:

- File CSV (data/pasien.csv) sebagai basis data permanen.
- HASH MAP (dict Python: id_pasien -> Pasien) sebagai index in-memory
  untuk akses/CRUD super cepat berdasarkan ID -> kompleksitas O(1).
- Queue berbasis Linked List (lihat linked_queue.py) untuk merepresentasikan
  urutan antrian pasien yang masih aktif (belum dilayani).

Setiap operasi CRUD yang mengubah data akan menulis ulang seluruh isi
hash map ke file CSV, sehingga CSV selalu menjadi "sumber kebenaran" (source
of truth) yang konsisten dengan data di memori.
"""

import csv
import os

from models import Pasien
from linked_queue import AntrianPasien

FIELDS = ["id_pasien", "nama", "usia", "keluhan", "prioritas", "status", "waktu_daftar"]


class DatabasePasien:
    def __init__(self, csv_path="data/pasien.csv"):
        self.csv_path = csv_path
        self.hash_map = {}              # struktur data Hash Map: id -> Pasien
        self.antrian = AntrianPasien()  # struktur data Queue (Linked List)
        self._pastikan_file_ada()
        self._muat_dari_csv()

    # ---------------- util internal ----------------
    def _pastikan_file_ada(self):
        folder = os.path.dirname(self.csv_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()

    def _muat_dari_csv(self):
        """Membaca seluruh isi CSV ke Hash Map, dan memasukkan pasien yang
        belum 'Selesai' ke dalam Queue (Linked List)."""
        self.hash_map.clear()
        self.antrian = AntrianPasien()
        with open(self.csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("id_pasien"):
                    continue
                p = Pasien.from_dict(row)
                self.hash_map[p.id_pasien] = p
                if p.status != "Selesai":
                    self.antrian.enqueue(p)

    def _simpan_ke_csv(self):
        """Menulis ulang seluruh isi Hash Map ke file CSV."""
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for p in self.hash_map.values():
                writer.writerow(p.to_dict())

    # ---------------- CREATE ----------------
    def tambah_pasien(self, pasien: Pasien):
        if pasien.id_pasien in self.hash_map:
            raise ValueError(f"ID pasien '{pasien.id_pasien}' sudah terdaftar.")
        self.hash_map[pasien.id_pasien] = pasien
        self.antrian.enqueue(pasien)
        self._simpan_ke_csv()

    # ---------------- READ ----------------
    def cari_by_id(self, id_pasien):
        """Pencarian via Hash Map -> kompleksitas O(1)."""
        return self.hash_map.get(str(id_pasien))

    def semua_pasien(self):
        """Mengembalikan daftar pasien yang masih aktif di antrian (Queue)."""
        return self.antrian.to_list()

    def semua_riwayat(self):
        """Mengembalikan seluruh data pasien, termasuk yang sudah 'Selesai'."""
        return list(self.hash_map.values())

    # ---------------- UPDATE ----------------
    def update_pasien(self, id_pasien, **perubahan):
        p = self.hash_map.get(str(id_pasien))
        if p is None:
            return False
        for k, v in perubahan.items():
            if v not in (None, "") and hasattr(p, k):
                setattr(p, k, v)
        self._simpan_ke_csv()
        return True

    # ---------------- DELETE ----------------
    def hapus_pasien(self, id_pasien):
        p = self.hash_map.pop(str(id_pasien), None)
        if p is None:
            return None
        self.antrian.remove_by_id(str(id_pasien))
        self._simpan_ke_csv()
        return p

    def selesaikan_pasien_terdepan(self):
        """Dequeue pasien terdepan antrian, ubah status jadi 'Selesai',
        riwayatnya tetap tersimpan permanen di CSV."""
        p = self.antrian.dequeue()
        if p is None:
            return None
        p.status = "Selesai"
        self._simpan_ke_csv()
        return p

    def urutkan_dan_simpan(self, list_terurut):
        """Membangun ulang urutan Queue (Linked List) sesuai hasil sorting."""
        self.antrian.rebuild_from_list(list_terurut)

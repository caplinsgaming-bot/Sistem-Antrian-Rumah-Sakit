"""
models.py
Definisi struktur data Pasien (Patient) untuk Sistem Antrian Rumah Sakit.
"""
from datetime import datetime


class Pasien:
    """Merepresentasikan satu data pasien dalam antrian rumah sakit."""

    # Bobot prioritas: semakin kecil angka, semakin diutamakan
    PRIORITAS_BOBOT = {
        "Darurat": 0,
        "Mendesak": 1,
        "Normal": 2,
    }

    def __init__(self, id_pasien, nama, usia, keluhan, prioritas="Normal",
                 status="Menunggu", waktu_daftar=None):
        self.id_pasien = str(id_pasien)
        self.nama = nama
        self.usia = int(usia)
        self.keluhan = keluhan
        self.prioritas = prioritas if prioritas in self.PRIORITAS_BOBOT else "Normal"
        self.status = status
        self.waktu_daftar = waktu_daftar or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def bobot_prioritas(self):
        return self.PRIORITAS_BOBOT.get(self.prioritas, 2)

    def to_dict(self):
        return {
            "id_pasien": self.id_pasien,
            "nama": self.nama,
            "usia": self.usia,
            "keluhan": self.keluhan,
            "prioritas": self.prioritas,
            "status": self.status,
            "waktu_daftar": self.waktu_daftar,
        }

    @staticmethod
    def from_dict(d):
        return Pasien(
            id_pasien=d["id_pasien"],
            nama=d["nama"],
            usia=d["usia"],
            keluhan=d["keluhan"],
            prioritas=d.get("prioritas", "Normal"),
            status=d.get("status", "Menunggu"),
            waktu_daftar=d.get("waktu_daftar"),
        )

    def __str__(self):
        return (f"[{self.id_pasien}] {self.nama:<18} | Usia: {self.usia:<3} | "
                f"Keluhan: {self.keluhan:<22} | Prioritas: {self.prioritas:<9} | "
                f"Status: {self.status:<10} | Daftar: {self.waktu_daftar}")

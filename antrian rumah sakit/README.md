# Sistem Antrian Rumah Sakit

Aplikasi CLI (Command Line Interface) berbasis Python untuk mengelola antrian
pasien rumah sakit, lengkap dengan implementasi struktur data, algoritma
sorting & searching, serta penyimpanan data menggunakan file CSV.

## Cara Menjalankan

```bash
cd hospital_queue_system
python3 main.py
```

Tidak ada library eksternal yang dibutuhkan (hanya modul standar Python:
`csv`, `os`, `datetime`).

## Struktur Berkas

```
hospital_queue_system/
├── main.py            -> Antarmuka CLI (menu & alur program)
├── models.py           -> Class Pasien (struktur data record pasien)
├── linked_queue.py      -> Struktur data Queue berbasis Linked List
├── database.py         -> Hash Map + CRUD + sinkronisasi ke CSV
├── algorithms.py        -> Algoritma Sorting (Insertion Sort) & Searching
│                           (Linear Search, Binary Search)
└── data/
    └── pasien.csv        -> Basis data (CSV)
```

## Struktur Data yang Diimplementasikan

| Struktur Data        | Lokasi             | Kegunaan                                                   |
|-----------------------|---------------------|--------------------------------------------------------------|
| **Queue (Linked List)** | `linked_queue.py` | Merepresentasikan urutan antrian pasien (FIFO), `enqueue` saat pasien baru daftar, `dequeue` saat pasien dipanggil |
| **Hash Map (dict)**    | `database.py`      | Index pasien berdasarkan `id_pasien` agar pencarian/CRUD berjalan O(1) |
| **Sorting**             | `algorithms.py`     | *Insertion Sort* untuk mengurutkan antrian berdasarkan tingkat prioritas (Darurat > Mendesak > Normal), lalu waktu daftar |
| **Searching**           | `algorithms.py`     | *Linear Search* (cari berdasarkan nama) dan *Binary Search* (cari berdasarkan ID pada data terurut) |

## Operasi CRUD

| Operasi | Menu CLI | Penjelasan |
|---------|----------|------------|
| **Create** | 1. Tambah Pasien | Menambah pasien baru ke Hash Map, di-*enqueue* ke antrian (Linked List), lalu ditulis ke CSV |
| **Read**   | 2. Lihat Antrian Aktif / 3. Lihat Riwayat / 4. Cari Pasien | Membaca data dari Linked List / Hash Map, termasuk fitur searching |
| **Update** | 5. Update Data Pasien | Mengubah nama, keluhan, prioritas, atau status pasien berdasarkan ID, lalu menulis ulang CSV |
| **Delete** | 6. Hapus Pasien | Menghapus pasien dari Hash Map & Linked List, lalu menulis ulang CSV |

Menu tambahan:
- **7. Urutkan Antrian Berdasarkan Prioritas** — menjalankan algoritma sorting.
- **8. Panggil Pasien Berikutnya** — men-*dequeue* pasien terdepan antrian (mengubah status menjadi "Selesai", riwayatnya tetap tersimpan di CSV).

## Format Data CSV (`data/pasien.csv`)

| Kolom | Keterangan |
|-------|------------|
| id_pasien | ID unik pasien, contoh `P001` |
| nama | Nama pasien |
| usia | Usia pasien |
| keluhan | Keluhan / alasan berobat |
| prioritas | `Darurat`, `Mendesak`, atau `Normal` |
| status | `Menunggu`, `Dipanggil`, atau `Selesai` |
| waktu_daftar | Stempel waktu pendaftaran (otomatis) |

## Catatan Kompleksitas

- Pencarian by ID via Hash Map: **O(1)** rata-rata.
- Pencarian by Nama via Linear Search: **O(n)**.
- Pencarian by ID via Binary Search (contoh algoritma tambahan): **O(log n)** — memerlukan data terurut.
- Enqueue / Dequeue pada Linked List: **O(1)**.
- Hapus pasien di posisi tertentu pada Linked List: **O(n)**.
- Insertion Sort untuk mengurutkan antrian: **O(n²)** kasus terburuk, mendekati **O(n)** jika data sudah hampir terurut.

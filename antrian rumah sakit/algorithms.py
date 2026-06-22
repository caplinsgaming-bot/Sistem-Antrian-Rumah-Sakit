"""
algorithms.py
Implementasi algoritma SORTING dan SEARCHING secara manual
(tidak memakai sorted()/list.sort() bawaan ataupun operator 'in' Python).
"""


def insertion_sort_prioritas(daftar_pasien):
    """
    Mengurutkan daftar pasien berdasarkan:
    1) bobot prioritas (Darurat < Mendesak < Normal)
    2) waktu_daftar (yang lebih dulu daftar, lebih dulu dilayani)

    Algoritma: Insertion Sort -> kompleksitas waktu O(n^2), O(n) untuk data
    yang hampir terurut (cocok karena antrian biasanya sudah cukup rapi).
    """
    data = list(daftar_pasien)
    for i in range(1, len(data)):
        kunci = data[i]
        j = i - 1
        while j >= 0 and _lebih_diprioritaskan(kunci, data[j]):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = kunci
    return data


def _lebih_diprioritaskan(a, b):
    """True jika pasien a harus dilayani lebih dulu dibanding pasien b."""
    if a.bobot_prioritas() != b.bobot_prioritas():
        return a.bobot_prioritas() < b.bobot_prioritas()
    return a.waktu_daftar < b.waktu_daftar


def linear_search_nama(daftar_pasien, kata_kunci):
    """
    Mencari pasien berdasarkan potongan nama (case-insensitive).
    Algoritma: Linear Search -> kompleksitas O(n).
    Mengembalikan list semua pasien yang cocok.
    """
    kata_kunci = kata_kunci.strip().lower()
    hasil = []
    for p in daftar_pasien:
        if kata_kunci in p.nama.lower():
            hasil.append(p)
    return hasil


def binary_search_by_id(daftar_pasien_terurut_id, id_pasien):
    """
    Mencari pasien berdasarkan id_pasien pada list yang SUDAH terurut
    menaik berdasarkan id_pasien.
    Algoritma: Binary Search -> kompleksitas O(log n).

    Catatan: disertakan sebagai contoh tambahan algoritma searching.
    Pencarian utama by-ID pada aplikasi memakai Hash Map (lihat database.py)
    karena memberi kompleksitas rata-rata O(1).
    """
    data = sorted(daftar_pasien_terurut_id, key=lambda p: p.id_pasien)
    low, high = 0, len(data) - 1
    target = str(id_pasien)
    while low <= high:
        mid = (low + high) // 2
        mid_id = data[mid].id_pasien
        if mid_id == target:
            return data[mid]
        elif mid_id < target:
            low = mid + 1
        else:
            high = mid - 1
    return None

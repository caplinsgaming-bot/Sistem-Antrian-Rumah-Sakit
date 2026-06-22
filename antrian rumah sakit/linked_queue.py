"""
linked_queue.py
Implementasi struktur data QUEUE (Antrian) menggunakan LINKED LIST murni
(tidak menggunakan list/deque bawaan Python untuk penyimpanan utamanya).

Operasi yang didukung:
- enqueue(pasien)      : menambah pasien ke akhir antrian -> O(1)
- dequeue()            : mengambil & menghapus pasien terdepan -> O(1)
- remove_by_id(id)     : menghapus pasien di posisi manapun -> O(n)
- to_list() / rebuild_from_list() : konversi untuk keperluan sorting/tampilan
"""


class _Node:
    """Node tunggal dalam linked list, menyimpan satu objek Pasien."""
    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class AntrianPasien:
    """Queue (FIFO) berbasis Singly Linked List untuk objek Pasien."""

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    # ---------- operasi inti Queue ----------
    def enqueue(self, pasien):
        """Menambahkan pasien baru ke ekor antrian. Kompleksitas O(1)."""
        node = _Node(pasien)
        if self._tail is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self):
        """Mengambil sekaligus menghapus pasien di kepala antrian. O(1)."""
        if self._head is None:
            return None
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.data

    def peek(self):
        return self._head.data if self._head else None

    # ---------- operasi pendukung CRUD ----------
    def remove_by_id(self, id_pasien):
        """Menghapus node dengan id_pasien tertentu di posisi manapun. O(n)."""
        prev = None
        curr = self._head
        while curr:
            if curr.data.id_pasien == str(id_pasien):
                if prev is None:
                    self._head = curr.next
                else:
                    prev.next = curr.next
                if curr is self._tail:
                    self._tail = prev
                self._size -= 1
                return curr.data
            prev = curr
            curr = curr.next
        return None

    def to_list(self):
        """Mengubah isi linked list menjadi list Python (untuk tampilan/sorting)."""
        hasil = []
        curr = self._head
        while curr:
            hasil.append(curr.data)
            curr = curr.next
        return hasil

    def rebuild_from_list(self, data_list):
        """Membangun ulang linked list dari sebuah list (dipakai setelah sorting)."""
        self._head = None
        self._tail = None
        self._size = 0
        for item in data_list:
            self.enqueue(item)

# Lab Test: Build a Warehouse Crate & Manifest System

## Deskripsi
Buatlah sebuah class bernama `Crate` untuk mengelola inventaris peti penyimpanan kargo dan sebuah fungsi standalone bernama `get_overloaded_crates` untuk menyaring peti yang hampir penuh.

---

## 1. Class `Crate`

### `__init__(self, crate_id, max_weight)`
- **Validasi `crate_id`:**
  - Harus bertipe `str`. Jika bukan, picu `TypeError`.
  - Bersihkan spasi di awal dan akhir menggunakan `.strip()`.
  - Format harus diawali `"CR-"` dan diikuti minimal 1 karakter digit angka saja (contoh valid: `"CR-101"`; tidak valid: `"CR-12A"`, `"101"`, `"CR-"`). Jika format salah, picu `ValueError`.
- **Validasi `max_weight`:**
  - Harus bertipe `int` atau `float`. Tipe `bool` wajib ditolak dengan memicu `TypeError`.
  - Nilainya harus lebih besar dari `0`. Jika `<= 0`, picu `ValueError`.
- **Atribut yang disimpan:**
  - `self.crate_id`: string hasil `.strip()`.
  - `self.max_weight`: angka yang dikonversi ke `float`.
  - `self.items`: diinisialisasi sebagai `list` kosong (`[]`).

### `add_item(self, name, weight, category="general")`
- **Validasi `name` & `category`:**
  - Harus bertipe `str`. Jika bukan, picu `TypeError`.
  - Setelah di-`.strip()`, string tidak boleh kosong. Jika kosong, picu `ValueError`.
- **Validasi `weight`:**
  - Harus bertipe `int` atau `float` (tolak tipe `bool` dengan `TypeError`).
  - Nilai harus lebih besar dari `0`. Jika `<= 0`, picu `ValueError`.
- **Logika Penambahan:**
  - Periksa apakah berat saat ini ditambah `weight` melebihi `self.max_weight`.
  - Jika **melebihi kapasitas**, batalkan penambahan dan kembalikan `False`.
  - Jika **muat**, simpan ke dalam `self.items` berupa dictionary:
    ```python
    {
        "name": name.strip(),
        "weight": float(weight),
        "category": category.strip().lower()
    }
    ```
  - Kembalikan `True`.

### `remove_item(self, name)`
- Cari item pertama di dalam `self.items` yang namanya cocok dengan parameter `name` secara *case-insensitive*.
- Jika ditemukan:
  - Hapus dictionary item tersebut dari `self.items`.
  - Kembalikan (*return*) dictionary item yang baru saja dihapus.
- Jika tidak ditemukan:
  - Picu `KeyError("Item not found")`.

### `get_current_weight(self)`
- Mengembalikan total berat seluruh item di dalam `self.items`.
- Nilai dibulatkan ke 2 angka desimal menggunakan `round()`.
- Jika `self.items` kosong, kembalikan `0.0`.

### `get_categories(self)`
- Mengembalikan sebuah `set` yang berisi seluruh kategori unik dari item yang saat ini ada di dalam `self.items`.

### `__str__(self)`
- Mengembalikan representasi string multi-baris:
  - **Baris 1 (Header):**
    `Crate [crate_id] ([current_weight:.2f]/[max_weight:.2f] kg)`
  - **Jika kosong (`self.items` tidak ada item):**
    `-- Empty --`
  - **Jika ada isinya (tiap item di baris baru):**
    `- [name] ([category]): [weight:.2f] kg`

---

## 2. Standalone Function: `get_overloaded_crates`

### `get_overloaded_crates(crates, threshold_percent)`
- **Parameter:**
  - `crates`: sebuah `list` berisi objek-objek dari class `Crate`.
  - `threshold_percent`: bertipe `int` atau `float` dengan rentang nilai `0` hingga `100` inklusif. Jika di luar rentang ini, picu `ValueError`.
- **Logika:**
  - Hitung persentase beban setiap peti:
    $$\text{Persentase} = \left(\frac{\text{berat saat ini}}{\text{max\_weight}}\right) \times 100$$
  - Saring dan ambil `crate_id` dari setiap peti yang persentase bebannya **$\ge$ `threshold_percent`**.
  - Urutkan hasil list `crate_id` tersebut dari persentase beban **tertinggi ke terendah**.
  - Kembalikan list `crate_id` yang sudah terurut.
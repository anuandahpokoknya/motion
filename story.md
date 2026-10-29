# Lab Test: Build an Event Ticketing & Revenue Engine

## Deskripsi
Buat dua class: `TicketTier` (mengelola kategori tiket & sisa kuota) dan `Event` (mengelola penjualan tiket, pembatalan dengan potongan penalti, dan pelaporan keuangan), serta satu fungsi standalone `get_top_performing_events`.

---

## 1. Class `TicketTier`

### `__init__(self, tier_name, price, capacity)`
- **Validasi `tier_name`:**
  - Harus bertipe `str`. Jika bukan, picu `TypeError`.
  - Bersihkan dengan `.strip()`. Jika kosong, picu `ValueError`.
  - Simpan dalam format *Title Case* (gunakan `.title()`).
- **Validasi `price` & `capacity`:**
  - `price`: bertipe `int` atau `float` (tolak `bool` dengan `TypeError`), nilai harus `> 0` (jika tidak, picu `ValueError`).
  - `capacity`: bertipe `int` (tolak `bool` dan float dengan `TypeError`), nilai harus `> 0` (jika tidak, picu `ValueError`).
- **Atribut:**
  - `self.tier_name`: string title case hasil sanitasi.
  - `self.price`: angka dikonversi ke `float`.
  - `self.capacity`: integer kapasitas total kursi.
  - `self.sold`: integer jumlah tiket terjual, diinisialisasi dengan nilai `0`.

### `get_available_seats(self)`
- Mengembalikan sisa kursi yang belum terjual (`self.capacity - self.sold`).

### `__str__(self)`
- Mengembalikan string format:
  `"[tier_name] - $[price:.2f] (Available: [available]/[capacity])"`
  *(Contoh: `"Vip - $150.00 (Available: 15/20)"`)*

---

## 2. Class `Event`

### `__init__(self, event_code, event_name)`
- **Validasi `event_code`:**
  - Harus bertipe `str`. Jika bukan, picu `TypeError`.
  - Setelah di-`.strip()`, harus diawali `"EVT-"` dan diikuti **tepat 4 karakter digit angka** (contoh valid: `"EVT-2026"`; tidak valid: `"EVT-26"`, `"EVT-202A"`, `"2026"`). Jika format salah, picu `ValueError`.
- **Validasi `event_name`:**
  - Harus bertipe `str` yang tidak kosong setelah di-`.strip()`. Jika tipe salah picu `TypeError`, jika kosong picu `ValueError`.
- **Atribut:**
  - `self.event_code`: string bersih.
  - `self.event_name`: string bersih.
  - `self.tiers`: diinisialisasi sebagai dictionary kosong `{}`.
  - `self.bookings`: diinisialisasi sebagai list kosong `[]`.

### `add_tier(self, tier)`
- Parameter `tier` harus berupa instance dari class `TicketTier` (gunakan `isinstance()`). Jika bukan, picu `TypeError`.
- Kunci penyimpanan di `self.tiers` adalah nama tier dalam huruf kecil (`tier.tier_name.lower()`).
- Jika nama tier sudah terdaftar di `self.tiers`, picu `ValueError("Tier already exists")`.
- Simpan `tier` ke `self.tiers`.

### `book_tickets(self, customer_name, tier_name, quantity, discount_percent=0.0)`
- **Validasi:**
  - `customer_name`: `str` non-empty (setelah `.strip()`). Jika salah tipe: `TypeError`, jika kosong: `ValueError`.
  - `tier_name`: `str`. Jika bukan string: `TypeError`. Cari tier di `self.tiers` secara *case-insensitive*. Jika tidak ditemukan: `KeyError("Tier not found")`.
  - `quantity`: `int` (tolak `bool` dengan `TypeError`), nilai harus `> 0` (jika `<= 0` picu `ValueError`).
  - `discount_percent`: `int` atau `float` (tolak `bool` dengan `TypeError`), nilai harus di rentang `0.0` sampai `50.0` inklusif. Jika di luar rentang, picu `ValueError`.
- **Logika Pemesanan:**
  - Cek ketersediaan tiket di tier yang dipilih. Jika `quantity > tier.get_available_seats()`, jangan proses pemesanan dan kembalikan `False`.
  - Jika tiket cukup:
    - Tambah `tier.sold` sebanyak `quantity`.
    - Hitung total bayar: `(quantity * tier.price) * (1 - discount_percent / 100)`. Bulatkan ke **2 angka desimal**.
    - Buat ID transaksi unik dengan format `"TRX-[nomor_urut_3_digit]"` dimulai dari `001` (contoh transaksi pertama: `"TRX-001"`, transaksi kedua: `"TRX-002"`, dst., memanfaatkan panjang `self.bookings`).
    - Simpan dictionary transaksi ke dalam `self.bookings`:
      ```python
      {
          "booking_id": booking_id,
          "customer": customer_name.strip(),
          "tier_key": tier_name.strip().lower(),
          "quantity": quantity,
          "total_paid": total_paid
      }
      ```
    - Kembalikan string `booking_id` tersebut.

### `cancel_booking(self, booking_id, penalty_percent=20.0)`
- **Validasi:**
  - `penalty_percent`: `int` atau `float` (tolak `bool` dengan `TypeError`) di rentang `0.0` sampai `100.0`. Jika di luar rentang, picu `ValueError`.
- **Logika Pembatalan:**
  - Cari transaksi di `self.bookings` berdasarkan `booking_id` (case-insensitive).
  - Jika tidak ditemukan, picu `KeyError("Booking not found")`.
  - Jika ditemukan:
    - Kembalikan stok kursi tier terkait: kurangi `tier.sold` sebanyak `quantity` dari transaksi yang dibatalkan.
    - Hitung nilai pengembalian dana (*refund*): `total_paid * (1 - penalty_percent / 100)`. Bulatkan ke **2 angka desimal**.
    - Hapus data transaksi tersebut dari `self.bookings`.
    - Kembalikan nilai nominal refund (`float`).

### `get_revenue(self)`
- Mengembalikan total uang yang saat ini ada di dalam `self.bookings` (`sum` dari semua `total_paid`, dibulatkan ke **2 angka desimal**). Kembalikan `0.0` jika belum ada pemesanan.

### `get_sold_out_tiers(self)`
- Mengembalikan sebuah `set` berisi nama asli `tier_name` dari kategori-kategori tiket yang sisa kursinya sudah habis (`get_available_seats() == 0`).

### Special Methods:
- **`__len__(self)`:**
  - Mengembalikan total seluruh tiket yang sudah terjual dari seluruh tier yang ada di event ini (akumulasi integer `tier.sold`).
- **`__str__(self)`:**
  - Menghasilkan format teks laporan:
    - **Baris 1:** `"EVENT: [event_name] ([event_code])"`
    - **Baris berikutnya:** daftar seluruh tier yang terdaftar (menggunakan string representasi dari masing-masing `TicketTier`, diawali tanda `- `). Jika belum ada tier, tulis `"-- No Tiers --"`.
    - **Baris terakhir:** `"Total Sold: [total_tiket] | Revenue: $[revenue:.2f]"`

---

## 3. Standalone Function: `get_top_performing_events`

### `get_top_performing_events(events, min_revenue)`
- **Parameter:**
  - `events`: `list` berisi objek-objek dari class `Event`.
  - `min_revenue`: `int` atau `float` (tolak `bool` dengan `TypeError`). Nilai harus `>= 0` (jika tidak, picu `ValueError`).
- **Logika:**
  - Saring event yang memiliki `get_revenue() >= min_revenue`.
  - Urutkan event yang lolos berdasarkan dua kriteria:
    1. **Tiket terjual terbanyak** (dihitung menggunakan `len(event)`, urutan menurun / *descending*).
    2. Jika jumlah tiket terjual sama, urutkan berdasarkan **revenue tertinggi** (urutan menurun / *descending*).
  - Kembalikan `list` berisi string `event_code` dari event-event yang sudah terurut tersebut.
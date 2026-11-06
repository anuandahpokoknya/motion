# Final Pre-OOP Lab: Financial Fraud & Threat Intelligence Enginexxx

Bangun sebuah pipeline pemrosesan data dan deteksi anomali yang terdiri dari 4 fungsi terpisah (tanpa menggunakan class). Output dari satu fungsi akan menjadi input bagi fungsi berikutnya.

---

## 1. `parse_transaction_logs(raw_logs)`

Membersihkan, memvalidasi, dan mengekstrak daftar catatan transaksi mentah menjadi struktur data yang siap diolah.

### Validasi Parameter Utama
* `raw_logs` wajib bertipe `list`. Jika bukan, picu `TypeError`.
* Setiap elemen di dalam `raw_logs` wajib bertipe `str`. Jika ditemukan elemen bertipe lain, langsung hentikan eksekusi dan picu `TypeError`.

### Struktur Baris Log
Setiap string mewakili 1 catatan dengan 5 bagian yang dipisahkan oleh karakter pipa (`|`):
```text
kode_transaksi | id_pengguna | lokasi_negara | kategori | nominal
```
*Contoh:* `" TX-9001 | USR-104 | id | TRANSFER | 1500.505 "`

### Aturan Penyaringan Baris
Jika sebuah baris melanggar salah satu syarat di bawah ini, abaikan/lewati baris tersebut tanpa menghentikan program:
1. **Format Kolom:** Harus memiliki tepat 5 bagian setelah dipisah dengan tanda pipa (`|`). Spasi di awal dan akhir setiap bagian harus dibersihkan (`strip`).
2. **Kode Transaksi (`tx_id`):** Harus diawali huruf kapital `"TX-"` dan diikuti tepat 4 digit angka murni (`0`–`9`).
3. **ID Pengguna (`user_id`):** Harus diawali huruf kapital `"USR-"` dan diikuti minimal 1 karakter digit angka murni.
4. **Lokasi Negara (`country`):** Harus terdiri dari tepat 2 karakter alfabet saja (tanpa angka/simbol), lalu disimpan dalam huruf kapital (contoh: `"ID"`, `"US"`, `"SG"`).
5. **Kategori (`category`):** Teks tidak boleh kosong, disimpan dalam huruf kecil semua. Hanya ada 3 kategori valid:
   * `"transfer"`
   * `"withdrawal"`
   * `"login_fail"`  
   *(Jika di luar 3 kategori tersebut, abaikan baris).*
6. **Nominal (`amount`):** Harus berupa teks yang valid jika dikonversi menjadi angka desimal (`float`).
   * Kategori `"transfer"` dan `"withdrawal"`: nilai nominal wajib **> 0**.
   * Kategori `"login_fail"`: nilai nominal wajib **tepat 0**.

### Nilai Kembalian
Sebuah `list` berisi `dict` untuk setiap baris yang sah dengan format kunci:
* `"tx_id"`: `str`
* `"user_id"`: `str`
* `"country"`: `str`
* `"category"`: `str`
* `"amount"`: `float` (dibulatkan ke 2 angka di belakang koma)

---

## 2. `build_user_profiles(cleaned_logs)`

Mengelompokkan daftar log transaksi bersih menjadi profil aktivitas masing-masing pengguna.

### Validasi Parameter
* `cleaned_logs` wajib bertipe `list`. Jika bukan, picu `TypeError`.

### Logika Pengelompokan
Buat sebuah `dict` utama di mana setiap kuncinya adalah string `user_id`, dan nilainya adalah sebuah `dict` profil dengan 5 kunci berikut:
* `"total_spent"`: Total akumulasi `amount` (`float`, dibulatkan 2 angka desimal) dari transaksi pengguna berkategori `"transfer"` atau `"withdrawal"`. Bernilai `0.0` jika belum ada pengeluaran.
* `"tx_count"`: Total seluruh log aktivitas yang tercatat milik pengguna tersebut (`int`).
* `"failed_logins"`: Jumlah aktivitas milik pengguna tersebut yang berkategori `"login_fail"` (`int`).
* `"countries"`: Sebuah `set` berisi kumpulan kode negara unik tempat pengguna pernah tercatat beraktivitas.
* `"max_single_tx"`: Nilai `amount` terbesar (`float`, dibulatkan 2 angka desimal) dari satu transaksi tunggal yang pernah dilakukan pengguna.

### Nilai Kembalian
Sebuah `dict` bersarang yang memetakan setiap `user_id` ke `dict` profilnya.

---

## 3. `evaluate_risk_scores(user_profiles, high_value_limit)`

Menghitung skor ancaman dan mengklasifikasikan tingkat risiko setiap pengguna berdasarkan profil aktivitas mereka.

### Validasi Parameter
* `user_profiles` wajib bertipe `dict`. Jika bukan, picu `TypeError`.
* `high_value_limit` wajib bertipe `int` atau `float` (tolak tipe `bool` dengan `TypeError`), dan nilainya harus **> 0** (jika $\le 0$, picu `ValueError`).

### Aturan Perhitungan Skor Risiko
Skor dimulai dari `0` untuk setiap pengguna:
1. **Aktivitas Lintas Negara:** Jika jumlah negara unik di dalam `"countries"` lebih dari 2, tambahkan **30 poin**.
2. **Rentetan Gagal Login:** Tambahkan **15 poin** untuk setiap 1 kejadian pada `"failed_logins"` (dikalikan jumlah kegagalan).
3. **Transaksi Tunggal Ekstrem:** Jika `"max_single_tx"` $\ge$ `high_value_limit`, tambahkan **40 poin**.
4. **Total Pengeluaran Masif:** Jika `"total_spent"` $\ge 2 \times \text{high\_value\_limit}$, tambahkan **25 poin**.

> **Batas Maksimal Skor:** Skor akhir tidak boleh melebihi 100. Jika hasil penjumlahan melebihi 100, kunci skor di angka **100**.

### Aturan Label Level Risiko (`level`)
* **75 – 100:** `"CRITICAL"`
* **40 – 74:** `"HIGH"`
* **1 – 39:** `"LOW"`
* **0:** `"SAFE"`

### Nilai Kembalian
Sebuah `dict` baru yang memetakan setiap `user_id` ke `dict` evaluasi dengan 4 kunci:
* `"score"`: `int`
* `"level"`: `str`
* `"total_spent"`: `float` (diambil dari profil pengguna)
* `"country_count"`: `int` (jumlah negara unik pengguna tersebut)

---

## 4. `get_priority_watchlist(risk_report, min_score=40)`

Menyaring dan mengurutkan daftar pengguna berisiko ke dalam daftar pantauan prioritas.

### Validasi Parameter
* `risk_report` wajib bertipe `dict`. Jika bukan, picu `TypeError`.
* `min_score` wajib bertipe `int` murni (tolak `float` dan `bool` dengan `TypeError`), dan nilainya harus berada pada rentang **0 sampai 100 inklusif** (jika di luar rentang, picu `ValueError`).

### Logika Penyaringan & Pengurutan
* **Penyaringan:** Saring hanya pengguna yang memiliki `"score"` $\ge$ `min_score`.
* **Pengurutan (Sort):** Urutkan pengguna yang lolos berdasarkan 3 kriteria prioritas:
  1. **Kriteria 1:** `"score"` tertinggi ke terendah (*descending*).
  2. **Kriteria 2 (Tie-breaker 1):** `"total_spent"` tertinggi ke terendah (*descending*).
  3. **Kriteria 3 (Tie-breaker 2):** `user_id` secara alfabetis dari A ke Z (*ascending*).

### Nilai Kembalian
Sebuah `list` berisi `tuple` dengan format 3 elemen:  
`[(user_id, score, level), ...]`

---

## Contoh Skenario Data & Output Ekspektasi

### Input Log Mentah
```python
raw_logs = [
    " TX-1001 | USR-02 | id | TRANSFER | 500.00 ",
    " TX-1002 | USR-02 | sg | WITHDRAWAL | 600.00 ",
    " TX-1003 | USR-02 | my | LOGIN_FAIL | 0 ",
    " TX-1004 | USR-01 | id | TRANSFER | 1100.00 ",
    " TX-1005 | USR-01 | id | LOGIN_FAIL | 0 ",
    " TX-9999 | USR-01 | id | TRANSFER | -50.00 ",     # Ditolak: nominal negatif
    " TX-12   | USR-03 | us | TRANSFER | 100.00 ",     # Ditolak: digit TX kurang dari 4
    " TX-1006 | USR-03 | u1 | TRANSFER | 100.00 "      # Ditolak: kode negara mengandung angka
]
```

### 1. Output `parse_transaction_logs`
```python
[
    {'tx_id': 'TX-1001', 'user_id': 'USR-02', 'country': 'ID', 'category': 'transfer', 'amount': 500.0},
    {'tx_id': 'TX-1002', 'user_id': 'USR-02', 'country': 'SG', 'category': 'withdrawal', 'amount': 600.0},
    {'tx_id': 'TX-1003', 'user_id': 'USR-02', 'country': 'MY', 'category': 'login_fail', 'amount': 0.0},
    {'tx_id': 'TX-1004', 'user_id': 'USR-01', 'country': 'ID', 'category': 'transfer', 'amount': 1100.0},
    {'tx_id': 'TX-1005', 'user_id': 'USR-01', 'country': 'ID', 'category': 'login_fail', 'amount': 0.0}
]
```

### 2. Output `build_user_profiles`
```python
{
    'USR-02': {
        'total_spent': 1100.0,
        'tx_count': 3,
        'failed_logins': 1,
        'countries': {'ID', 'SG', 'MY'},
        'max_single_tx': 600.0
    },
    'USR-01': {
        'total_spent': 1100.0,
        'tx_count': 2,
        'failed_logins': 1,
        'countries': {'ID'},
        'max_single_tx': 1100.0
    }
}
```

### 3. Output `evaluate_risk_scores` (`high_value_limit = 500.0`)
```python
{
    'USR-02': {'score': 100, 'level': 'CRITICAL', 'total_spent': 1100.0, 'country_count': 3},
    'USR-01': {'score': 80, 'level': 'CRITICAL', 'total_spent': 1100.0, 'country_count': 1}
}
```

### 4. Output `get_priority_watchlist` (`min_score = 40`)
```python
[
    ('USR-02', 100, 'CRITICAL'),
    ('USR-01', 80, 'CRITICAL')
]
```
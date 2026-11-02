# Laporan Analisis End-to-End: Jadwal & Tarif Kereta Api KAI (Pasar Senen ke 22 Stasiun Tujuan)

**Penulis:** Tim Data Analyst  
**Dataset:** `Data KAI PSE-YKLPN.csv` (1.854 baris, 15 kolom)  
**Lingkup Analisis:** Keberangkatan Stasiun Pasar Senen (PSE) menuju koridor lintas Jawa (hingga Yogyakarta / Lempuyangan)

---

## 1. Tujuan Analisis
Tujuan dari analisis data ini adalah:
1. Melakukan pembersihan data (*data cleaning*) dan penyeragaman format pada dataset operasional jadwal dan tarif KAI.
2. Membedah struktur tarif tiket berdasarkan kelas (Ekonomi vs Eksekutif) dan mengisolasi skema subsidi PSO (*Public Service Obligation*).
3. Mengevaluasi korelasi durasi perjalanan (sebagai proxy jarak tempuh) dan jumlah pemberhentian stasiun terhadap pembentukan harga tiket.
4. Menganalisis pola operasional sebaran waktu keberangkatan dan mengidentifikasi kereta-kereta dengan intensitas layanan tertinggi.
5. Menemukan anomali tarif dan inefisiensi harga per satuan waktu perjalanan antarkota.

---

## 2. Ringkasan Data
Dataset memuat 1.854 entri jadwal perjalanan dan tarif resmi PT Kereta Api Indonesia (KAI) dengan rincian:
- **Stasiun Asal:** 1 stasiun tunggal, yaitu **Pasar Senen (PSE)**.
- **Stasiun Tujuan:** 22 stasiun tujuan di koridor Jawa Barat, Jawa Tengah, hingga D.I. Yogyakarta.
- **Kereta Unik:** 31 nama komersial kereta api (mencakup 35 nomor/kode unik KA, misal Serayu 284B dan 288).
- **Komposisi Kelas Layanan:**
  - **Ekonomi:** 1.046 entri (56,42%)
    - *Ekonomi Komersial:* 1.012 entri (54,58%)
    - *Ekonomi Subsidi PSO:* 34 entri (1,83%)
  - **Eksekutif:** 808 entri (43,58%)
- **Jenis Rangkaian:** Terdiri atas 11 tipe sarana kereta, didominasi oleh *New Generation Stainless Steel* (508 jadwal), *Premium Modifikasi Mild Steel* (356 jadwal), dan *Eksekutif Mild Steel* (352 jadwal).

---

## 3. Dokumentasi Langkah Data Cleaning
Pembersihan data dilakukan secara ketat dengan tahapan berikut:
1. **Parsing Data Mentah & Penanganan Teks Ribuan:**
   - Kolom `Harga (Rp)` pada file asli berformat teks bertitik ribuan (contoh: `"340.000"`).
   - Tanda titik dihilangkan menggunakan regex/string replacement dan dikonversi menjadi integer murni `int64` (contoh: `340000`). Hal ini mencegah kesalahan umum di mana pandas menginterpretasikan titik sebagai tanda desimal.
2. **Transformasi Waktu & Kategorisasi Periode:**
   - Kolom `Jam Berangkat` dan `Jam Sampai` diuraikan menjadi tipe waktu.
   - Dibuat kolom `jam_berangkat_jam` (integer 0–23) dan kolom kategorikal `waktu_keberangkatan`:
     - *Dini hari:* 00:00 – 04:59
     - *Pagi:* 05:00 – 10:59
     - *Siang:* 11:00 – 14:59
     - *Sore:* 15:00 – 18:59
     - *Malam:* 19:00 – 23:59
3. **Standarisasi Penamaan Kolom (snake_case):**
   - Seluruh nama kolom diubah menjadi huruf kecil dengan garis bawah, seperti: `stasiun_tujuan`, `kode_stasiun_tujuan`, `durasi_menit`, `harga_rp`, `jumlah_stasiun_pemberhentian`.
4. **Verifikasi Integritas Data & Konsistensi:**
   - *Missing Value:* 0 nilai hilang (data 100% lengkap pada seluruh kolom).
   - *Duplikasi Baris:* 0 duplikat baris persis.
   - *Konsistensi Durasi:* Validasi selisih antara `Jam Berangkat` dan `Jam Sampai` (memperhitungkan pergantian hari / lewat tengah malam) dibandingkan langsung dengan kolom `Durasi (menit)`. Hasilnya **100% konsisten (0 anomali perhitungan waktu)**.
5. **Pembuatan Fitur Turunan:**
   - `harga_per_menit`: Dihitung dari `harga_rp / durasi_menit` (dibulatkan 2 desimal) sebagai indikator efisiensi tarif per satuan waktu perjalanan.
   - `kategori_kelas_detail`: Memisahkan tarif subsidi pemerintah PSO (Kode Kelas `"C"`, sarana *Mild Steel PSO* seperti KA Bengawan, Airlangga, Serayu, Cikuray) dari Ekonomi Komersial reguler dan Eksekutif.
6. **Perlakuan Khusus Subkelas Tiket (Yield Management):**
   - Satu nama KA memiliki beberapa Kode Kelas / Subkelas (seperti CA–CD pada Ekonomi, AA–AD pada Eksekutif). Subkelas ini mencerminkan struktur kuota harga dinamis (*dynamic pricing*) KAI dan **tidak dihapus**, melainkan dipertahankan untuk mencerminkan variasi tarif riil yang dihadapi calon penumpang.

---

## 4. Temuan Utama (Key Findings)

### 1. Disparitas Tarif Ekstrem: Subsidi PSO vs Komersial
- Tarif Ekonomi Subsidi PSO dipatok flat sangat murah: **Rp 45.000** (KA Cikuray PSE-Cikampek/Karawang) hingga **Rp 74.000** (KA Bengawan rute jauh PSE-Kutoarjo/Wates), dengan rata-rata **Rp 62.000** dan median **Rp 63.000**.
- Sebaliknya, Ekonomi Komersial beroperasi pada rentang **Rp 105.000 s.d. Rp 450.000** (rata-rata **Rp 302.923**, median **Rp 290.000**).
- Kelas Eksekutif berada di rentang **Rp 155.000 s.d. Rp 675.000** (rata-rata **Rp 446.708**, median **Rp 435.000**). Pemisahan label PSO krusial agar tidak membias rata-rata tarif pasar kelas ekonomi.

### 2. Anomali Tarif Jarak Pendek (*Minimum Fare Barrier*)
- Tarif per menit perjalanan tertinggi ditemukan pada stasiun-stasiun terdekat dari Pasar Senen:
  - **Jatinegara (JNG, durasi ~10 mnt):** Rata-rata tarif per menit **Rp 29.977/menit** (maksimum mencapai **Rp 50.000/menit**).
  - **Bekasi (BKS, durasi ~25 mnt):** Rata-rata tarif per menit **Rp 12.616/menit**.
- Hal ini terjadi karena KAI menetapkan batas tarif minimum tiket KA antarkota komersial (minimum tiket Rp 150.000–Rp 450.000), meskipun penumpang turun di stasiun pemberhentian pertama yang berjarak sangat dekat.
- Sebaliknya, rute jarak jauh sangat efisien dari perspektif waktu: **Lempuyangan (Rp 932/menit)** dan **Yogyakarta (Rp 1.078/menit)**.

### 3. Korelasi Jarak/Durasi terhadap Tarif
- Pada kategori Ekonomi Komersial, korelasi durasi perjalanan dengan harga tiket bernilai positif kuat (**r = 0,7043**), dan pada Eksekutif (**r = 0,6902**).
- Korelasi pada kategori PSO lebih moderat (**r = 0,5052**) karena adanya batasan pagu tarif subsidi pemerintah yang bersifat flat per zona trayek.

### 4. Ilusi Hubungan Jumlah Pemberhentian vs Durasi (*Confounding Factor*)
- Secara keseluruhan (global), jumlah stasiun pemberhentian berkorelasi sangat tinggi dengan durasi perjalanan (**r = 0,9218**).
- **Namun, ini merupakan variabel pengacau (*confounding factor*) jarak:** stasiun yang lebih jauh secara alami melewati lebih banyak perhentian.
- Ketika dianalisis pada stasiun tujuan yang sama (jarak dikontrol), korelasi tersebut turun drastis:
  - PSE ke Yogyakarta: **r = 0,2911**
  - PSE ke Purwokerto: **r = 0,1199**
  - PSE ke Lempuyangan: **r = 0,0986**
- Artinya, untuk tujuan yang sama, KA dengan pemberhentian lebih banyak tidak serta-merta memiliki waktu tempuh yang jauh lebih lambat; faktor prioritas persilangan jalur dan tipe lokomotif/rangkaian lebih menentukan durasi akhir.

### 5. Pola Keberangkatan Terkonsentrasi pada Malam & Pagi
- Distribusi jadwal keberangkatan dari Pasar Senen:
  - **Malam (19:00 – 23:59):** 614 jadwal (**33,12%**) — waktu paling favorit untuk perjalanan jarak jauh tiba pagi di Jawa Tengah/Yogyakarta. Didominasi oleh KA Singasari (120 jadwal), Mataram (104 jadwal), dan Senja Utama YK (96 jadwal).
  - **Pagi (05:00 – 10:59):** 528 jadwal (**28,48%**). Didominasi oleh Gajahwong (112 jadwal), Fajar Utama YK (112 jadwal), dan Fajar Utama Solo (96 jadwal).
  - **Siang (11:00 – 14:59):** 456 jadwal (**24,59%**). Didominasi Gaya Baru Malam Selatan (128 jadwal).
  - **Sore (15:00 – 18:59):** 256 jadwal (**13,81%**). Didominasi Bogowonto (120 jadwal).
  - **Dini Hari (00:00 – 04:59):** 0 jadwal (**0,00%**). Tidak ada keberangkatan KA antarkota PSE pada waktu ini demi efisiensi operasional dan waktu istirahat stasiun.

### 6. Kereta Api Paling Aktif & Variasi Sarana
- **10 Kereta dengan Layanan Terbanyak:**
  1. **KA SAWUNGGALIH:** 192 jadwal (Rata-rata tarif Rp 300.859, durasi rata-rata 215,8 menit). Memimpin karena memiliki jadwal ganda (pagi & malam) serta membawa kelas campuran Eksekutif dan Ekonomi.
  2. **GAYA BARU MALAM SELATAN:** 128 jadwal (Rata-rata Rp 390.312, durasi 255,4 menit).
  3. **SINGASARI:** 120 jadwal (Rata-rata Rp 413.833, durasi 234,1 menit).
  4. **BOGOWONTO:** 120 jadwal (Rata-rata Rp 439.167, durasi 267,1 menit).
  5. **GAJAHWONG:** 112 jadwal (Rata-rata Rp 417.679, durasi 284,4 menit).
  6. **FAJAR UTAMA YK:** 112 jadwal (Rata-rata Rp 406.964, durasi 253,7 menit).
  7. **MATARAM:** 104 jadwal (Rata-rata Rp 455.385, durasi 234,3 menit).
  8. **FAJAR UTAMA SOLO:** 96 jadwal (Rata-rata Rp 447.083, durasi 214,9 menit).
  9. **SENJA UTAMA YK:** 96 jadwal (Rata-rata Rp 408.542, durasi 250,6 menit).
  10. **BANGUNKARTA:** 80 jadwal (Rata-rata Rp 359.000, durasi 244,0 menit).
- **Stasiun Tujuan Terbanyak Dilayani:** Bekasi (201 jadwal), Cirebon (128 jadwal), Jatibarang (125 jadwal), Purwokerto (123 jadwal), dan Kroya (123 jadwal).
- **Stasiun Tujuan Paling Sedikit Dilayani:** Ketanggungan (12 jadwal), Ciledug (16 jadwal), Cikampek (24 jadwal), Kutowinangun (24 jadwal), dan Prupuk (25 jadwal).

---

## 5. Keterbatasan Data (Data Limitations)
1. **Tidak Ada Dimensi Transaksi & Okupansi:** Dataset hanya memuat jadwal reguler dan pagu tarif (*tariff table*), bukan transaksi tiket harian. Oleh karena itu, analisis ini tidak mencerminkan tingkat keterisian kursi (*load factor*), jumlah penumpang riil, maupun pendapatan penjualan (*revenue*).
2. **Tidak Ada Variabel Tanggal Kalender:** Data tidak membedakan tarif hari kerja (*weekday*), akhir pekan (*weekend*), maupun musim puncak (*peak season/Lebaran/Nataru*).
3. **Ketiadaan Data Jarak Riil (Kilometer Rel):** Analisis mengandalkan `Durasi (menit)` sebagai proksi jarak, di mana durasi dipengaruhi oleh faktor kecepatan teknis lokomotif, kelandaian jalur, dan antrean persilangan stasiun.

---

## 6. Saran Analisis Lanjutan
1. **Integrasi Data Transaksi & Okupansi (Load Factor):** Menghubungkan tarif subkelas (CA-CD, AA-AD) dengan data transaksi riil untuk melihat sensitivitas elastisitas harga (*price elasticity of demand*) penumpang kereta api.
2. **Optimasi Struktur Tarif Jarak Pendek (*Short-Haul Pricing Strategy*):** Meninjau ulang tarif minimum stasiun dekat (PSE-JNG/BKS) guna melihat potensi kanibalisasi atau komplementaritas terhadap layanan KRL Commuter Line.
3. **Analisis Efisiensi Waktu Tempuh (*Bottleneck Detection*):** Menggabungkan data jarak kilometer fisik rel dan grafik perjalanan kereta api (Gapeka) untuk mengukur kecepatan rata-rata efektif per koridor (misal lintas Cirebon vs Purwokerto-Kroya).

---
*Laporan ini disusun secara otomatis dan didukung oleh analisis komputasi Python pada notebook `analisis_kai.ipynb` serta visualisasi grafik beresolusi tinggi pada folder `output/grafik/`.*

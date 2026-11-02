# Analisis Jadwal & Tarif Kereta Api KAI (Pasar Senen)

Repositori ini memuat analisis data *end-to-end* (pembersihan data, eksplorasi statistik, visualisasi, dan dashboard analitik interaktif) pada dataset jadwal dan pagu tarif resmi PT Kereta Api Indonesia (Persero) untuk keberangkatan Stasiun Pasar Senen (PSE) menuju 22 stasiun tujuan koridor lintas Jawa.

---

## 📁 Struktur Direktori

```text
├── Data KAI PSE-YKLPN.csv          # Dataset mentah (1.854 baris, 15 kolom)
├── data_bersih.csv                 # Dataset hasil pembersihan (1.854 baris, 19 kolom)
├── analisis_kai.ipynb              # Jupyter Notebook komputasi & analisis lengkap
├── app_dashboard.py                # Dashboard analitik interaktif (Streamlit + Altair)
├── dashboard_interaktif.html       # Dashboard mandiri offline (HTML5 + Chart.js)
├── laporan_analisis.md             # Laporan temuan analitik formal berbahasa Indonesia
├── requirements.txt                # Dependensi pustaka Python
├── .gitignore                      # Berkas pengabaian Git
├── .streamlit/
│   └── config.toml                 # Konfigurasi tema resmi Streamlit (Light Mode)
└── output/
    └── grafik/                     # 9 visualisasi grafis resolusi tinggi (300 DPI)
        ├── 01_sebaran_kelas_dan_pso.png
        ├── 02_distribusi_harga_per_kelas.png
        ├── 03_rata_rata_harga_stasiun_tujuan.png
        ├── 04_scatter_durasi_vs_harga.png
        ├── 05_harga_per_menit_stasiun.png
        ├── 06_pemberhentian_vs_durasi.png
        ├── 07_distribusi_waktu_keberangkatan.png
        ├── 08_top10_kereta_layanan_terbanyak.png
        └── 09_harga_jenis_rangkaian.png
```

---

## 🔍 Temuan Utama Analisis

1. **Disparitas Tarif Subsidi PSO vs Komersial:**
   - **Ekonomi PSO (Subsidi Pemerintah):** Tarif flat antara **Rp 45.000 s.d. Rp 74.000** (rata-rata Rp 62.000) pada KA Bengawan, Airlangga, Serayu, dan Cikuray.
   - **Ekonomi Komersial:** Bergerak dinamis antara **Rp 105.000 s.d. Rp 450.000** (rata-rata Rp 302.923).
   - **Eksekutif:** Bergerak antara **Rp 155.000 s.d. Rp 675.000** (rata-rata Rp 446.708).

2. **Anomali Tarif Jarak Pendek (*Minimum Fare Barrier*):**
   - Stasiun terdekat dari Pasar Senen memiliki rasio tarif per menit perjalanan tertinggi: **Jatinegara (Rp 29.977/menit)** dan **Bekasi (Rp 12.616/menit)**.
   - Hal ini disebabkan oleh penerapan batas tarif bawah tiket kereta antarkota komersial.

3. **Confounding Variable pada Durasi Perjalanan (*Simpson's Paradox*):**
   - Secara keseluruhan, korelasi jumlah pemberhentian terhadap durasi perjalanan bernilai tinggi ($r = 0,9218$).
   - Namun ketika diuji pada stasiun tujuan yang sama, korelasi turun tajam ($r = 0,0986$ s.d. $0,2911$), membuktikan bahwa durasi akhir lebih dipengaruhi oleh persilangan jalur dan prioritas operasi daripada semata jumlah perhentian.

4. **Konsentrasi Jadwal Operasional:**
   - Keberangkatan didominasi pada **Malam hari (33,1%)** dan **Pagi hari (28,5%)**.
   - Tidak ada jadwal keberangkatan kereta antarkota pada periode dini hari (00:00 - 04:59).

---

## 🚀 Panduan Menjalankan Proyek

### 1. Prasyarat Lingkungan
Pastikan Python 3.10+ telah terpasang. Pasang pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Dashboard Streamlit
```bash
streamlit run app_dashboard.py
```
Akses dashboard melalui peramban web pada alamat `http://localhost:8501`.

### 3. Membuka Dashboard Mandiri (Offline)
Buka berkas `dashboard_interaktif.html` langsung dengan klik dua kali di peramban web Anda tanpa memerlukan server.

### 4. Menjalankan Jupyter Notebook
```bash
jupyter notebook analisis_kai.ipynb
```

---

## 🔒 Catatan Keamanan Git
Dataset dalam repositori ini merupakan jadwal dan tarif operasional publik. Tidak memuat data pribadi penumpang (*Personally Identifiable Information*), data transaksi keuangan, kunci API, maupun token rahasia. Repositori ini aman untuk diunggah (*push*) ke GitHub.


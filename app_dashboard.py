import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import altair as alt
import os

# ─────────────────────────────────────────────────────────────────────────────
# 1. KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis Tarif & Jadwal KAI PSE",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Skrip Otomatis Pembuka Sidebar jika sebelumnya terminimalkan di browser
components.html("""
<script>
function autoExpandSidebar() {
    try {
        const doc = window.parent.document;
        const expandBtn = doc.querySelector('[data-testid="stExpandSidebarButton"] button, [data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"]');
        if (expandBtn) {
            expandBtn.click();
        }
    } catch (e) {}
}
setTimeout(autoExpandSidebar, 80);
setTimeout(autoExpandSidebar, 350);
setTimeout(autoExpandSidebar, 800);
</script>
""", height=0, width=0)

# ─────────────────────────────────────────────────────────────────────────────
# 2. DESAIN ANTARMUKA ENTERPRISE (Minimalis, Serius, Bebas Ornamen Berlebih)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #1E293B;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 1360px !important;
}

/* Sembunyikan elemen dekoratif default TANPA menghilangkan tombol collapse/expand */
/* Sembunyikan elemen dekoratif default */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDecoration"] { visibility: hidden; }
[data-testid="stStatusWidget"] { visibility: hidden; }

/* Header & Toolbar: Pastikan tombol buka sidebar SELALU terlihat */
header[data-testid="stHeader"] {
    background: transparent !important;
    z-index: 99999 !important;
}

[data-testid="stToolbar"] {
    visibility: visible !important;
    background: transparent !important;
}

[data-testid="stToolbarActions"] {
    display: none !important;
}

/* Pastikan tombol buka sidebar (saat diminimize) selalu tampak jelas & bisa diklik */
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    width: 38px !important;
    height: 38px !important;
    color: #0F172A !important;
    background: #FFFFFF !important;
    border: 1.5px solid #2563EB !important;
    border-radius: 6px !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
    cursor: pointer !important;
    z-index: 9999999 !important;
}
[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stSidebarCollapsedControl"]:hover {
    background: #EFF6FF !important;
    border-color: #1D4ED8 !important;
}
[data-testid="stExpandSidebarButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg {
    fill: #2563EB !important;
    stroke: #2563EB !important;
    width: 22px !important;
    height: 22px !important;
}

/* Sembunyikan tombol tutup sidebar di dalam panel agar menu selalu tetap terbuka di kiri */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* Sidebar styling bersih & profesional */
section[data-testid="stSidebar"] {
    background-color: #F8FAFC !important;
    border-right: 1px solid #E2E8F0 !important;
}

/* Header Halaman */
.header-container {
    padding-bottom: 1rem;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}
.header-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.01em;
    margin: 0;
}
.header-sub {
    font-size: 0.82rem;
    color: #64748B;
    margin-top: 4px;
}
.header-meta {
    font-size: 0.78rem;
    color: #475569;
    font-weight: 500;
    text-align: right;
}

/* Kartu Metrik (Minimalis Modern) */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
    margin-bottom: 1.8rem;
}
.metric-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 14px 16px;
}
.metric-tile-label {
    font-size: 0.70rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}
.metric-tile-value {
    font-size: 1.28rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.2;
}
.metric-tile-sub {
    font-size: 0.72rem;
    color: #64748B;
    margin-top: 4px;
}

/* Panel Visualisasi */
.panel-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 18px 20px 14px;
    margin-bottom: 16px;
}
.panel-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #0F172A;
    margin-bottom: 2px;
}
.panel-desc {
    font-size: 0.76rem;
    color: #64748B;
    margin-bottom: 14px;
}

/* Catatan Analisis Konseptual */
.note-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 3px solid #3B82F6;
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 0.80rem;
    color: #334155;
    line-height: 1.55;
    margin-top: 12px;
    margin-bottom: 6px;
}

/* Header Seksi */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding-bottom: 6px;
    border-bottom: 1px solid #E2E8F0;
    margin: 18px 0 12px 0;
}

/* Sidebar */
.sidebar-heading {
    font-size: 0.88rem;
    font-weight: 700;
    color: #0F172A;
    padding-bottom: 10px;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 16px;
}

/* Download Buttons */
.stDownloadButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 500 !important;
    font-size: 0.80rem !important;
    padding: 6px 14px !important;
}
.stDownloadButton > button:hover {
    background-color: #1D4ED8 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. FUNGSI PEMFORMATAN DATA
# ─────────────────────────────────────────────────────────────────────────────
def format_rupiah(val):
    if pd.isna(val): return "–"
    return "Rp " + f"{int(val):,}".replace(",", ".")

def format_durasi(menit):
    if pd.isna(menit): return "–"
    m = int(menit)
    return f"{m//60}j {m%60}m"

# ─────────────────────────────────────────────────────────────────────────────
# 4. MEMUAT DATASET
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_clean_data():
    search_paths = [
        os.path.join(os.path.dirname(__file__), "data_bersih.csv"),
        r"D:\dtkai\data_bersih.csv",
        "data_bersih.csv"
    ]
    for p in search_paths:
        if os.path.exists(p):
            df = pd.read_csv(p, sep=";", encoding="utf-8-sig")
            num_cols = ["harga_rp", "durasi_menit", "harga_per_menit",
                        "jumlah_stasiun_pemberhentian", "jam_berangkat_jam"]
            for col in num_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            return df
    st.error("File data_bersih.csv tidak ditemukan.")
    st.stop()

DF_RAW = load_clean_data()

# Palet Warna Data Formal
KELAS_DOMAIN = ["Ekonomi (Komersial)", "Eksekutif", "Ekonomi (PSO)"]
KELAS_RANGE  = ["#2563EB", "#D97706", "#059669"]  # Biru, Amber, Hijau

def configure_altair_theme():
    return {
        "config": {
            "font": "Inter, sans-serif",
            "background": "#FFFFFF",
            "view": {"stroke": "transparent", "fill": "#FFFFFF"},
            "axis": {
                "labelFont": "Inter",
                "titleFont": "Inter",
                "labelFontSize": 11,
                "titleFontSize": 11,
                "titleFontWeight": 600,
                "labelColor": "#475569",
                "titleColor": "#1E293B",
                "gridColor": "#F1F5F9",
                "gridOpacity": 1,
                "domainColor": "#CBD5E1",
                "tickColor": "#CBD5E1",
            },
            "legend": {
                "labelFont": "Inter",
                "titleFont": "Inter",
                "labelFontSize": 11,
                "titleFontSize": 11,
                "titleFontWeight": 600,
                "labelColor": "#334155",
                "titleColor": "#0F172A",
                "symbolSize": 100,
            },
            "title": {
                "font": "Inter",
                "fontSize": 12.5,
                "fontWeight": 600,
                "color": "#0F172A",
                "anchor": "start",
            }
        }
    }

alt.themes.register("kai_formal", configure_altair_theme)
alt.themes.enable("kai_formal")

# ─────────────────────────────────────────────────────────────────────────────
# 5. SIDEBAR: MENU PILIHAN & FILTER (SISI KIRI)
# ─────────────────────────────────────────────────────────────────────────────
opt_kereta = sorted(DF_RAW["nama_kereta"].dropna().unique().tolist())
opt_kelas = sorted(DF_RAW["kategori_kelas_detail"].dropna().unique().tolist())
order_waktu = ["Pagi", "Siang", "Sore", "Malam", "Dini hari"]
opt_waktu = [w for w in order_waktu if w in DF_RAW["waktu_keberangkatan"].unique()]
opt_tujuan = sorted(DF_RAW["stasiun_tujuan"].dropna().unique().tolist())
min_val, max_val = int(DF_RAW.harga_rp.min()), int(DF_RAW.harga_rp.max())

with st.sidebar:
    st.markdown("""
    <div style="padding-bottom:12px; margin-bottom:16px; border-bottom:1px solid #E2E8F0;">
        <div style="font-size:0.95rem; font-weight:700; color:#0F172A;">Menu Pilihan & Filter</div>
        <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">Parameter Analisis Kereta Api PSE</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Menu Pilihan Kereta Api Utama
    pilihan_kereta = st.selectbox(
        "Pilihan Kereta Api",
        options=["Semua Kereta Api (31 KA)"] + opt_kereta,
        index=0,
        help="Pilih salah satu armada kereta api untuk memfilter seluruh visualisasi atau tampilkan semua armada."
    )

    # 2. Kategori Layanan
    sel_kelas = st.multiselect(
        "Kategori Layanan",
        options=opt_kelas,
        default=opt_kelas,
        help="Filter kelas komersial atau subsidi PSO."
    )

    # 3. Waktu Keberangkatan
    sel_waktu = st.multiselect(
        "Waktu Keberangkatan",
        options=opt_waktu,
        default=opt_waktu,
        help="Filter periode waktu keberangkatan dari Pasar Senen."
    )

    # 4. Stasiun Tujuan
    sel_tujuan = st.multiselect(
        "Stasiun Tujuan",
        options=opt_tujuan,
        default=opt_tujuan,
        help="Filter stasiun tujuan di koridor Jawa."
    )

    # 5. Rentang Tarif Tiket
    sel_harga = st.slider(
        "Rentang Tarif (Rp)",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val),
        step=5000,
        format="Rp %d"
    )

    st.markdown(f"""
    <div style="font-size:0.75rem; color:#475569; background:#FFFFFF; border:1px solid #CBD5E1; border-radius:4px; padding:6px 10px; margin-top:6px; margin-bottom:12px;">
        Tarif: <strong style="color:#0F172A;">{format_rupiah(sel_harga[0])}</strong> – <strong style="color:#0F172A;">{format_rupiah(sel_harga[1])}</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:16px 0; border:0; border-top:1px solid #E2E8F0;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.75rem; color:#64748B; line-height:1.55;">
        <strong style="color:#0F172A;">Stasiun Keberangkatan:</strong><br>
        Pasar Senen (PSE), Jakarta Pusat<br><br>
        <strong style="color:#0F172A;">Cakupan Basis Data:</strong><br>
        1.854 Jadwal &bull; 31 Nama KA &bull; 22 Tujuan
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 6. PENYARINGAN DATASET
# ─────────────────────────────────────────────────────────────────────────────
df = DF_RAW[
    DF_RAW.kategori_kelas_detail.isin(sel_kelas) &
    DF_RAW.waktu_keberangkatan.isin(sel_waktu) &
    DF_RAW.stasiun_tujuan.isin(sel_tujuan) &
    DF_RAW.harga_rp.between(sel_harga[0], sel_harga[1])
].copy()

if pilihan_kereta != "Semua Kereta Api (31 KA)":
    df = df[df.nama_kereta == pilihan_kereta]

# ─────────────────────────────────────────────────────────────────────────────
# 7. HEADER HALAMAN UTAMA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="header-title">Analisis Jadwal & Tarif Kereta Api</h1>
        <div class="header-sub">Keberangkatan Stasiun Pasar Senen (PSE) menuju 22 Stasiun Tujuan Koridor Lintas Jawa</div>
    </div>
    <div class="header-meta">
        Dataset: 1.854 Jadwal Terdaftar<br>
        Sumber: Jadwal & Pagu Tarif Resmi KAI
    </div>
</div>
""", unsafe_allow_html=True)

if len(df) == 0:
    st.warning("Tidak ada jadwal yang memenuhi kombinasi kriteria filter saat ini. Silakan sesuaikan kembali pilihan kereta api, kelas, atau rentang tarif pada menu di samping kiri.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 8. METRIK UTAMA
# ─────────────────────────────────────────────────────────────────────────────
n_filtered = len(df)
pct_filter = (n_filtered / len(DF_RAW)) * 100
mean_p = df.harga_rp.mean()
med_p  = df.harga_rp.median()
mean_d = df.durasi_menit.mean()
mean_m = df.harga_per_menit.mean()
n_dest = df.stasiun_tujuan.nunique()
n_ka   = df.nama_kereta.nunique()

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-tile">
        <div class="metric-tile-label">Total Jadwal</div>
        <div class="metric-tile-value">{n_filtered:,}</div>
        <div class="metric-tile-sub">{pct_filter:.0f}% dari total data</div>
    </div>
    <div class="metric-tile">
        <div class="metric-tile-label">Rata-Rata Tarif</div>
        <div class="metric-tile-value">{format_rupiah(mean_p)}</div>
        <div class="metric-tile-sub">Median: {format_rupiah(med_p)}</div>
    </div>
    <div class="metric-tile">
        <div class="metric-tile-label">Rentang Tarif</div>
        <div class="metric-tile-value">{format_rupiah(df.harga_rp.min())}</div>
        <div class="metric-tile-sub">Maks: {format_rupiah(df.harga_rp.max())}</div>
    </div>
    <div class="metric-tile">
        <div class="metric-tile-label">Rata-Rata Durasi</div>
        <div class="metric-tile-value">{format_durasi(mean_d)}</div>
        <div class="metric-tile-sub">{int(mean_d)} menit perjalanan</div>
    </div>
    <div class="metric-tile">
        <div class="metric-tile-label">Tarif per Menit</div>
        <div class="metric-tile-value">Rp {int(mean_m):,}/m</div>
        <div class="metric-tile-sub">Rasio waktu tempuh</div>
    </div>
    <div class="metric-tile">
        <div class="metric-tile-label">Cakupan Armada</div>
        <div class="metric-tile-value">{n_ka} KA</div>
        <div class="metric-tile-sub">{n_dest} stasiun tujuan</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 9. TABS VISUALISASI
# ─────────────────────────────────────────────────────────────────────────────
tab_tarif, tab_stasiun, tab_durasi, tab_operasional, tab_profil_ka, tab_data = st.tabs([
    "Distribusi Tarif",
    "Analisis Stasiun",
    "Durasi & Jarak",
    "Pola Keberangkatan",
    "Jadwal & Profil Kereta",
    "Tabel Data",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: DISTRIBUSI TARIF
# ─────────────────────────────────────────────────────────────────────────────
with tab_tarif:
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Sebaran Tarif per Kategori Kelas</div>
            <div class="panel-desc">Menampilkan batas minimum, Q1, median, Q3, dan maksimum per kelas layanan</div>
        """, unsafe_allow_html=True)

        chart_box = (
            alt.Chart(df)
            .mark_boxplot(
                extent="min-max",
                size=44,
                median=alt.MarkConfig(color="#0F172A", strokeWidth=2),
                outliers=alt.MarkConfig(size=20, opacity=0.4, filled=True)
            )
            .encode(
                x=alt.X("kategori_kelas_detail:N", sort=KELAS_DOMAIN, title=None,
                        axis=alt.Axis(labelAngle=0, labelFontWeight=500, labelColor="#334155")),
                y=alt.Y("harga_rp:Q", title="Harga Tiket (Rp)",
                        axis=alt.Axis(labelExpr="'Rp '+format(datum.value/1000,',.0f')+'k'")),
                color=alt.Color("kategori_kelas_detail:N",
                                scale=alt.Scale(domain=KELAS_DOMAIN, range=KELAS_RANGE), legend=None),
                tooltip=[
                    alt.Tooltip("kategori_kelas_detail:N", title="Kategori"),
                    alt.Tooltip("harga_rp:Q", format=",", title="Tarif (Rp)")
                ]
            )
            .properties(height=320)
        )
        st.altair_chart(chart_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Sebaran Titik Tarif Individual</div>
            <div class="panel-desc">Distribusi individual jadwal tarif (klik nama kelas di legenda untuk isolasi)</div>
        """, unsafe_allow_html=True)

        sel_point = alt.selection_point(fields=["kategori_kelas_detail"], bind="legend")
        chart_strip = (
            alt.Chart(df)
            .mark_circle(size=28)
            .transform_calculate(jitter="(random()-0.5)*0.44")
            .encode(
                x=alt.X("kategori_kelas_detail:N", sort=KELAS_DOMAIN, title=None,
                        axis=alt.Axis(labelAngle=0, labelFontWeight=500, labelColor="#334155")),
                xOffset="jitter:Q",
                y=alt.Y("harga_rp:Q", title="Harga Tiket (Rp)",
                        axis=alt.Axis(labelExpr="'Rp '+format(datum.value/1000,',.0f')+'k'")),
                color=alt.Color("kategori_kelas_detail:N",
                                scale=alt.Scale(domain=KELAS_DOMAIN, range=KELAS_RANGE),
                                legend=alt.Legend(title="Kategori Layanan", orient="bottom", direction="horizontal",
                                                  titleColor="#0F172A", labelColor="#334155")),
                opacity=alt.condition(sel_point, alt.value(0.60), alt.value(0.08)),
                tooltip=[
                    alt.Tooltip("nama_kereta:N",           title="Kereta Api"),
                    alt.Tooltip("stasiun_tujuan:N",        title="Stasiun Tujuan"),
                    alt.Tooltip("kategori_kelas_detail:N", title="Kategori"),
                    alt.Tooltip("harga_rp:Q",              title="Harga", format=","),
                    alt.Tooltip("jam_berangkat:N",         title="Waktu Berangkat"),
                ]
            )
            .add_params(sel_point)
            .properties(height=320)
        )
        st.altair_chart(chart_strip, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Statistik Deskriptif Tarif</div>', unsafe_allow_html=True)
    stats_table = (
        df.groupby("kategori_kelas_detail")["harga_rp"]
        .agg(Jumlah_Layanan="count", Minimum="min", Maksimum="max",
             Rata_Rata="mean", Median="median", Standar_Deviasi="std")
        .reset_index().rename(columns={"kategori_kelas_detail": "Kategori Layanan"})
    )
    for c in ["Minimum", "Maksimum", "Rata_Rata", "Median", "Standar_Deviasi"]:
        stats_table[c] = stats_table[c].apply(format_rupiah)
    st.dataframe(stats_table, use_container_width=True, hide_index=True)

    avg_eko = df[df.kategori_kelas_detail == "Ekonomi (Komersial)"]["harga_rp"].mean()
    avg_eks = df[df.kategori_kelas_detail == "Eksekutif"]["harga_rp"].mean()
    avg_pso = df[df.kategori_kelas_detail == "Ekonomi (PSO)"]["harga_rp"].mean()
    summary_notes = []
    if avg_eko: summary_notes.append(f"Ekonomi Komersial: rata-rata <b>{format_rupiah(avg_eko)}</b>")
    if avg_eks: summary_notes.append(f"Eksekutif: rata-rata <b>{format_rupiah(avg_eks)}</b>")
    if avg_pso: summary_notes.append(f"Subsidi PSO: rata-rata <b>{format_rupiah(avg_pso)}</b> (subsidi kewajiban pelayanan publik)")
    if avg_eko and avg_eks: summary_notes.append(f"Selisih rata-rata Eksekutif–Ekonomi: <b>{format_rupiah(avg_eks - avg_eko)}</b>")
    if summary_notes:
        st.markdown(f'<div class="note-box"><strong>Karakteristik Data Tarif:</strong> ' + ' &ensp;·&ensp; '.join(summary_notes) + '.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: ANALISIS STASIUN
# ─────────────────────────────────────────────────────────────────────────────
with tab_stasiun:
    col_a, col_b = st.columns([1.1, 0.9], gap="medium")

    with col_a:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Rata-Rata Tarif Berdasarkan Rute & Kelas</div>
            <div class="panel-desc">Perbandingan rata-rata tarif tiket per stasiun tujuan dan kelas layanan</div>
        """, unsafe_allow_html=True)

        hm_data = df.groupby(["stasiun_tujuan", "kelas"])["harga_rp"].mean().reset_index()
        hm_data.columns = ["Stasiun", "Kelas", "Tarif"]

        chart_hm = (
            alt.Chart(hm_data)
            .mark_rect(cornerRadius=2, stroke="#FFFFFF", strokeWidth=1)
            .encode(
                x=alt.X("Kelas:N", title="Kelas",
                        axis=alt.Axis(labelAngle=0, labelFontWeight=500, labelColor="#334155")),
                y=alt.Y("Stasiun:N", title="Stasiun Tujuan",
                        sort=alt.EncodingSortField("Tarif", op="mean", order="descending"),
                        axis=alt.Axis(labelColor="#334155", labelFontWeight=500)),
                color=alt.Color("Tarif:Q",
                                scale=alt.Scale(scheme="blues", zero=False),
                                legend=alt.Legend(title="Rata-Rata (Rp)", format=",", labelColor="#334155", titleColor="#0F172A")),
                tooltip=[
                    alt.Tooltip("Stasiun:N", title="Stasiun Tujuan"),
                    alt.Tooltip("Kelas:N",   title="Kelas"),
                    alt.Tooltip("Tarif:Q",   title="Rata-Rata Tarif", format=","),
                ]
            )
            .properties(height=max(300, df.stasiun_tujuan.nunique()*20))
        )
        st.altair_chart(chart_hm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Volume Jadwal Layanan per Stasiun</div>
            <div class="panel-desc">Frekuensi jadwal perjalanan (batang) dan rata-rata tarif (titik)</div>
        """, unsafe_allow_html=True)

        st_agg = (
            df.groupby("stasiun_tujuan")
            .agg(Layanan=("kode", "count"), Tarif=("harga_rp", "mean"))
            .reset_index().sort_values("Layanan", ascending=False)
        )
        bar_stn = (
            alt.Chart(st_agg)
            .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3, color="#94A3B8")
            .encode(
                y=alt.Y("stasiun_tujuan:N", sort="-x", title="Stasiun Tujuan",
                        axis=alt.Axis(labelColor="#334155", labelFontWeight=500)),
                x=alt.X("Layanan:Q", title="Jumlah Jadwal Layanan"),
                tooltip=[
                    alt.Tooltip("stasiun_tujuan:N", title="Stasiun Tujuan"),
                    alt.Tooltip("Layanan:Q",        title="Frekuensi Jadwal"),
                    alt.Tooltip("Tarif:Q",          title="Rata-Rata Tarif", format=","),
                ]
            )
        )
        dot_stn = (
            alt.Chart(st_agg)
            .mark_circle(size=50, color="#2563EB")
            .encode(
                y=alt.Y("stasiun_tujuan:N", sort="-x"),
                x="Layanan:Q",
                tooltip=[alt.Tooltip("Tarif:Q", title="Rata-Rata Tarif (Rp)", format=",")]
            )
        )
        st.altair_chart((bar_stn + dot_stn).properties(height=max(300, len(st_agg)*20)), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Rasio Tarif per Menit Perjalanan</div>', unsafe_allow_html=True)
    hpm_agg = (
        df.groupby("stasiun_tujuan")["harga_per_menit"]
        .mean().reset_index()
        .sort_values("harga_per_menit", ascending=False)
    )
    hpm_agg["Status_Relasi"] = hpm_agg.stasiun_tujuan.isin(["JATINEGARA", "BEKASI", "CIKARANG"])

    chart_hpm = (
        alt.Chart(hpm_agg)
        .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
        .encode(
            y=alt.Y("stasiun_tujuan:N", sort="-x", title="Stasiun Tujuan", axis=alt.Axis(labelColor="#334155")),
            x=alt.X("harga_per_menit:Q", title="Tarif per Menit Perjalanan (Rp/Menit)",
                    axis=alt.Axis(labelExpr="'Rp '+format(datum.value,',.0f')")),
            color=alt.Color("Status_Relasi:N",
                            scale=alt.Scale(domain=[True, False], range=["#DC2626", "#64748B"]),
                            legend=alt.Legend(title="Kategori Jarak",
                                              labelExpr="datum.value==='true'?'Jarak Dekat (Tarif Minimum)':'Rute Antarkota'",
                                              labelColor="#334155", titleColor="#0F172A")),
            tooltip=[
                alt.Tooltip("stasiun_tujuan:N",  title="Stasiun Tujuan"),
                alt.Tooltip("harga_per_menit:Q", title="Tarif per Menit", format=",.1f"),
            ]
        )
        .properties(height=380)
    )
    st.altair_chart(chart_hpm, use_container_width=True)
    st.markdown("""
    <div class="note-box">
    <strong>Efek Batas Tarif Bawah:</strong> Stasiun <b>Jatinegara</b> (~10 menit) dan <b>Bekasi</b> (~25 menit) memiliki biaya per menit tertinggi (hingga Rp 29.977/menit). Hal ini disebabkan oleh penetapan tarif minimum pada tiket kereta antarkota komersial keberangkatan Jakarta.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: DURASI & JARAK
# ─────────────────────────────────────────────────────────────────────────────
with tab_durasi:
    col_a, col_b = st.columns([1.25, 0.75], gap="medium")

    with col_a:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Korelasi Durasi Perjalanan terhadap Harga Tiket</div>
            <div class="panel-desc">Sebaran data durasi tempuh dan tarif disertai garis regresi linier per kelas</div>
        """, unsafe_allow_html=True)

        sel_scatter = alt.selection_point(fields=["kategori_kelas_detail"], bind="legend")
        sc = (
            alt.Chart(df)
            .mark_circle(size=36)
            .encode(
                x=alt.X("durasi_menit:Q", title="Durasi Perjalanan (Menit)"),
                y=alt.Y("harga_rp:Q", title="Harga Tiket (Rp)",
                        axis=alt.Axis(labelExpr="'Rp '+format(datum.value/1000,',.0f')+'k'")),
                color=alt.Color("kategori_kelas_detail:N",
                                scale=alt.Scale(domain=KELAS_DOMAIN, range=KELAS_RANGE),
                                legend=alt.Legend(title="Kategori", orient="bottom", direction="horizontal",
                                                  labelColor="#334155", titleColor="#0F172A")),
                opacity=alt.condition(sel_scatter, alt.value(0.65), alt.value(0.08)),
                tooltip=[
                    alt.Tooltip("nama_kereta:N",           title="Kereta Api"),
                    alt.Tooltip("stasiun_tujuan:N",        title="Stasiun Tujuan"),
                    alt.Tooltip("kategori_kelas_detail:N", title="Kategori"),
                    alt.Tooltip("durasi_menit:Q",          title="Durasi (Menit)"),
                    alt.Tooltip("harga_rp:Q",              title="Harga Tiket", format=","),
                ]
            )
            .add_params(sel_scatter)
        )
        rg = (
            alt.Chart(df)
            .transform_regression("durasi_menit", "harga_rp", groupby=["kategori_kelas_detail"])
            .mark_line(strokeWidth=1.8, strokeDash=[4, 3])
            .encode(
                x="durasi_menit:Q", y="harga_rp:Q",
                color=alt.Color("kategori_kelas_detail:N", scale=alt.Scale(domain=KELAS_DOMAIN, range=KELAS_RANGE), legend=None),
                strokeOpacity=alt.condition(sel_scatter, alt.value(0.9), alt.value(0.1)),
            )
        )
        st.altair_chart((sc + rg).properties(height=350).interactive(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Kekuatan Korelasi Pearson (r)</div>
            <div class="panel-desc">Tingkat hubungan linier antara durasi dan harga tiket per kelas</div>
        """, unsafe_allow_html=True)

        corr_all = df.durasi_menit.corr(df.harga_rp)
        corr_data = []
        for kat in KELAS_DOMAIN:
            sub = df[df.kategori_kelas_detail == kat]
            if len(sub) > 5:
                corr_data.append({"Kategori": kat, "r": round(sub.durasi_menit.corr(sub.harga_rp), 4), "n": len(sub)})
        corr_df = pd.DataFrame(corr_data)

        bar_corr = (
            alt.Chart(corr_df)
            .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
            .encode(
                y=alt.Y("Kategori:N", sort="-x", title=None, axis=alt.Axis(labelColor="#334155", labelFontWeight=500)),
                x=alt.X("r:Q", title="Koefisien Korelasi (r)", scale=alt.Scale(domain=[0, 1])),
                color=alt.Color("Kategori:N", scale=alt.Scale(domain=KELAS_DOMAIN, range=KELAS_RANGE), legend=None),
                tooltip=[alt.Tooltip("Kategori:N"), alt.Tooltip("r:Q", format=".4f"), alt.Tooltip("n:Q", title="Sampel")]
            )
        )
        lbl_corr = (
            alt.Chart(corr_df)
            .mark_text(align="left", dx=6, fontWeight=600, fontSize=11, color="#0F172A")
            .encode(y=alt.Y("Kategori:N", sort="-x"), x="r:Q", text=alt.Text("r:Q", format=".3f"))
        )
        st.altair_chart((bar_corr + lbl_corr).properties(height=150), use_container_width=True)
        st.markdown(f'<div class="note-box">Korelasi keseluruhan dataset: <b>r = {corr_all:.4f}</b>. Durasi waktu merefleksikan jarak perjalanan secara linier pada kelas komersial.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Pemberhentian vs Durasi (Intra-Stasiun)</div>
            <div class="panel-desc">Korelasi dengan mengontrol jarak fisik tujuan yang sama</div>
        """, unsafe_allow_html=True)

        intra_data = []
        for st_name in df.stasiun_tujuan.unique():
            sub = df[df.stasiun_tujuan == st_name]
            if len(sub) >= 8:
                intra_data.append({
                    "Stasiun": st_name,
                    "r": round(sub.jumlah_stasiun_pemberhentian.corr(sub.durasi_menit), 3),
                    "n": len(sub)
                })
        if intra_data:
            intra_df = pd.DataFrame(intra_data).sort_values("r", ascending=False)
            bar_intra = (
                alt.Chart(intra_df)
                .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
                .encode(
                    y=alt.Y("Stasiun:N", sort="-x", title=None, axis=alt.Axis(labelColor="#334155")),
                    x=alt.X("r:Q", title="Korelasi (r)", scale=alt.Scale(domain=[-0.2, 1])),
                    color=alt.condition(alt.datum.r > 0.45, alt.value("#2563EB"), alt.value("#94A3B8")),
                    tooltip=[alt.Tooltip("Stasiun:N"), alt.Tooltip("r:Q", format=".3f"), alt.Tooltip("n:Q", title="Sampel")]
                )
                .properties(height=max(140, len(intra_df)*18))
            )
            st.altair_chart(bar_intra, use_container_width=True)
            st.markdown('<div class="note-box">Korelasi global (r = 0.92) terdistorsi oleh jarak. Pada stasiun yang sama, korelasi menurun ke r = 0.09 s.d. 0.57.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: POLA KEBERANGKATAN
# ─────────────────────────────────────────────────────────────────────────────
with tab_operasional:
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Kepadatan Jadwal Berdasarkan Jam Keberangkatan</div>
            <div class="panel-desc">Distribusi volume keberangkatan kereta sepanjang 24 jam</div>
        """, unsafe_allow_html=True)

        hourly_df = df.groupby("jam_berangkat_jam")["kode"].count().reset_index()
        hourly_df.columns = ["Jam", "Frekuensi"]
        chart_area = (
            alt.Chart(hourly_df)
            .mark_area(
                interpolate="monotone",
                line={"color": "#2563EB", "strokeWidth": 2},
                color="#EFF6FF"
            )
            .encode(
                x=alt.X("Jam:Q", title="Jam Keberangkatan (0 – 23)", scale=alt.Scale(domain=[0, 23]),
                        axis=alt.Axis(tickMinStep=1, labelColor="#334155")),
                y=alt.Y("Frekuensi:Q", title="Jumlah Jadwal", axis=alt.Axis(labelColor="#334155")),
                tooltip=["Jam:Q", alt.Tooltip("Frekuensi:Q", title="Jumlah Jadwal")]
            )
        )
        pk = hourly_df.nlargest(1, "Frekuensi")
        pk_rule = alt.Chart(pk).mark_rule(color="#DC2626", strokeDash=[3, 3], strokeWidth=1.2).encode(x="Jam:Q")
        pk_lbl  = alt.Chart(pk).mark_text(dy=-8, color="#DC2626", fontWeight=600, fontSize=11).encode(x="Jam:Q", y="Frekuensi:Q", text=alt.Text("Frekuensi:Q", format="d"))

        st.altair_chart((chart_area + pk_rule + pk_lbl).properties(height=250).interactive(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="panel-box">
            <div class="panel-title">Proporsi Jadwal per Periode Waktu</div>
            <div class="panel-desc">Pagi (05-10), Siang (11-14), Sore (15-18), Malam (19-23)</div>
        """, unsafe_allow_html=True)

        color_time = {"Pagi": "#F59E0B", "Siang": "#3B82F6", "Sore": "#6366F1", "Malam": "#1E293B", "Dini hari": "#94A3B8"}
        time_df = df.groupby("waktu_keberangkatan")["kode"].count().reset_index()
        time_df.columns = ["Periode", "Frekuensi"]
        time_df["Persentase"] = (time_df.Frekuensi / time_df.Frekuensi.sum() * 100).round(1)

        chart_time = (
            alt.Chart(time_df)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X("Periode:N", sort=list(color_time), title="Periode",
                        axis=alt.Axis(labelAngle=0, labelFontWeight=500, labelColor="#334155")),
                y=alt.Y("Frekuensi:Q", title="Jumlah Jadwal", axis=alt.Axis(labelColor="#334155")),
                color=alt.Color("Periode:N", scale=alt.Scale(domain=list(color_time), range=list(color_time.values())), legend=None),
                tooltip=["Periode:N", "Frekuensi:Q", alt.Tooltip("Persentase:Q", title="Pangsa", format=".1f")]
            )
        )
        lbl_time = (
            alt.Chart(time_df)
            .mark_text(dy=-8, fontWeight=600, fontSize=11, color="#0F172A")
            .encode(x=alt.X("Periode:N", sort=list(color_time)), y="Frekuensi:Q", text=alt.Text("Persentase:Q", format=".1f"))
        )
        st.altair_chart((chart_time + lbl_time).properties(height=250), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Kereta Api Paling Aktif per Periode</div>', unsafe_allow_html=True)
    p_active = [w for w in ["Pagi", "Siang", "Sore", "Malam", "Dini hari"] if w in df.waktu_keberangkatan.unique()]
    cols_period = st.columns(len(p_active))

    for idx, wkt in enumerate(p_active):
        top_k = df[df.waktu_keberangkatan == wkt]["nama_kereta"].value_counts().head(4)
        with cols_period[idx]:
            st.markdown(f"""
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:4px;padding:10px 12px;">
                <div style="font-size:0.74rem;font-weight:700;color:#0F172A;text-transform:uppercase;margin-bottom:6px;padding-bottom:4px;border-bottom:1px solid #E2E8F0;">
                    {wkt}
                </div>
            """, unsafe_allow_html=True)
            for kname, kcnt in top_k.items():
                st.markdown(f"""
                <div style="font-size:0.77rem;padding:3px 0;display:flex;justify-content:space-between;color:#334155;">
                    <span style="font-weight:500;">{kname}</span>
                    <span style="color:#64748B;">{kcnt}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:20px;">10 Kereta Api Teratas Berdasarkan Jumlah Jadwal</div>', unsafe_allow_html=True)
    top10_df = (
        df.groupby("nama_kereta")
        .agg(Layanan=("kode", "count"), Tarif=("harga_rp", "mean"), Durasi=("durasi_menit", "median"))
        .reset_index().nlargest(10, "Layanan")
    )
    b_top = (
        alt.Chart(top10_df)
        .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3, color="#64748B")
        .encode(
            y=alt.Y("nama_kereta:N", sort="-x", title="Nama Kereta", axis=alt.Axis(labelColor="#334155", labelFontWeight=500)),
            x=alt.X("Layanan:Q", title="Jumlah Jadwal Layanan"),
            tooltip=[
                alt.Tooltip("nama_kereta:N", title="Kereta Api"),
                alt.Tooltip("Layanan:Q",     title="Total Jadwal"),
                alt.Tooltip("Tarif:Q",       title="Rata-Rata Tarif", format=","),
                alt.Tooltip("Durasi:Q",      title="Median Durasi (Menit)"),
            ]
        )
    )
    d_top = (
        alt.Chart(top10_df)
        .mark_circle(size=60, color="#2563EB")
        .encode(
            y=alt.Y("nama_kereta:N", sort="-x"),
            x="Layanan:Q",
            tooltip=[alt.Tooltip("Tarif:Q", title="Rata-Rata Tarif", format=",")]
        )
    )
    l_top = (
        alt.Chart(top10_df)
        .mark_text(align="left", dx=6, fontSize=11, fontWeight=600, color="#0F172A")
        .encode(y=alt.Y("nama_kereta:N", sort="-x"), x="Layanan:Q", text=alt.Text("Layanan:Q"))
    )
    st.altair_chart((b_top + d_top + l_top).properties(height=320), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5: JADWAL & PROFIL KERETA API
# ─────────────────────────────────────────────────────────────────────────────
with tab_profil_ka:
    st.markdown("""
    <div class="panel-box">
        <div class="panel-title">Profil & Jadwal Kereta Api Tertentu</div>
        <div class="panel-desc">Pilih salah satu dari 31 armada kereta api untuk melihat stasiun singgah, jam tiba, jenis sarana, dan struktur tarif subkelas</div>
    """, unsafe_allow_html=True)

    col_select_ka, _ = st.columns([1.5, 2.5])
    with col_select_ka:
        default_ka_idx = 0
        if pilihan_kereta != "Semua Kereta Api (31 KA)" and pilihan_kereta in opt_kereta:
            default_ka_idx = opt_kereta.index(pilihan_kereta)
        elif "SAWUNGGALIH" in opt_kereta:
            default_ka_idx = opt_kereta.index("SAWUNGGALIH")

        ka_selected = st.selectbox(
            "Pilih Kereta Api yang Ingin Ditinjau:",
            options=opt_kereta,
            index=default_ka_idx,
            key="select_ka_profil"
        )

    ka_data = DF_RAW[DF_RAW.nama_kereta == ka_selected].copy()

    ka_nomor = sorted(ka_data["kode_kereta"].unique().tolist())
    ka_berangkat = sorted(ka_data["jam_berangkat"].unique().tolist())
    ka_kelas = sorted(ka_data["kategori_kelas_detail"].unique().tolist())
    ka_rangkaian = sorted(ka_data["jenis_rangkaian"].unique().tolist())
    ka_dest_count = ka_data["stasiun_tujuan"].nunique()
    ka_min_p = ka_data["harga_rp"].min()
    ka_max_p = ka_data["harga_rp"].max()

    st.markdown(f"""
    <div class="metric-grid" style="margin-top:14px; margin-bottom:18px;">
        <div class="metric-tile">
            <div class="metric-tile-label">Nomor KA</div>
            <div class="metric-tile-value" style="font-size:1.15rem;">{", ".join(ka_nomor)}</div>
            <div class="metric-tile-sub">Kode grafik perjalanan</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-label">Jam Berangkat PSE</div>
            <div class="metric-tile-value" style="font-size:1.15rem;">{", ".join(ka_berangkat)}</div>
            <div class="metric-tile-sub">Stasiun Pasar Senen</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-label">Kelas Tersedia</div>
            <div class="metric-tile-value" style="font-size:1.05rem;">{", ".join(ka_kelas)}</div>
            <div class="metric-tile-sub">Kategori armada</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-label">Jenis Rangkaian</div>
            <div class="metric-tile-value" style="font-size:0.95rem; font-weight:600;">{ka_rangkaian[0] if len(ka_rangkaian)==1 else f"{len(ka_rangkaian)} Tipe Rangkaian"}</div>
            <div class="metric-tile-sub">Sarana kereta</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-label">Rentang Tarif</div>
            <div class="metric-tile-value" style="font-size:1.15rem;">{format_rupiah(ka_min_p)}</div>
            <div class="metric-tile-sub">s.d. {format_rupiah(ka_max_p)}</div>
        </div>
        <div class="metric-tile">
            <div class="metric-tile-label">Stasiun Singgah</div>
            <div class="metric-tile-value" style="font-size:1.15rem;">{ka_dest_count} Stasiun</div>
            <div class="metric-tile-sub">Tujuan akhir koridor</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_ka_c, col_ka_t = st.columns([1.15, 0.85], gap="medium")

    with col_ka_c:
        st.markdown('<div class="panel-title" style="font-size:0.84rem;margin-bottom:8px;">Tarif Tiket Berdasarkan Stasiun Tujuan (Urutan Waktu Tempuh)</div>', unsafe_allow_html=True)
        ka_chart = (
            alt.Chart(ka_data)
            .mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
            .encode(
                y=alt.Y("stasiun_tujuan:N",
                        sort=alt.EncodingSortField("durasi_menit", order="ascending"),
                        title="Stasiun Tujuan"),
                x=alt.X("harga_rp:Q", title="Harga Tiket (Rp)",
                        axis=alt.Axis(labelExpr="'Rp '+format(datum.value/1000,',.0f')+'k'")),
                color=alt.Color("kategori_kelas_detail:N",
                                scale=alt.Scale(domain=KELAS_DOMAIN, range=KELAS_RANGE),
                                legend=alt.Legend(title="Kelas", orient="bottom")),
                tooltip=[
                    alt.Tooltip("stasiun_tujuan:N", title="Stasiun"),
                    alt.Tooltip("jam_sampai:N",     title="Jam Tiba"),
                    alt.Tooltip("durasi_menit:Q",    title="Durasi (Mnt)"),
                    alt.Tooltip("kode_kelas:N",      title="Subkelas"),
                    alt.Tooltip("harga_rp:Q",        title="Tarif", format=","),
                ]
            )
            .properties(height=max(280, ka_dest_count * 23))
        )
        st.altair_chart(ka_chart, use_container_width=True)

    with col_ka_t:
        st.markdown('<div class="panel-title" style="font-size:0.84rem;margin-bottom:8px;">Daftar Rute & Tarif Subkelas</div>', unsafe_allow_html=True)
        ka_show_cols = ["stasiun_tujuan", "kategori_kelas_detail", "kode_kelas", "jam_berangkat", "jam_sampai", "durasi_menit", "harga_rp"]
        ka_table_out = ka_data[ka_show_cols].sort_values("durasi_menit").rename(columns={
            "stasiun_tujuan": "Tujuan",
            "kategori_kelas_detail": "Kelas",
            "kode_kelas": "Subkelas",
            "jam_berangkat": "Berangkat",
            "jam_sampai": "Tiba",
            "durasi_menit": "Durasi (Mnt)",
            "harga_rp": "Tarif (Rp)"
        })
        st.dataframe(
            ka_table_out,
            use_container_width=True,
            hide_index=True,
            height=max(280, ka_dest_count * 24),
            column_config={
                "Tarif (Rp)": st.column_config.NumberColumn(format="Rp %d")
            }
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6: TABEL DATA
# ─────────────────────────────────────────────────────────────────────────────
with tab_data:
    col_search, col_sort, col_dir = st.columns([2.2, 1.3, 1.1])
    with col_search:
        search_query = st.text_input("Pencarian Langsung", placeholder="Cari nama kereta, stasiun tujuan, atau kode...", label_visibility="collapsed")
    with col_sort:
        sort_field = st.selectbox("Urutkan Kolom", ["harga_rp", "durasi_menit", "harga_per_menit", "jumlah_stasiun_pemberhentian", "nama_kereta"])
    with col_dir:
        sort_asc = st.radio("Arah", ["Naik", "Turun"], horizontal=True, label_visibility="collapsed") == "Naik"

    filtered_table = df.copy()
    if search_query:
        sq = search_query.upper()
        filtered_table = filtered_table[
            filtered_table.nama_kereta.str.contains(sq, na=False) |
            filtered_table.stasiun_tujuan.str.contains(sq, na=False) |
            filtered_table.kode.str.contains(sq, na=False)
        ]
    filtered_table = filtered_table.sort_values(sort_field, ascending=sort_asc)

    columns_show = [
        "kode", "nama_kereta", "stasiun_tujuan", "kategori_kelas_detail",
        "jenis_rangkaian", "jam_berangkat", "jam_sampai",
        "durasi_menit", "jumlah_stasiun_pemberhentian", "harga_rp", "harga_per_menit"
    ]
    renamed_df = filtered_table[[c for c in columns_show if c in filtered_table.columns]].rename(columns={
        "kode": "Kode Jadwal", "nama_kereta": "Nama Kereta", "stasiun_tujuan": "Stasiun Tujuan",
        "kategori_kelas_detail": "Kelas", "jenis_rangkaian": "Jenis Rangkaian",
        "jam_berangkat": "Berangkat", "jam_sampai": "Tiba",
        "durasi_menit": "Durasi (Mnt)", "jumlah_stasiun_pemberhentian": "Perhentian",
        "harga_rp": "Tarif (Rp)", "harga_per_menit": "Tarif/Mnt"
    })

    st.caption(f"Menampilkan {len(renamed_df):,} baris dari total {n_filtered:,} jadwal terfilter.")

    st.dataframe(
        renamed_df,
        use_container_width=True,
        hide_index=True,
        height=430,
        column_config={
            "Tarif (Rp)":   st.column_config.NumberColumn("Tarif (Rp)", format="Rp %d"),
            "Tarif/Mnt":    st.column_config.NumberColumn("Tarif/Mnt", format="%.1f"),
            "Durasi (Mnt)": st.column_config.NumberColumn("Durasi (Mnt)", format="%d mnt"),
        }
    )

    st.write("")
    btn_a, btn_b, _ = st.columns([1.2, 1.2, 1.6])
    with btn_a:
        st.download_button(
            "Unduh Data Terfilter (CSV)",
            data=filtered_table.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig"),
            file_name="kai_pse_terfilter.csv",
            mime="text/csv",
            use_container_width=True
        )
    with btn_b:
        st.download_button(
            "Unduh Seluruh Data (CSV)",
            data=DF_RAW.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig"),
            file_name="kai_pse_data_bersih_lengkap.csv",
            mime="text/csv",
            use_container_width=True
        )

# ─────────────────────────────────────────────────────────────────────────────
# 10. FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #E2E8F0;margin-top:24px;padding-top:10px;display:flex;justify-content:space-between;color:#64748B;font-size:0.74rem;">
    <span>PT Kereta Api Indonesia (Persero) · Koridor Keberangkatan Pasar Senen (PSE)</span>
    <span>Laporan Analitik Jadwal & Tarif · Platform BI</span>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Stravue | Business Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 2. CUSTOM CSS INJECTION (FORCE LIGHT THEME & PILL NAVBAR)
# =========================================================
st.markdown("""
<style>
    /* Menyembunyikan elemen bawaan Streamlit untuk full-width web app */
    [data-testid="collapsedControl"] {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Latar belakang aplikasi */
    .stApp {background-color: #F8FAFC !important;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px;}
    
    /* ---------------------------------------------------
       FORCE TEXT COLOR (Mencegah teks putih di Dark Mode)
    --------------------------------------------------- */
    .stMarkdown p, .stMarkdown span, .stText p, label p {color: #0F172A !important;}
    h1, h2, h3, h4, h5, h6 {color: #0F172A !important;}
    
    [data-testid="stMetricValue"] div {color: #0F172A !important; font-weight: 800 !important; font-size: 2rem !important;}
    [data-testid="stMetricLabel"] p {color: #64748B !important; font-weight: 600 !important; text-transform: uppercase;}
    [data-testid="stMetricDelta"] div {color: #10B981 !important; font-weight: 600 !important;}
    
    /* ---------------------------------------------------
       FIX: Memaksa warna dropdown, number input, dan slider
    --------------------------------------------------- */
    /* Selectbox / Dropdown */
    [data-baseweb="select"] > div {background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important;}
    [data-baseweb="select"] span, [data-baseweb="select"] div {color: #0F172A !important;}
    ul[data-baseweb="menu"] {background-color: #FFFFFF !important;}
    ul[data-baseweb="menu"] li {color: #0F172A !important;}

    /* Number Input (Config AI Page) */
    [data-testid="stNumberInput"] > div > div > div {background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; border-radius: 6px !important;}
    [data-testid="stNumberInput"] input {background-color: #FFFFFF !important; color: #0F172A !important; -webkit-text-fill-color: #0F172A !important;}
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {background-color: #F1F5F9 !important; color: #0F172A !important;}
    [data-testid="stNumberInputStepUp"] svg, [data-testid="stNumberInputStepDown"] svg {fill: #0F172A !important;}
    
    /* Slider Text */
    .stSlider div, .stSlider p {color: #0F172A !important;}

    /* ---------------------------------------------------
       STYLING NAVBAR PILL
    --------------------------------------------------- */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        background-color: #FFFFFF !important;
        padding: 5px 15px;
        border-radius: 50px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0 !important;
        width: fit-content;
        gap: 10px;
    }
    div[role="radiogroup"] > label {
        background-color: transparent !important;
        padding: 10px 20px !important;
        border-radius: 50px !important;
        margin: 0 !important;
        border: none !important;
        cursor: pointer;
    }
    div[role="radiogroup"] > label > div:first-child {display: none !important;}
    div[role="radiogroup"] > label[data-checked="true"] {background-color: #2563EB !important;}
    div[role="radiogroup"] > label[data-checked="true"] p {color: #FFFFFF !important; font-weight: 600 !important;}
    div[role="radiogroup"] > label[data-checked="false"] p {color: #64748B !important; font-weight: 600 !important;}

    /* ---------------------------------------------------
       TYPOGRAPHY & CUSTOM CARDS
    --------------------------------------------------- */
    .page-title {font-size: 1.8rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; letter-spacing: -0.5px;}
    .section-title {font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-top: 1.5rem; margin-bottom: 1rem;}

    .guide-box {background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 1.2rem 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);}
    .guide-box p {color: #334155 !important; font-size: 0.95rem; line-height: 1.6; margin:0 !important;}
    .guide-box strong {color: #0F172A !important; font-weight: 700;}

    .metric-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05); min-height: 120px;}
    
    .insight-card {background: #EFF6FF; border-left: 4px solid #2563EB; border-radius: 8px; padding: 18px 20px; margin: 15px 0;}
    .insight-card p {color: #0F172A !important; margin: 0 !important; font-size: 1rem;}
    
    .warning-card {background: #FEF2F2; border-left: 4px solid #EF4444; border-radius: 8px; padding: 18px 20px; margin: 15px 0;}
    .warning-card p {color: #0F172A !important; margin: 0 !important; font-size: 1rem;}

    .success-card {background: #F0FDF4; border-left: 4px solid #10B981; border-radius: 8px; padding: 18px 20px; margin: 15px 0;}
    .success-card p {color: #0F172A !important; margin: 0 !important; font-size: 1rem;}

    .stTabs [data-baseweb="tab-list"] {gap: 2rem;}
    .stTabs [data-baseweb="tab"] {height: 3rem; white-space: pre-wrap; font-weight: 600; color: #475569 !important;}
    .stTabs [aria-selected="true"] {color: #2563eb !important;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. STATE MANAGEMENT & DATA MOCKUP
# =========================================================
if 'horizon' not in st.session_state: st.session_state['horizon'] = 30
if 'lead_time' not in st.session_state: st.session_state['lead_time'] = 7
if 'cash_budget' not in st.session_state: st.session_state['cash_budget'] = 50000000

@st.cache_data
def get_inventory_data():
    return pd.DataFrame({
        "Category": ["Furniture", "Office Supplies", "Technology"],
        "Current Stock": [450, 1800, 120],
        "Safety Stock": [50, 200, 30],
        "Reorder Point": [80, 400, 50],
        "Unit Cost (IDR)": [1500000, 25000, 3500000],
        "Selling Price (IDR)": [2000000, 35000, 5000000],
        "Base Daily Demand": [15, 60, 5]
    })

if 'df_inv' not in st.session_state:
    st.session_state['df_inv'] = get_inventory_data()

@st.cache_data
def generate_full_forecast_data(daily_avg, horizon):
    np.random.seed(42)
    today = datetime.today()
    
    # Data Historis 90 Hari
    hist_dates = [today - timedelta(days=i) for i in range(90, 0, -1)]
    hist_sales = [max(0, int(np.random.normal(daily_avg, daily_avg * 0.2))) for _ in range(90)]
    
    # Data Forecast AI
    fcst_dates = [today + timedelta(days=i) for i in range(horizon)]
    weeks_needed = (horizon // 7) + 2
    weekly_seasonality = np.array([1.2, 1.1, 1.0, 1.1, 1.2, 0.7, 0.6] * weeks_needed)[:horizon]
    fcst_sales = (daily_avg * weekly_seasonality) + np.random.normal(0, daily_avg * 0.1, horizon)
    fcst_sales = [max(0, int(x)) for x in fcst_sales]
    
    return hist_dates, hist_sales, fcst_dates, fcst_sales

# =========================================================
# 4. TOP NAVBAR BUILDER
# =========================================================
nav_col1, nav_col2 = st.columns([1, 4])

with nav_col1:
    logo_c1, logo_c2 = st.columns([1, 4])
    with logo_c1:
        # Hapus bagian ini jika error / gambar a.png tidak ada
        st.image("a.png", width=40)
    with logo_c2:
        st.markdown("<h3 style='margin:0; padding-top:5px; font-weight:800; color:#0F172A;'>Stravue</h3>", unsafe_allow_html=True)

with nav_col2:
    menu = st.radio(
        "Menu", 
        ["Overview", "Inventory", "Data Pipeline", "Prediksi Baru", "Config AI"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown("<hr style='border-color: #CBD5E1; margin-top: 0; margin-bottom: 2rem;'>", unsafe_allow_html=True)

# =========================================================
# 5. HALAMAN: OVERVIEW
# =========================================================
if menu == "Overview":
    st.markdown('<div class="page-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <p><strong>Informasi Halaman:</strong> Halaman ini memberikan ringkasan eksekutif mengenai performa dan kesehatan inventaris bisnis Anda secara menyeluruh. Panel atas menunjukkan matriks performa utama, termasuk rata-rata permintaan harian dan akurasi model AI. Tabel 'Status Risiko Inventaris' secara proaktif mendeteksi kategori produk yang berisiko mengalami kekosongan stok berdasarkan proyeksi algoritma.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Kategori Produk", len(st.session_state["df_inv"]), "Teranalisis oleh AI")
    with c2:
        st.metric("Rata-rata Demand Harian", "145", "+5.2% dari bulan lalu")
    with c3:
        st.metric("Forecast Horizon", str(st.session_state["horizon"]), "Hari ke depan")
    with c4:
        st.metric("Akurasi Model", "87.6%", "Facebook Prophet")

    st.markdown('<div class="section-title">Status Risiko Inventaris</div>', unsafe_allow_html=True)
    
    df_display = st.session_state['df_inv'].copy()
    df_display["Forecast Demand"] = df_display["Base Daily Demand"] * st.session_state['horizon']
    df_display["Status"] = np.where((df_display["Current Stock"] - df_display["Forecast Demand"]) < 0, 'Kritis', 'Aman')
    
    st.dataframe(df_display[["Category", "Current Stock", "Safety Stock", "Reorder Point", "Status"]], use_container_width=True, hide_index=True)

# =========================================================
# 6. HALAMAN: INVENTORY CONTROL
# =========================================================
elif menu == "Inventory":
    st.markdown('<div class="page-title">Manajemen Inventaris</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <p><strong>Informasi Halaman:</strong> Tabel di bawah ini merepresentasikan basis data stok gudang aktual. Anda dapat mengubah angka pada kolom <strong>Current Stock (Edit Manual)</strong> dengan mengklik sel secara langsung. Sistem ini bertindak sebagai sumber data tunggal (Single Source of Truth), sehingga setiap perubahan akan langsung memperbarui kalkulasi prediksi, risiko, dan rekomendasi AI di seluruh platform. Gunakan tombol unduh untuk mengekspor data operasional ke format CSV.</p>
    </div>
    """, unsafe_allow_html=True)
    
    edited_df = st.data_editor(
        st.session_state['df_inv'],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Category": st.column_config.TextColumn("Kategori Produk", disabled=True),
            "Current Stock": st.column_config.NumberColumn("Current Stock (Edit Manual)", min_value=0),
            "Unit Cost (IDR)": st.column_config.NumberColumn("Unit Cost (IDR)", format="%d"),
            "Selling Price (IDR)": st.column_config.NumberColumn("Selling Price (IDR)", format="%d")
        }
    )
    st.session_state['df_inv'] = edited_df
    
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("Export Data (CSV)", data=csv, file_name='inventory_data.csv', mime='text/csv')

# =========================================================
# 7. HALAMAN: DATA PIPELINE
# =========================================================
elif menu == "Data Pipeline":
    st.markdown('<div class="page-title">Arsitektur Data Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <p><strong>Informasi Halaman:</strong> Mesin Prediktif AI membutuhkan kualitas data yang tinggi. Halaman ini memberikan transparansi logistik mengenai proses <i>Extract, Transform, and Load (ETL)</i>. Sistem memproses data historis secara otomatis, melakukan imputasi pada nilai yang kosong, membersihkan duplikasi, dan menstabilkan anomali (outlier) sebelum rangkaian data tersebut disalurkan ke dalam model Machine Learning.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Missing Values Imputed", "142 Baris")
    col2.metric("Duplicates Removed", "12 Baris")
    col3.metric("Anomalies Smoothed", "5 Titik Data")
    
    st.markdown('<div class="section-title">Alur Eksekusi Sistem ETL</div>', unsafe_allow_html=True)
    st.code("""
    [1] Raw Data Ingestion (Dataset Sumber Internal/Kaggle)
        |
    [2] Data Cleaning & Standardization
        - Null Value Imputation (Metode Median)
        - Proses Penghapusan Duplikasi
        |
    [3] Time-Series Feature Engineering
        - Ekstraksi Format Datetime
        - Parameter Musiman (DayOfWeek, Hari Libur)
        |
    [4] Outlier Detection & Handling
        - Stabilisasi Varians (Z-Score method)
        |
    [5] Machine Learning Feed (Algoritma Facebook Prophet)
    """, language="text")

# =========================================================
# 8. HALAMAN: PREDIKSI BARU
# =========================================================
elif menu == "Prediksi Baru":
    st.markdown('<div class="page-title">Sistem Pendukung Keputusan AI</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <p><strong>Informasi Halaman:</strong> Modul ini merupakan pusat kecerdasan preskriptif. Pertama, pilih kategori produk pada menu lungsur (dropdown) di bawah. 
        <br><br><strong>Tab AI Forecasting:</strong> Menampilkan visualisasi sambungan tren historis dengan proyeksi model masa depan.<br><strong>Tab Rekomendasi Aksi:</strong> Menerjemahkan data prediksi menjadi instruksi operasional yang eksplisit.<br><strong>Tab Simulator Skenario:</strong> Digital Twin untuk menguji ketahanan inventaris terhadap berbagai kejutan operasional.<br><strong>Tab Proyeksi Arus Kas:</strong> Mengkalkulasi dampak keputusan pemesanan terhadap rasio likuiditas perusahaan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        st.markdown("<p style='font-weight: 700; color: #0F172A; margin-bottom: 0.2rem;'>Pilih Kategori Produk:</p>", unsafe_allow_html=True)
        cat = st.selectbox("Select Target Category", st.session_state['df_inv']['Category'].tolist(), label_visibility="collapsed")
    
    cat_data = st.session_state['df_inv'][st.session_state['df_inv']["Category"] == cat].iloc[0]
    daily_avg = cat_data["Base Daily Demand"]
    horizon = st.session_state['horizon']
    base_demand = int(daily_avg * horizon)
    
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["AI Forecasting", "Rekomendasi Aksi", "Simulator Skenario", "Proyeksi Arus Kas"])
    
    # --- TAB 1: AI FORECASTING CHART ---
    with tab1:
        st.markdown(f"<div class='section-title'>Prediksi Permintaan ({horizon} Hari Ke Depan)</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-bottom: 1rem;'>Garis abu-abu menunjukkan data performa historis aktual. Garis biru menampilkan proyeksi algoritma AI yang memodelkan tren, pola mingguan, dan musiman ke depan.</p>", unsafe_allow_html=True)
        
        hist_dates, hist_sales, fcst_dates, fcst_sales = generate_full_forecast_data(daily_avg, horizon)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_dates, y=hist_sales, mode='lines', name='Penjualan Historis',
            line=dict(color='#94A3B8', width=2),
            hovertemplate='<b>Tanggal</b>: %{x}<br><b>Penjualan</b>: %{y} unit<extra></extra>'
        ))
        
        conn_dates = [hist_dates[-1]] + fcst_dates
        conn_sales = [hist_sales[-1]] + fcst_sales
        
        fig.add_trace(go.Scatter(
            x=conn_dates, y=conn_sales, mode='lines+markers', name='Prediksi AI',
            line=dict(color='#2563EB', width=3, dash='solid'), marker=dict(size=5),
            hovertemplate='<b>Tanggal</b>: %{x}<br><b>Prediksi</b>: %{y} unit<extra></extra>'
        ))
        
        fig.add_vline(x=datetime.today().timestamp() * 1000, line_width=1, line_dash="dash", line_color="#0F172A")
        
        # Fixing Dark Text for Plotly
        fig.update_layout(
            height=400, hovermode="x unified",
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(color="#0F172A"),
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(showgrid=False, tickfont=dict(color="#0F172A")),
            yaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#0F172A")),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#0F172A"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: PRESCRIPTIVE ---
    with tab2:
        st.markdown("<div class='section-title'>Rekomendasi Tindakan Operasional</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        
        with c1:
            status_text = "Inventaris Tidak Mencukupi" if base_demand > cat_data['Current Stock'] else "Kapasitas Aman"
            box_class = "warning-card" if base_demand > cat_data['Current Stock'] else "insight-card"
            
            st.markdown(f"""
            <div class="{box_class}">
                <p style="font-size: 1.1rem; margin-top: 0; font-weight: 700;">Status Inventaris Saat Ini:</p>
                <p style="margin-bottom: 5px;"><strong>Proyeksi Permintaan ({horizon} hari):</strong> {base_demand} unit</p>
                <p style="margin-bottom: 5px;"><strong>Stok Tersedia:</strong> {cat_data['Current Stock']} unit</p>
                <p style="margin-bottom: 5px;"><strong>Estimasi Pengiriman Supplier:</strong> {st.session_state['lead_time']} hari</p>
                <hr style="border-color: rgba(0,0,0,0.1); margin: 10px 0;">
                <p style="margin-bottom: 0px; font-weight: 700;">Status Operasional: {status_text}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            shortage = base_demand - cat_data['Current Stock'] + cat_data['Safety Stock']
            order_date = (datetime.today() - timedelta(days=st.session_state['lead_time'] - 2)).strftime('%Y-%m-%d')
            
            if shortage > 0:
                st.markdown(f"""
                <div class="warning-card" style="border-color: #F59E0B; background-color: #FFFBEB;">
                    <p style="font-size: 1.1rem; margin-top: 0; font-weight: 700;">Tindakan Diperlukan: Lakukan Pemesanan Segera</p>
                    <p style="margin-bottom: 5px;">Sistem merekomendasikan eksekusi pengadaan sebanyak <b>{shortage} unit</b> paling lambat pada tanggal <b>{order_date}</b>.</p>
                    <p style="margin-bottom: 0px;">Tindakan ini diperlukan untuk mengamankan Safety Stock dan mencegah risiko Stockout secara menyeluruh.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-card">
                    <p style="font-size: 1.1rem; margin-top: 0; font-weight: 700;">Kondisi Operasional Stabil</p>
                    <p style="margin-bottom: 0;">Kapasitas inventaris saat ini memadai untuk menutupi proyeksi permintaan pasar. Tidak ada tindakan pengadaan darurat yang direkomendasikan.</p>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 3: WHAT-IF SIMULATOR ---
    with tab3:
        st.markdown("<div class='section-title'>Simulator Skenario Disrupsi (Digital Twin)</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-bottom: 1.5rem;'>Sesuaikan parameter slider di bawah ini untuk mensimulasikan dampak fluktuasi pasar atau kendala rantai pasok terhadap profitabilitas Anda.</p>", unsafe_allow_html=True)
        
        sc1, sc2, sc3 = st.columns(3)
        sim_demand = sc1.slider("Lonjakan Permintaan (%)", -50, 100, 20)
        sim_delay = sc2.slider("Keterlambatan Supplier (Hari)", 0, 30, 7)
        sim_inv = sc3.slider("Penyusutan Inventaris (%)", 0, 50, 0)
        
        new_demand = int(base_demand * (1 + sim_demand/100))
        new_inv = int(cat_data['Current Stock'] * (1 - sim_inv/100))
        
        risk_current = max(0, min(100, ((base_demand - cat_data['Current Stock'])/base_demand) * 100)) if base_demand > 0 else 0
        risk_scenario = max(0, min(100, ((new_demand - new_inv + (sim_delay*10))/new_demand) * 100)) if new_demand > 0 else 0
        
        profit_current = (cat_data['Current Stock'] if cat_data['Current Stock'] < base_demand else base_demand) * (cat_data['Selling Price (IDR)'] - cat_data['Unit Cost (IDR)'])
        profit_scenario = (new_inv if new_inv < new_demand else new_demand) * (cat_data['Selling Price (IDR)'] - cat_data['Unit Cost (IDR)'])
        
        st.markdown('<div class="section-title">Perbandingan Hasil Simulasi</div>', unsafe_allow_html=True)
        
        sim_data = pd.DataFrame({
            "Metrik Evaluasi": ["Proyeksi Permintaan", "Inventaris Tersedia", "Risiko Stockout", "Proyeksi Profitabilitas"],
            "Kondisi Saat Ini": [f"{base_demand} unit", f"{cat_data['Current Stock']} unit", f"{risk_current:.1f}%", f"IDR {profit_current:,.0f}"],
            "Hasil Skenario Simulasi": [f"{new_demand} unit", f"{new_inv} unit", f"{risk_scenario:.1f}%", f"IDR {profit_scenario:,.0f}"]
        })
        st.dataframe(sim_data, use_container_width=True, hide_index=True)
        
        if risk_scenario > 30:
            st.markdown("""
            <div class="warning-card">
                <p style="margin: 0; font-weight: 700;">Deteksi Risiko Strategis Tinggi</p>
                <p style="margin: 0; margin-top: 5px;">Skenario dengan parameter ini mengindikasikan kerentanan rantai pasok yang parah. Anda disarankan untuk segera melakukan diversifikasi pemasok (supplier) untuk mitigasi risiko.</p>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 4: CASH FLOW ---
    with tab4:
        st.markdown("<div class='section-title'>Dampak Proyeksi Pengadaan Terhadap Arus Kas (Cash Flow)</div>", unsafe_allow_html=True)
        st.write(f"**Total Anggaran Operasional Tersedia:** IDR {st.session_state['cash_budget']:,.0f}")
        
        shortage = max(0, base_demand - cat_data['Current Stock'] + cat_data['Safety Stock'])
        purchasing_cost = shortage * cat_data['Unit Cost (IDR)']
        remaining_cash = st.session_state['cash_budget'] - purchasing_cost
        
        cash_flow_data = pd.DataFrame({
            "Deskripsi Transaksi Eksekusi": ["Kebutuhan Restock Berdasarkan AI", "Estimasi Total Biaya Pengadaan", "Proyeksi Sisa Anggaran Arus Kas"],
            "Nilai Eksekusi": [f"{shortage} unit", f"IDR {purchasing_cost:,.0f}", f"IDR {remaining_cash:,.0f}"]
        })
        st.dataframe(cash_flow_data, use_container_width=True, hide_index=True)
        
        if remaining_cash < 0:
            st.markdown(f"""
            <div class="warning-card">
                <p style="margin-bottom: 5px; font-weight: 700;">Deteksi Defisit Likuiditas</p>
                <p style="margin: 0;">Sistem mengidentifikasi bahwa skala pengadaan ini akan melampaui plafon anggaran yang dialokasikan (Defisit IDR {abs(remaining_cash):,.0f}). Pertimbangkan untuk merestrukturisasi pesanan menjadi beberapa fase atau renegosiasi syarat pembayaran dengan pihak pemasok.</p>
            </div>
            """, unsafe_allow_html=True)
        elif remaining_cash < (st.session_state['cash_budget'] * 0.2):
            st.markdown("""
            <div class="warning-card" style="border-color: #F59E0B; background-color: #FFFBEB;">
                <p style="margin: 0; font-weight: 700;">Peringatan Margin Likuiditas Tipis</p>
                <p style="margin: 0; margin-top: 5px;">Rasio arus kas pasca-pengadaan akan menurun signifikan. Sangat disarankan untuk menangguhkan seluruh belanja modal (Capital Expenditure) yang tidak bersifat krusial untuk menjaga stabilitas operasional.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-card">
                <p style="margin: 0; font-weight: 700;">Validasi Kelayakan Finansial Sukses</p>
                <p style="margin: 0; margin-top: 5px;">Posisi likuiditas berada dalam ambang batas yang dikonfigurasi. Anda dapat melanjutkan eksekusi dokumen pengadaan tanpa memicu gangguan pada struktur arus kas bisnis.</p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# 9. HALAMAN: CONFIGURATION
# =========================================================
elif menu == "Config AI":
    st.markdown('<div class="page-title">Sistem Konfigurasi Global</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <p><strong>Informasi Halaman:</strong> Atur parameter fundamental bisnis (Business Constraints) yang digunakan oleh mesin algoritma AI. <strong>Forecast Horizon</strong> menentukan panjang periode prediksi ke depan. <strong>Waktu Pengiriman Supplier</strong> digunakan dalam logika perhitungan tanggal rekomendasi pemesanan. <strong>Anggaran Kas</strong> berfungsi sebagai garis dasar untuk validasi mitigasi risiko pada modul Proyeksi Arus Kas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Parameter Kendali Operasional</div>', unsafe_allow_html=True)
    
    # Memastikan layout tidak bertabrakan dengan CSS global
    with st.container(border=False):
        c1, c2 = st.columns(2)
        with c1:
            st.session_state['horizon'] = st.number_input("Forecast Horizon (Hari)", min_value=7, max_value=365, value=st.session_state['horizon'], step=1)
            st.session_state['lead_time'] = st.number_input("Waktu Pengiriman Supplier (Hari)", min_value=1, max_value=90, value=st.session_state['lead_time'])
        with c2:
            st.session_state['cash_budget'] = st.number_input("Anggaran Kas Operasional Maksimal (IDR)", min_value=0, value=st.session_state['cash_budget'], step=1000000)
        
    st.markdown("""
    <div class="success-card">
        <p style="margin: 0; font-weight: 700;">Sinkronisasi Parameter Aktif</p>
        <p style="margin: 0; margin-top: 5px;">Sistem terhubung secara komprehensif. Pembaruan variabel di atas telah diterapkan secara instan ke seluruh perhitungan matematis pada Executive Overview, Modul Preskriptif, dan Digital Twin Simulator.</p>
    </div>
    """, unsafe_allow_html=True)
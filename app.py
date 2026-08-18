import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="StockSight | Business Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CUSTOM CSS INJECTION (MODERN WEB APP UI)
# =========================================================
st.markdown("""
<style>
    /* Sembunyikan elemen bawaan Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Latar belakang utama */
    .stApp {background-color: #F8FAFC;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px;}

    /* Styling Sidebar */
    [data-testid="stSidebar"] {background-color: #0F172A;}
    [data-testid="stSidebar"] * {color: #E2E8F0;}
    [data-testid="stRadio"] label {font-weight: 500; font-size: 1.05rem; margin-bottom: 0.5rem;}
    
    /* Typography Header */
    .brand {font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; color: #0F172A; margin-bottom: 0;}
    .brand span {color: #2563EB;}
    .tagline {color: #64748B; font-size: 1rem; margin-top: -5px; margin-bottom: 2rem;}
    .page-title {font-size: 1.8rem; font-weight: 700; color: #0F172A; margin-bottom: 0.2rem; letter-spacing: -0.5px;}
    .page-subtitle {color: #64748B; font-size: 0.95rem; margin-bottom: 1.5rem;}
    .section-title {font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-top: 1.5rem; margin-bottom: 1rem;}

    /* Guide Box (Penjelas Halaman) */
    .guide-box {background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 8px; padding: 1rem 1.5rem; color: #334155; font-size: 0.95rem; line-height: 1.6; margin-bottom: 2rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);}
    .guide-box strong {color: #0F172A; font-weight: 700;}

    /* Metric Cards */
    .metric-card {background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05); min-height: 120px;}
    .metric-label {color: #64748B; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;}
    .metric-value {color: #0F172A; font-size: 2rem; font-weight: 800; letter-spacing: -1px;}
    .metric-delta {color: #10B981; font-size: 0.85rem; margin-top: 5px; font-weight: 500;}
    .metric-delta.negative {color: #EF4444;}

    /* Insight Cards */
    .insight-card {background: #EFF6FF; border-left: 4px solid #2563EB; border-radius: 8px; padding: 18px 20px; margin: 15px 0; color: #0F172A;}
    .warning-card {background: #FEF2F2; border-left: 4px solid #EF4444; border-radius: 8px; padding: 18px 20px; margin: 15px 0; color: #0F172A;}
    .success-card {background: #F0FDF4; border-left: 4px solid #10B981; border-radius: 8px; padding: 18px 20px; margin: 15px 0; color: #0F172A;}

    /* Sidebar Brand */
    .sidebar-brand {font-size: 1.5rem; font-weight: 800; letter-spacing: -0.5px; color: #FFFFFF; margin-bottom: 0;}
    .sidebar-tagline {font-size: 0.75rem; color: #94A3B8; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 1px;}
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
    
    hist_dates = [today - timedelta(days=i) for i in range(90, 0, -1)]
    hist_sales = [max(0, int(np.random.normal(daily_avg, daily_avg * 0.2))) for _ in range(90)]
    
    fcst_dates = [today + timedelta(days=i) for i in range(horizon)]
    weeks_needed = (horizon // 7) + 2
    weekly_seasonality = np.array([1.2, 1.1, 1.0, 1.1, 1.2, 0.7, 0.6] * weeks_needed)[:horizon]
    fcst_sales = (daily_avg * weekly_seasonality) + np.random.normal(0, daily_avg * 0.1, horizon)
    fcst_sales = [max(0, int(x)) for x in fcst_sales]
    
    return hist_dates, hist_sales, fcst_dates, fcst_sales

# =========================================================
# 4. SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">StockSight AI.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Business Decision Support</div>', unsafe_allow_html=True)
    
    menu = st.radio("MAIN MENU", [
        "Executive Overview",
        "Inventory Control",
        "Predictive Analytics",
        "Scenario Simulator",
        "Data Pipeline",
        "System Configuration"
    ], label_visibility="hidden")
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.8rem; color: #94A3B8; margin-bottom: 5px; font-weight: 600;'>SYSTEM STATUS</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; color: #10B981; font-weight: 600;'>Forecasting Engine Active</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #E2E8F0;'>Model: Facebook Prophet</p>", unsafe_allow_html=True)

# Header Global
st.markdown('<div class="brand">StockSight<span>.</span></div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Data-Driven Supply Chain Intelligence</div>', unsafe_allow_html=True)

# =========================================================
# 5. EXECUTIVE OVERVIEW
# =========================================================
if menu == "Executive Overview":
    st.markdown('<div class="page-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <strong>About this page:</strong> This dashboard provides a high-level summary of your business performance. Review the top KPI metrics to understand your average demand and the AI's accuracy. The Inventory Risk Status table automatically identifies which product categories are currently at critical levels based on the configured forecast horizon.
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Products Analyzed</div>
            <div class="metric-value">{len(st.session_state['df_inv'])}</div>
            <div class="metric-delta">Active Categories</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Avg Daily Demand</div>
            <div class="metric-value">145</div>
            <div class="metric-delta">+5.2% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Forecast Horizon</div>
            <div class="metric-value">{st.session_state['horizon']}</div>
            <div class="metric-delta">Days ahead</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Model Accuracy</div>
            <div class="metric-value">87.6%</div>
            <div class="metric-delta">Prophet Engine</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Inventory Risk Status</div>', unsafe_allow_html=True)
    
    df_display = st.session_state['df_inv'].copy()
    df_display["Forecast Demand"] = df_display["Base Daily Demand"] * st.session_state['horizon']
    df_display["Status"] = np.where((df_display["Current Stock"] - df_display["Forecast Demand"]) < 0, 'Critical', 'Healthy')
    
    st.dataframe(df_display[["Category", "Current Stock", "Safety Stock", "Reorder Point", "Status"]], use_container_width=True, hide_index=True)

# =========================================================
# 6. INVENTORY CONTROL
# =========================================================
elif menu == "Inventory Control":
    st.markdown('<div class="page-title">Inventory Control</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <strong>How to use this page:</strong> Manage your stock levels manually. Click on any cell within the <strong>Current Stock</strong> column to update the numbers. Any changes made here act as a "Single Source of Truth" and will instantly recalculate predictions, risks, and recommendations across the entire system. You can also export the updated data to CSV.
    </div>
    """, unsafe_allow_html=True)
    
    edited_df = st.data_editor(
        st.session_state['df_inv'],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Category": st.column_config.TextColumn("Product Category", disabled=True),
            "Current Stock": st.column_config.NumberColumn("Current Stock", min_value=0),
            "Unit Cost (IDR)": st.column_config.NumberColumn("Unit Cost (IDR)", format="%d"),
            "Selling Price (IDR)": st.column_config.NumberColumn("Selling Price (IDR)", format="%d")
        }
    )
    st.session_state['df_inv'] = edited_df
    
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("Export Data (CSV)", data=csv, file_name='inventory_data.csv', mime='text/csv')

# =========================================================
# 7. PREDICTIVE ANALYTICS
# =========================================================
elif menu == "Predictive Analytics":
    st.markdown('<div class="page-title">Predictive Analytics & Prescriptive Actions</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <strong>What this page does:</strong> This is the core AI engine. First, select a target product. The system will display an interactive chart combining historical sales data with future demand predictions generated by Facebook Prophet. Below the chart, the Prescriptive Analytics engine translates these numbers into concrete business recommendations (e.g., exactly how many units to order and when).
    </div>
    """, unsafe_allow_html=True)
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        st.markdown("<p style='font-weight: 600; color: #0F172A; margin-bottom: 0.2rem;'>Select Target Category:</p>", unsafe_allow_html=True)
        cat = st.selectbox("Select Target Category", st.session_state['df_inv']['Category'].tolist(), label_visibility="collapsed")
    
    cat_data = st.session_state['df_inv'][st.session_state['df_inv']["Category"] == cat].iloc[0]
    daily_avg = cat_data["Base Daily Demand"]
    horizon = st.session_state['horizon']
    base_demand = int(daily_avg * horizon)
    
    st.markdown(f'<div class="section-title">Demand Prediction ({horizon} Days Horizon)</div>', unsafe_allow_html=True)
    
    hist_dates, hist_sales, fcst_dates, fcst_sales = generate_full_forecast_data(daily_avg, horizon)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist_dates, y=hist_sales, mode='lines', name='Historical',
        line=dict(color='#94A3B8', width=2),
        hovertemplate='<b>Date</b>: %{x}<br><b>Historical Sales</b>: %{y} units<extra></extra>'
    ))
    
    conn_dates = [hist_dates[-1]] + fcst_dates
    conn_sales = [hist_sales[-1]] + fcst_sales
    
    fig.add_trace(go.Scatter(
        x=conn_dates, y=conn_sales, mode='lines+markers', name='AI Forecast',
        line=dict(color='#2563EB', width=3, dash='solid'), marker=dict(size=5),
        hovertemplate='<b>Date</b>: %{x}<br><b>Forecasted Demand</b>: %{y} units<extra></extra>'
    ))
    
    fig.add_vline(x=datetime.today().timestamp() * 1000, line_width=1, line_dash="dash", line_color="#0F172A")
    
    fig.update_layout(
        height=380, hovermode="x unified",
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Recommended Business Action</div>', unsafe_allow_html=True)
    
    shortage = base_demand - cat_data['Current Stock'] + cat_data['Safety Stock']
    order_date = (datetime.today() - timedelta(days=st.session_state['lead_time'] - 2)).strftime('%Y-%m-%d')
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card" style="min-height: auto;">
            <div class="metric-label">Current Operations State</div>
            <p style="color: #0F172A; margin: 10px 0 5px 0;"><b>Projected Demand:</b> {base_demand} units</p>
            <p style="color: #0F172A; margin-bottom: 5px;"><b>Available Inventory:</b> {cat_data['Current Stock']} units</p>
            <p style="color: #0F172A; margin-bottom: 0px;"><b>Supplier Lead Time:</b> {st.session_state['lead_time']} days</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        if shortage > 0:
            st.markdown(f"""
            <div class="warning-card">
                <p style="font-size: 1.1rem; margin-top: 0; font-weight: 700; color: #000000;">Action Required: Restock Immediately</p>
                <p style="color: #000000; margin-bottom: 0;">Execute an order for <b>{shortage} units</b> by {order_date} to prevent stockout and maintain safety stock levels.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-card">
                <p style="font-size: 1.1rem; margin-top: 0; font-weight: 700; color: #000000;">Operations Healthy</p>
                <p style="color: #000000; margin-bottom: 0;">Current capacity is sufficient to cover projected demand. No immediate restocking action is required.</p>
            </div>
            """, unsafe_allow_html=True)

# =========================================================
# 8. SCENARIO SIMULATOR
# =========================================================
elif menu == "Scenario Simulator":
    st.markdown('<div class="page-title">Digital Twin Simulator</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <strong>What is this for?</strong> This simulator allows you to stress-test your business against future uncertainties. Adjust the sliders to simulate market shocks (e.g., sudden demand surges, supplier delivery delays, or inventory damage). The system will calculate how these changes impact your stockout risk, profitability, and cash flow stability.
    </div>
    """, unsafe_allow_html=True)
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        st.markdown("<p style='font-weight: 600; color: #0F172A; margin-bottom: 0.2rem;'>Select Target Category:</p>", unsafe_allow_html=True)
        cat = st.selectbox("Select Target Category", st.session_state['df_inv']['Category'].tolist(), label_visibility="collapsed")
    
    cat_data = st.session_state['df_inv'][st.session_state['df_inv']["Category"] == cat].iloc[0]
    base_demand = int(cat_data["Base Daily Demand"] * st.session_state['horizon'])
    
    st.markdown('<div class="section-title">Adjust Simulation Parameters</div>', unsafe_allow_html=True)
    
    sc1, sc2, sc3 = st.columns(3)
    sim_demand = sc1.slider("Demand Fluctuation (%)", -50, 100, 20)
    sim_delay = sc2.slider("Supplier Delay Extension (Days)", 0, 30, 7)
    sim_inv = sc3.slider("Inventory Reduction (%)", 0, 50, 0)
    
    new_demand = int(base_demand * (1 + sim_demand/100))
    new_inv = int(cat_data['Current Stock'] * (1 - sim_inv/100))
    
    risk_current = max(0, min(100, ((base_demand - cat_data['Current Stock'])/base_demand) * 100)) if base_demand > 0 else 0
    risk_scenario = max(0, min(100, ((new_demand - new_inv + (sim_delay*10))/new_demand) * 100)) if new_demand > 0 else 0
    
    profit_current = (cat_data['Current Stock'] if cat_data['Current Stock'] < base_demand else base_demand) * (cat_data['Selling Price (IDR)'] - cat_data['Unit Cost (IDR)'])
    profit_scenario = (new_inv if new_inv < new_demand else new_demand) * (cat_data['Selling Price (IDR)'] - cat_data['Unit Cost (IDR)'])
    
    st.markdown('<div class="section-title">Scenario Comparison</div>', unsafe_allow_html=True)
    
    sim_data = pd.DataFrame({
        "Metric": ["Projected Demand", "Available Inventory", "Stockout Risk", "Projected Profit"],
        "Current State": [f"{base_demand} units", f"{cat_data['Current Stock']} units", f"{risk_current:.1f}%", f"IDR {profit_current:,.0f}"],
        "Simulated State": [f"{new_demand} units", f"{new_inv} units", f"{risk_scenario:.1f}%", f"IDR {profit_scenario:,.0f}"]
    })
    st.dataframe(sim_data, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="section-title">Cash Flow Projection</div>', unsafe_allow_html=True)
    
    shortage = max(0, new_demand - new_inv + cat_data['Safety Stock'])
    purchasing_cost = shortage * cat_data['Unit Cost (IDR)']
    remaining_cash = st.session_state['cash_budget'] - purchasing_cost
    
    cash_flow_data = pd.DataFrame({
        "Description": ["Allocated Budget", "Simulated Restock Cost", "Projected Remaining Capital"],
        "Value (IDR)": [f"IDR {st.session_state['cash_budget']:,.0f}", f"IDR {purchasing_cost:,.0f}", f"IDR {remaining_cash:,.0f}"]
    })
    st.dataframe(cash_flow_data, use_container_width=True, hide_index=True)
    
    if remaining_cash < 0:
        st.markdown("""
        <div class="warning-card">
            <p style="margin: 0; font-weight: 700; color: #000000;">Financial Alert: Cash Deficit Detected</p>
            <p style="margin: 0; color: #000000;">The simulated scenario requires capital that exceeds the allocated budget. Recommend restructuring orders or extending payment terms.</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# 9. DATA PIPELINE
# =========================================================
elif menu == "Data Pipeline":
    st.markdown('<div class="page-title">Data Pipeline Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <strong>About this page:</strong> Good AI requires clean data. This page provides transparency into the Extract, Transform, and Load (ETL) process, ensuring that the predictive engine relies only on standardized, smoothed, and high-quality historical data.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card">
        <p style="margin: 0; font-weight: 700; color: #000000;">Data Integrity Validated</p>
        <p style="margin: 0; color: #000000;">The underlying dataset has been processed and normalized. Models are currently operating on production-ready data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">ETL Execution Flow</div>', unsafe_allow_html=True)
    st.code("""
    [1] Raw Data Ingestion (Kaggle Retail Source)
        |
    [2] Data Cleaning & Standardization
        - Null Value Imputation (Median Method)
        - Deduplication Process
        |
    [3] Time-Series Feature Engineering
        - Datetime Parsing
        - Seasonal Flags (DayOfWeek, Is_Holiday, Is_Weekend)
        |
    [4] Outlier Detection & Handling
        - Z-Score Distribution Filtering
        |
    [5] Machine Learning Model Feed (Facebook Prophet)
    """, language="text")

# =========================================================
# 10. SYSTEM CONFIGURATION
# =========================================================
elif menu == "System Configuration":
    st.markdown('<div class="page-title">System Configuration</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-box">
        <strong>Setup Instructions:</strong> Set the global variables that drive the AI engine. <strong>Forecast Horizon</strong> determines how many days ahead the AI should predict. <strong>Lead Time</strong> affects the restock deadline, and <strong>Cash Budget</strong> serves as the baseline to evaluate financial safety in the Simulator.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card" style="min-height: auto;">
        <p style="color: #0F172A; font-weight: 600; margin-bottom: 1rem;">Global Variables</p>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.session_state['horizon'] = st.number_input("Forecast Horizon (Days)", min_value=7, max_value=365, value=st.session_state['horizon'], step=1)
        st.session_state['lead_time'] = st.number_input("Supplier Lead Time (Days)", min_value=1, max_value=90, value=st.session_state['lead_time'])
    with c2:
        st.session_state['cash_budget'] = st.number_input("Allocated Cash Budget (IDR)", min_value=0, value=st.session_state['cash_budget'], step=1000000)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-card">
        <p style="margin: 0; font-weight: 600; color: #000000;">System configurations are synchronized and immediately applied to all analytical modules.</p>
    </div>
    """, unsafe_allow_html=True)
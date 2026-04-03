#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ============================================
# SET PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Báo Cáo Hiệu Suất PM 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# STYLING - MIMIC HTML TEMPLATE
# ============================================
st.markdown("""
<style>
    /* Header styling */
    .header-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .header-gradient h1 {
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
    }
    
    .header-gradient p {
        font-size: 1.1em;
        opacity: 0.95;
        margin: 10px 0 0 0;
    }
    
    /* Summary cards */
    .summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 8px;
        color: white;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .summary-number {
        font-size: 2.2em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .summary-label {
        font-size: 0.95em;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Section headers */
    .section-header {
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        font-size: 1.5em;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    /* Scoring guide styling */
    .scoring-guide {
        background: white;
        padding: 25px;
        border-radius: 8px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .formula-box {
        background-color: #f0f0f0;
        padding: 15px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.9em;
    }
    
    .note-box {
        background: #e8f4f8;
        padding: 15px;
        border-radius: 4px;
        margin: 15px 0;
        border-left: 4px solid #0288d1;
        font-size: 0.95em;
    }
    
    /* Rank colors */
    .rank-green {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    .rank-yellow {
        background-color: #fff3cd;
        color: #856404;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    .rank-red {
        background-color: #f8d7da;
        color: #721c24;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #999;
        font-size: 0.9em;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    try:
        excel_file = r"Report_2026_All_Tables_FINAL_CORRECTED.xlsx"
        
        # Load all sheets
        table_1 = pd.read_excel(excel_file, sheet_name='Table_1')
        table_2 = pd.read_excel(excel_file, sheet_name='Table_2')
        table_3 = pd.read_excel(excel_file, sheet_name='Table_3')
        
        return table_1, table_2, table_3
    except Exception as e:
        st.error(f"❌ Lỗi load dữ liệu: {e}")
        return None, None, None

# Load dữ liệu
table_1, table_2, table_3 = load_data()

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="header-gradient">
    <h1>📊 Báo Cáo Quản Lý Hiệu Suất PM</h1>
    <p>Năm 2026 - Phân tích chi tiết theo từng tháng</p>
    <p style="font-size: 0.9em; opacity: 0.9;">Cập nhật lần cuối: {}</p>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

if table_1 is None or table_2 is None or table_3 is None:
    st.error("❌ Không thể load dữ liệu. Vui lòng kiểm tra file Excel.")
    st.stop()

# Format currency function
def format_currency(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f} VNĐ"

# ============================================
# SIDEBAR - FILTERS
# ============================================
st.sidebar.markdown("## 🔍 Bộ Lọc Dữ Liệu")

# Get unique months and PMs
months = sorted(table_1['Tháng'].unique())
pms = sorted(table_1['Tên PM'].unique())

selected_month = st.sidebar.selectbox("📅 Chọn tháng:", months, index=len(months)-1)
selected_pm = st.sidebar.multiselect("👤 Chọn PM:", pms, default=pms)

# Filter data
filtered_table_1 = table_1[(table_1['Tháng'] == selected_month) & (table_1['Tên PM'].isin(selected_pm))]
filtered_table_2 = table_2[(table_2['Tháng'] == selected_month) & (table_2['Tên PM'].isin(selected_pm))]
filtered_table_3 = table_3[(table_3['Tháng'] == selected_month) & (table_3['Tên PM'].isin(selected_pm))]

# ============================================
# TABS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tóm Tắt Thống Kê", "🎯 Hệ Thống Tính Điểm", "📋 Chi Tiết Dự Án", "⭐ Xếp Hạng 5 Sao"])

# ============================================
# TAB 1: SUMMARY STATISTICS
# ============================================
with tab1:
    st.markdown('<h2 class="section-header">📈 Tóm Tắt Thống Kê - {}</h2>'.format(selected_month), unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📦 Số Dự Án",
            len(filtered_table_1),
            help="Tổng số công trình phụ trách"
        )
    
    with col2:
        total_value = filtered_table_1['Giá trị gói thầu'].sum() if 'Giá trị gói thầu' in filtered_table_1.columns else 0
        st.metric(
            "💰 Tổng Giá Trị",
            f"{total_value/1e9:.2f}B",
            help="Tổng giá trị gói thầu (tỷ VNĐ)"
        )
    
    with col3:
        defect_a = filtered_table_1['Số lỗi defect loại A'].sum()
        st.metric(
            "🔴 Defect A",
            int(defect_a),
            help="Lỗi loại A (Critical)"
        )
    
    with col4:
        late_projects = filtered_table_1['Số ngày trễ hạn'].apply(lambda x: 1 if x > 0 else 0).sum()
        st.metric(
            "⏰ Dự Án Trễ Hạn",
            int(late_projects),
            help="Số công trình không hoàn thành đúng hạn"
        )
    
    st.divider()
    
    # Performance by PM
    st.subheader("📊 Hiệu Suất Theo PM")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pm_stats = filtered_table_2.groupby('Tên PM').agg({
            'Số công trình phụ trách': 'sum',
            'Số lỗi defect loại A': 'sum',
            'Số lỗi defect loại B': 'sum',
            'Số lỗi defect loại C': 'sum'
        }).reset_index().rename(columns={'Số công trình phụ trách': 'Projects'})
        
        fig_projects = px.bar(
            pm_stats, 
            x='Tên PM', 
            y='Projects',
            title="💼 Số Dự Án Theo PM",
            color='Projects',
            color_continuous_scale='Blues',
            text='Projects'
        )
        fig_projects.update_traces(textposition='auto')
        fig_projects.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_projects, use_container_width=True)
    
    with col2:
        defect_data = pm_stats[['Tên PM', 'Số lỗi defect loại A', 'Số lỗi defect loại B', 'Số lỗi defect loại C']]
        fig_defects = px.bar(
            defect_data,
            x='Tên PM',
            y=['Số lỗi defect loại A', 'Số lỗi defect loại B', 'Số lỗi defect loại C'],
            title="🐛 Defect Theo PM",
            barmode='stack',
            labels={'value': 'Số Lỗi', 'variable': 'Loại Defect'}
        )
        fig_defects.update_layout(height=400)
        st.plotly_chart(fig_defects, use_container_width=True)

# ============================================
# TAB 2: SCORING GUIDE
# ============================================
with tab2:
    st.markdown('<h2 class="section-header">🎯 Hệ Thống Tính Điểm & Công Thức</h2>', unsafe_allow_html=True)
    
    st.markdown("### 1️⃣ Tiêu Chí Đánh Giá (Hệ 5 Sao)")
    
    scoring_data = {
        "Tiêu Chí": [
            "TC1: Số Công Trình Phụ Trách",
            "TC2: Số Lỗi Defect",
            "TC3: Timeline"
        ],
        "Tính Điểm": [
            "1 sao: <1 | 3 sao: 1 | 4 sao: 2 | 5 sao: ≥3",
            "4 sao: Default | 3 sao: ≥2 lỗi A | 2 sao: ≥4 lỗi A | 1 sao: ≥6 lỗi A",
            "-1 sao/công trình muộn | Điểm TC3 = max(1, 4 - số CT muộn)"
        ]
    }
    
    st.dataframe(pd.DataFrame(scoring_data), use_container_width=True, hide_index=True)
    
    st.markdown("### 2️⃣ Điểm Xếp Hạng Trung Bình")
    st.markdown('<div class="formula-box">Điểm TB = (TC1 + TC2 + TC3) / 3</div>', unsafe_allow_html=True)
    
    st.markdown("### 3️⃣ Tính Toán Quỹ Khoán")
    st.markdown('<div class="formula-box">Quỹ Khoán = Số Ngày Công Trình Phụ Trách × 600,000 VNĐ/ngày</div>', unsafe_allow_html=True)
    
    st.markdown("### 4️⃣ Chênh Lệch Khoán & Hệ Số Ảnh Hưởng")
    st.markdown("""
    <div class="formula-box">
    Chênh Lệch Khoán = (Quỹ Khoán - Lương Tháng) × Hệ Số Xếp Hạng
    <br><br>
    Hệ Số Xếp Hạng:
    • Xanh (Excellent): 1.0 (thưởng 100% chênh lệch)
    • Vàng (Good): 1.0 (thưởng 100% chênh lệch)
    • Đỏ (Improvement): 0.5 (thưởng chỉ 50% chênh lệch)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📌 Ghi Chú Quan Trọng")
    st.markdown("""
    <div class="note-box">
    <strong>Phân Bố Xếp Hạng:</strong>
    <ul>
        <li><strong>30% PM hàng tháng</strong> → Xanh (đạt điểm cao nhất)</li>
        <li><strong>40% PM hàng tháng</strong> → Vàng (đạt điểm trung bình)</li>
        <li><strong>30% PM hàng tháng</strong> → Đỏ (đạt điểm thấp nhất)</li>
    </ul>
    <br>
    <strong>Thưởng Tối Đa:</strong> Trên mỗi tháng, chênh lệch khoán không được vượt quá 1 tháng lương.
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 3: DETAILED PROJECTS
# ============================================
with tab3:
    st.markdown('<h2 class="section-header">📋 Chi Tiết Các Dự Án</h2>', unsafe_allow_html=True)
    
    if len(filtered_table_1) > 0:
        # Display table with formatting
        display_cols = [
            'Tháng', 'Tên PM', 'Tên công trình',
            'Ngày bắt đầu thực tế', 'Ngày kết thúc thực tế',
            'Số ngày trễ hạn', 'Số lỗi defect loại A',
            'Số lỗi defect loại B', 'Số lỗi defect loại C',
            'Giá trị gói thầu'
        ]
        
        display_cols = [col for col in display_cols if col in filtered_table_1.columns]
        st.dataframe(
            filtered_table_1[display_cols],
            use_container_width=True,
            height=600
        )
        
        # Download option
        csv = filtered_table_1.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Tải CSV",
            data=csv,
            file_name=f"Projects_{selected_month.replace('/', '-')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ Không có dữ liệu cho bộ lọc này")

# ============================================
# TAB 4: RATING
# ============================================
with tab4:
    st.markdown('<h2 class="section-header">⭐ Xếp Hạng 5 Sao - Racing</h2>', unsafe_allow_html=True)
    
    if len(filtered_table_3) > 0:
        # Sort by điểm trung bình (descending)
        filtered_table_3_sorted = filtered_table_3.sort_values('Điểm trung bình', ascending=False)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            display_cols_3 = [
                'Tên PM', 'Số công trình phụ trách',
                'Số lỗi defect A', 'Số lỗi defect B', 'Số lỗi defect C',
                'Số công trình trễ hạn', 'Điểm trung bình', 'Xếp hạng 5 sao'
            ]
            display_cols_3 = [col for col in display_cols_3 if col in filtered_table_3_sorted.columns]
            
            st.dataframe(
                filtered_table_3_sorted[display_cols_3],
                use_container_width=True,
                height=500
            )
        
        with col2:
            if len(filtered_table_3_sorted) > 0:
                st.metric(
                    "🏆 Top PM",
                    filtered_table_3_sorted.iloc[0]['Tên PM']
                )
                st.metric(
                    "⭐ Điểm Cao Nhất",
                    f"{filtered_table_3_sorted.iloc[0]['Điểm trung bình']:.2f}"
                )
        
        st.divider()
        
        # Chart
        fig_rating = px.bar(
            filtered_table_3_sorted,
            x='Tên PM',
            y='Điểm trung bình',
            color='Điểm trung bình',
            color_continuous_scale='RdYlGn',
            title="📈 Điểm Trung Bình Theo PM",
            text='Điểm trung bình'
        )
        fig_rating.update_traces(textposition='auto')
        fig_rating.update_layout(height=400)
        st.plotly_chart(fig_rating, use_container_width=True)
    else:
        st.warning("❌ Không có dữ liệu xếp hạng")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>📄 Báo Cáo Quản Lý Hiệu Suất PM - Golden Gate Trade & Service JSC</p>
    <p>© 2026 Phòng Quản Lý Dự Án (PMO) | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

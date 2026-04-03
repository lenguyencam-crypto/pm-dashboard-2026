# 📊 PM Hiệu Suất Dashboard 2026

**Báo Cáo Quản Lý Hiệu Suất PM - Golden Gate Trade & Service JSC**

## 🎯 Mô Tả

Ứng dụng Streamlit để theo dõi và báo cáo hiệu suất quản lý dự án (PM) theo hệ thống xếp hạng 5 sao. Hiển thị:

- **📈 Tóm Tắt Thống Kê**: Số dự án, giá trị, defect, tình hình trễ hạn
- **🎯 Hệ Thống Tính Điểm**: Giải thích chi tiết công thức tính điểm 5 sao, quỹ khoán
- **📋 Chi Tiết Dự Án**: Danh sách đầy đủ các công trình được phân tích
- **⭐ Xếp Hạng 5 Sao**: Bảng xếp hạng PM, điểm trung bình, biểu đồ hiệu suất

## 📋 Tính Năng

✅ **Lọc Dữ Liệu**: Chọn tháng, PM để xem kết quả  
✅ **Biểu Đồ Tương Tác**: Plotly charts cho phân tích visual  
✅ **Export Data**: Tải CSV cho báo cáo  
✅ **Responsive Design**: Hoạt động tốt trên desktop, tablet, mobile  
✅ **Real-time Updates**: Tự động cải tạo khi Excel file thay đổi  

## 🚀 How to Run

### Local Machine
```bash
cd "f:\Ondriver\Golden Gate Trade & Service JSC\Hien, Ta thi Thu - PMS-Hiệu suất\2. RSC\12. PMO\Phân tích"
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Cloud (Online)
1. Push code to GitHub
2. Deploy via [Streamlit Cloud](https://streamlit.io/cloud)
3. Share link with team

## 📁 Files

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `Report_2026_All_Tables_FINAL_CORRECTED.xlsx` - Source data
- `.streamlit/config.toml` - Streamlit configuration

## 📚 Data Source

Dữ liệu được load từ file Excel: `Report_2026_All_Tables_FINAL_CORRECTED.xlsx`

Bao gồm:
- **Table_1**: Chi tiết từng dự án (công trình)
- **Table_2**: Tóm tắt theo tháng và PM
- **Table_3**: Xếp hạng 5 sao và tính điểm

## 🎨 Styling

Sử dụng styling từ template HTML báo cáo gốc + Streamlit CSS customization

## 📝 Notes

- Ứng dụng tự động cache dữ liệu từ Excel
- Update tự động mỗi khi file Excel thay đổi
- Không cần tài khoản đăng nhập để xem

## 👨‍💻 Author

Created: April 2026  
Update: Latest

---

**📄 Golden Gate Trade & Service JSC - Phòng Quản Lý Dự Án (PMO)**

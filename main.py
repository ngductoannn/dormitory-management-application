#!/usr/bin/env python3
"""
HỆ THỐNG QUẢN LÝ KÝ TÚC XÁ SINH VIÊN (KTX MANAGEMENT SYSTEM)
Cơ sở dữ liệu: 10 Bảng quan hệ (sinhvien, phong, dangky_phong, hoadon, dichvu, sudung_dichvu, xe, luot_xe, khach, lan_tham)
Giao diện: Python Desktop GUI (Tkinter / TTK) + SQLite SQL
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from ui.main_window import MainWindow

def main():
    print("=" * 65)
    print("🏛️ ĐANG KHỞI CHẠY HỆ THỐNG QUẢN LÝ KÝ TÚC XÁ SINH VIÊN (KTX)...")
    print("=" * 65)
    
    db = DatabaseManager()
    print(f"✓ Cơ sở dữ liệu SQLite KTX đã sẵn sàng tại: {db.db_path}")

    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()

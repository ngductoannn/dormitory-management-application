import sqlite3
import os
from typing import Optional
from contextlib import contextmanager

DB_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DB_DIR)
DEFAULT_DB_PATH = os.path.join(PROJECT_DIR, "data", "student_management.db")

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

-- 1. BẢNG SINHVIEN
CREATE TABLE IF NOT EXISTS SINHVIEN (
    MaSV VARCHAR(20) PRIMARY KEY,
    SoCMT VARCHAR(20),
    NgaySinh DATE,
    Lop VARCHAR(50),
    QueQuan VARCHAR(100)
);

-- 2. BẢNG PHONG
CREATE TABLE IF NOT EXISTS PHONG (
    SoPhong VARCHAR(20) PRIMARY KEY,
    LoaiPhong VARCHAR(50),
    DonGia DECIMAL(12,2),
    SoNguoiToiDa INT
);

-- 3. BẢNG DANGKY_PHONG
CREATE TABLE IF NOT EXISTS DANGKY_PHONG (
    MaDKPHONG INTEGER PRIMARY KEY AUTOINCREMENT,
    MaSV VARCHAR(20) NOT NULL,
    SoPhong VARCHAR(20) NOT NULL,
    NgayBatDau DATE,
    NgayKetThuc DATE,
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV) ON DELETE CASCADE,
    FOREIGN KEY (SoPhong) REFERENCES PHONG(SoPhong) ON DELETE RESTRICT
);

-- 4. BẢNG HOADON
CREATE TABLE IF NOT EXISTS HOADON (
    MaHD INTEGER PRIMARY KEY AUTOINCREMENT,
    MaDKPHONG INT NOT NULL,
    Thang INT,
    Nam INT,
    TienPhong DECIMAL(12,2),
    TienDichVu DECIMAL(12,2),
    TongTien DECIMAL(12,2),
    TrangThai VARCHAR(30),
    CONSTRAINT UQ_HOADON_THANG UNIQUE (MaDKPHONG, Thang, Nam),
    FOREIGN KEY (MaDKPHONG) REFERENCES DANGKY_PHONG(MaDKPHONG) ON DELETE CASCADE
);

-- 5. BẢNG DICHVU
CREATE TABLE IF NOT EXISTS DICHVU (
    MaDV VARCHAR(20) PRIMARY KEY,
    TenDV VARCHAR(100),
    DonGia DECIMAL(12,2)
);

-- 6. BẢNG SUDUNG_DICHVU
CREATE TABLE IF NOT EXISTS SUDUNG_DICHVU (
    MaLanSD INTEGER PRIMARY KEY AUTOINCREMENT,
    MaSV VARCHAR(20) NOT NULL,
    MaDV VARCHAR(20) NOT NULL,
    ThoiDiemSD DATETIME,
    SoLuong INT,
    DonGiaApDung DECIMAL(12,2),
    ThanhTien DECIMAL(12,2),
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV) ON DELETE CASCADE,
    FOREIGN KEY (MaDV) REFERENCES DICHVU(MaDV) ON DELETE RESTRICT
);

-- 7. BẢNG KHACH
CREATE TABLE IF NOT EXISTS KHACH (
    SoCMT VARCHAR(20) PRIMARY KEY,
    TenKhach VARCHAR(100),
    NgaySinh DATE
);

-- 8. BẢNG LAN_THAM
CREATE TABLE IF NOT EXISTS LAN_THAM (
    MaLanTham INTEGER PRIMARY KEY AUTOINCREMENT,
    SoCMT VARCHAR(20) NOT NULL,
    MaSV VARCHAR(20) NOT NULL,
    NgayDen DATETIME,
    FOREIGN KEY (SoCMT) REFERENCES KHACH(SoCMT) ON DELETE CASCADE,
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV) ON DELETE CASCADE
);

-- 9. BẢNG XE
CREATE TABLE IF NOT EXISTS XE (
    MaXE VARCHAR(20) PRIMARY KEY,
    BienSo VARCHAR(20),
    LoaiXe VARCHAR(50),
    MaSV VARCHAR(20),
    NgayDangKy DATE,
    NgayHetHan DATE,
    DonGiaThang DECIMAL(12,2) DEFAULT 100000,
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV) ON DELETE CASCADE
);

-- 10. BẢNG LUOT_XE
CREATE TABLE IF NOT EXISTS LUOT_XE (
    MaLuotXe INTEGER PRIMARY KEY AUTOINCREMENT,
    MaXE VARCHAR(20) NOT NULL,
    ThoiGianGui DATETIME,
    ThoiGianLay DATETIME,
    SoTienPhatSinh DECIMAL(12,2),
    FOREIGN KEY (MaXE) REFERENCES XE(MaXE) ON DELETE CASCADE
);

-- =====================================================================
-- TRIGGERS KIỂM TRA RÀNG BUỘC NGHIỆP VỤ (SQLite Trigger syntax)
-- =====================================================================

-- 1. Ràng buộc: Số lượng sinh viên trong phòng không vượt quá SoNguoiToiDa
CREATE TRIGGER IF NOT EXISTS trg_Check_SoLuongPhong
BEFORE INSERT ON DANGKY_PHONG
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM DANGKY_PHONG WHERE SoPhong = NEW.SoPhong) >= (SELECT SoNguoiToiDa FROM PHONG WHERE SoPhong = NEW.SoPhong)
        THEN RAISE(ABORT, 'Loi: Phong nay da dat so nguoi toi da, khong the dang ky them!')
    END;
END;

-- 2. Ràng buộc: Mỗi sinh viên chỉ được đăng ký tối đa 2 xe vé tháng
CREATE TRIGGER IF NOT EXISTS trg_Check_MaxXeThang
BEFORE INSERT ON XE
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM XE WHERE MaSV = NEW.MaSV) >= 2
        THEN RAISE(ABORT, 'Loi: Moi sinh vien chi duoc phep dang ky toi da 2 xe ve thang!')
    END;
END;
"""

SAMPLE_DATA_SQL = """
-- 1. Phòng
INSERT INTO PHONG (SoPhong, LoaiPhong, DonGia, SoNguoiToiDa) VALUES
('P101', 'Phong 4 nguoi', 800000, 4),
('P102', 'Phong 6 nguoi', 600000, 6),
('P201', 'Phong 4 nguoi', 900000, 4),
('P202', 'Phong 6 nguoi', 650000, 6),
('P301', 'Phong 4 nguoi', 950000, 4),
('P302', 'Phong 6 nguoi', 650000, 6),
('P401', 'Phong 4 nguoi', 950000, 4),
('P402', 'Phong 6 nguoi', 700000, 6),
('P501', 'Phong 4 nguoi', 1000000, 4);

-- 2. Dịch vụ
INSERT INTO DICHVU (MaDV, TenDV, DonGia) VALUES
('DV001', 'Giat ui', 20000),
('DV002', 'Nuoc uong', 10000),
('DV003', 'Ve sinh phong', 30000),
('DV004', 'May giat', 15000),
('DV005', 'Nuoc uong dong chai', 8000),
('DV006', 'Ve sinh chan ga', 25000);

-- 3. Sinh viên (33 sinh viên)
INSERT INTO SINHVIEN (MaSV, SoCMT, NgaySinh, Lop, QueQuan) VALUES
('SV001', '038201001001', '2006-02-14', 'CNTT1', 'Thanh Hoa'),
('SV002', '038201001002', '2005-11-08', 'CNTT2', 'Ha Noi'),
('SV003', '038201001003', '2006-06-21', 'DTVT1', 'Nghe An'),
('SV004', '038201001004', '2005-09-30', 'CNTT1', 'Nam Dinh'),
('SV005', '038201001005', '2006-01-17', 'DTVT2', 'Hai Phong'),
('SV006', '038201001006', '2005-03-12', 'CNTT2', 'Thanh Hoa'),
('SV007', '038201001007', '2006-08-25', 'DTVT1', 'Ha Noi'),
('SV008', '038201001008', '2005-05-16', 'CNTT1', 'Nghe An'),
('SV009', '038201001009', '2006-10-02', 'DTVT2', 'Ninh Binh'),
('SV010', '038201001010', '2005-12-20', 'CNTT3', 'Hai Duong'),
('SV011', '038201001011', '2006-04-09', 'CNTT2', 'Thanh Hoa'),
('SV012', '038201001012', '2006-01-15', 'CNTT1', 'Nam Dinh'),
('SV013', '038201001013', '2005-07-22', 'CNTT3', 'Ha Noi'),
('SV014', '038201001014', '2006-03-30', 'DTVT1', 'Thanh Hoa'),
('SV015', '038201001015', '2005-11-12', 'DTVT2', 'Nghe An'),
('SV016', '038201001016', '2006-09-05', 'CNTT2', 'Hai Phong'),
('SV017', '038201001017', '2005-02-18', 'CNTT1', 'Quang Ninh'),
('SV018', '038201001018', '2006-05-24', 'CNTT3', 'Ninh Binh'),
('SV019', '038201001019', '2005-08-14', 'DTVT1', 'Thai Binh'),
('SV020', '038201001020', '2006-12-01', 'DTVT2', 'Bac Ninh'),
('SV021', '038201001021', '2005-04-19', 'CNTT2', 'Hung Yen'),
('SV022', '038201001022', '2006-07-08', 'CNTT1', 'Ha Tinh'),
('SV023', '038201001023', '2005-10-25', 'CNTT3', 'Vinh Phuc'),
('SV024', '038201001024', '2006-02-03', 'DTVT1', 'Phu Tho'),
('SV025', '038201001025', '2005-06-17', 'DTVT2', 'Thanh Hoa'),
('SV026', '038201001026', '2006-11-28', 'CNTT2', 'Ha Noi'),
('SV027', '038201001027', '2005-01-09', 'CNTT1', 'Nghe An'),
('SV028', '038201001028', '2006-08-16', 'CNTT3', 'Nam Dinh'),
('SV029', '038201001029', '2005-03-21', 'DTVT1', 'Hai Duong'),
('SV030', '038201001030', '2006-10-11', 'DTVT2', 'Quang Binh'),
('SV031', '038201001031', '2005-12-05', 'CNTT2', 'Thai Nguyen'),
('SV032', '038201001032', '2006-03-14', 'CNTT1', 'Hai Phong'),
('SV033', '038201001033', '2005-08-19', 'DTVT1', 'Nam Dinh');

-- 4. Đăng ký phòng
INSERT INTO DANGKY_PHONG (MaSV, SoPhong, NgayBatDau, NgayKetThuc) VALUES
('SV001', 'P101', '2026-08-15', '2027-01-15'),
('SV002', 'P101', '2026-08-15', '2027-05-30'),
('SV003', 'P102', '2026-09-01', '2026-12-31'),
('SV004', 'P201', '2026-09-01', '2027-06-30'),
('SV005', 'P102', '2026-09-01', '2027-02-28'),
('SV006', 'P202', '2026-09-01', '2027-06-30'),
('SV007', 'P202', '2026-10-01', '2027-01-31'),
('SV008', 'P301', '2026-09-01', '2027-08-31'),
('SV009', 'P301', '2026-09-15', '2027-03-15'),
('SV010', 'P202', '2026-09-15', '2027-06-30'),
('SV011', 'P301', '2026-10-01', '2026-12-31'),
('SV012', 'P201', '2026-09-01', '2027-01-31'),
('SV013', 'P201', '2026-09-01', '2027-06-30'),
('SV014', 'P302', '2026-08-01', '2026-11-30'),
('SV015', 'P302', '2026-09-01', '2027-05-15'),
('SV016', 'P302', '2026-09-01', '2027-06-30'),
('SV017', 'P302', '2026-10-15', '2027-04-15'),
('SV018', 'P401', '2026-09-01', '2027-01-15'),
('SV019', 'P401', '2026-09-01', '2027-06-30'),
('SV020', 'P401', '2026-10-01', '2027-03-31'),
('SV021', 'P402', '2026-09-01', '2027-06-30'),
('SV022', 'P402', '2026-09-01', '2026-12-31'),
('SV023', 'P402', '2026-09-01', '2027-05-30'),
('SV024', 'P402', '2026-09-15', '2027-02-15'),
('SV025', 'P402', '2026-09-15', '2027-06-30'),
('SV026', 'P501', '2026-09-01', '2027-01-31'),
('SV027', 'P501', '2026-09-01', '2027-06-30'),
('SV028', 'P501', '2026-10-01', '2027-04-30'),
('SV029', 'P501', '2026-09-15', '2027-06-30'),
('SV030', 'P101', '2026-09-15', '2026-12-15'),
('SV031', 'P102', '2026-10-01', '2027-05-31'),
('SV032', 'P101', '2026-09-01', '2026-09-20'),
('SV032', 'P201', '2026-09-21', '2027-06-30'),
('SV033', 'P102', '2026-10-01', '2026-10-22'),
('SV033', 'P301', '2026-10-23', '2027-06-30');

-- 5. Hóa đơn
INSERT INTO HOADON (MaDKPHONG, Thang, Nam, TienPhong, TienDichVu, TongTien, TrangThai) VALUES
(1, 8, 2026, 800000, 100000, 900000, 'Da thanh toan'),
(1, 9, 2026, 800000, 120000, 920000, 'Da thanh toan'),
(1, 10, 2026, 800000, 135000, 935000, 'Chua thanh toan'),
(2, 8, 2026, 800000, 80000, 880000, 'Da thanh toan'),
(2, 9, 2026, 800000, 90000, 890000, 'Chua thanh toan'),
(2, 10, 2026, 800000, 110000, 910000, 'Da thanh toan'),
(3, 9, 2026, 600000, 150000, 750000, 'Da thanh toan'),
(3, 10, 2026, 600000, 95000, 695000, 'Chua thanh toan'),
(4, 9, 2026, 900000, 80000, 980000, 'Da thanh toan'),
(4, 10, 2026, 900000, 125000, 1025000, 'Da thanh toan'),
(5, 9, 2026, 600000, 50000, 650000, 'Da thanh toan'),
(6, 9, 2026, 650000, 70000, 720000, 'Da thanh toan'),
(7, 10, 2026, 650000, 85000, 735000, 'Chua thanh toan'),
(8, 9, 2026, 950000, 120000, 1070000, 'Da thanh toan'),
(9, 10, 2026, 950000, 60000, 1010000, 'Chua thanh toan'),
(10, 10, 2026, 650000, 95000, 745000, 'Da thanh toan'),
(11, 10, 2026, 950000, 110000, 1060000, 'Chua thanh toan'),
(12, 10, 2026, 900000, 50000, 950000, 'Da thanh toan'),
(13, 10, 2026, 900000, 110000, 1010000, 'Chua thanh toan'),
(14, 8, 2026, 650000, 45000, 695000, 'Da thanh toan'),
(15, 10, 2026, 650000, 80000, 730000, 'Chua thanh toan'),
(16, 10, 2026, 650000, 60000, 710000, 'Da thanh toan'),
(17, 10, 2026, 650000, 30000, 680000, 'Chua thanh toan'),
(18, 10, 2026, 950000, 120000, 1070000, 'Da thanh toan'),
(19, 10, 2026, 950000, 90000, 1040000, 'Da thanh toan'),
(20, 10, 2026, 950000, 40000, 990000, 'Chua thanh toan'),
(21, 10, 2026, 700000, 75000, 775000, 'Da thanh toan'),
(32, 9, 2026, 800000, 50000, 850000, 'Da thanh toan'),
(33, 9, 2026, 900000, 70000, 970000, 'Chua thanh toan'),
(34, 10, 2026, 600000, 40000, 640000, 'Da thanh toan'),
(35, 10, 2026, 950000, 60000, 1010000, 'Chua thanh toan');

-- 6. Sử dụng dịch vụ
INSERT INTO SUDUNG_DICHVU (MaSV, MaDV, ThoiDiemSD, SoLuong, DonGiaApDung, ThanhTien) VALUES
('SV001', 'DV001', '2026-08-20 09:30:00', 1, 20000, 20000),
('SV001', 'DV002', '2026-09-05 14:00:00', 3, 10000, 30000),
('SV001', 'DV001', '2026-09-12 09:30:00', 2, 20000, 40000),
('SV002', 'DV004', '2026-09-10 18:15:00', 2, 15000, 30000),
('SV003', 'DV003', '2026-09-12 10:00:00', 1, 30000, 30000),
('SV003', 'DV001', '2026-10-03 08:20:00', 3, 20000, 60000),
('SV004', 'DV002', '2026-10-07 12:00:00', 4, 10000, 40000),
('SV005', 'DV004', '2026-10-11 19:00:00', 1, 15000, 15000),
('SV006', 'DV001', '2026-09-06 10:00:00', 1, 20000, 20000),
('SV007', 'DV002', '2026-09-09 13:20:00', 2, 10000, 20000),
('SV008', 'DV003', '2026-09-14 09:00:00', 1, 30000, 30000),
('SV009', 'DV004', '2026-10-04 17:10:00', 2, 15000, 30000),
('SV010', 'DV005', '2026-10-09 11:30:00', 5, 8000, 40000),
('SV011', 'DV006', '2026-10-13 15:45:00', 2, 25000, 50000),
('SV012', 'DV001', '2026-10-02 08:30:00', 2, 20000, 40000),
('SV013', 'DV003', '2026-10-05 14:00:00', 1, 30000, 30000),
('SV015', 'DV004', '2026-10-08 09:15:00', 3, 15000, 45000),
('SV018', 'DV002', '2026-10-12 16:20:00', 5, 10000, 50000),
('SV021', 'DV006', '2026-10-15 10:45:00', 1, 25000, 25000),
('SV026', 'DV005', '2026-10-18 11:00:00', 4, 8000, 32000);

-- 7. Khách & Lần thăm
INSERT INTO KHACH (SoCMT, TenKhach, NgaySinh) VALUES
('079201002001', 'Nguyen Van An', '2004-04-12'),
('079201002002', 'Tran Thi Binh', '2005-07-19'),
('079201002003', 'Le Quang Huy', '2003-12-02'),
('079201002004', 'Pham Minh Duc', '2004-02-08'),
('079201002005', 'Do Thu Trang', '2005-05-27'),
('079201002006', 'Hoang Van Nam', '2004-09-10'),
('079201002007', 'Vu Thi Mai', '2005-01-25'),
('079201002008', 'Bui Van Hung', '2003-06-15'),
('079201002009', 'Nguyen Thi Lan', '2005-11-04');

INSERT INTO LAN_THAM (SoCMT, MaSV, NgayDen) VALUES
('079201002001', 'SV001', '2026-10-05 15:00:00'),
('079201002002', 'SV001', '2026-10-08 16:30:00'),
('079201002003', 'SV002', '2026-10-10 14:15:00'),
('079201002001', 'SV003', '2026-10-15 17:00:00'),
('079201002002', 'SV004', '2026-10-18 13:45:00'),
('079201002004', 'SV006', '2026-10-06 14:00:00'),
('079201002005', 'SV007', '2026-10-09 16:00:00'),
('079201002004', 'SV008', '2026-10-16 10:30:00'),
('079201002005', 'SV010', '2026-10-19 18:00:00'),
('079201002006', 'SV012', '2026-10-10 14:00:00'),
('079201002007', 'SV012', '2026-10-15 15:30:00'),
('079201002008', 'SV014', '2026-10-16 09:00:00'),
('079201002009', 'SV018', '2026-10-19 16:20:00'),
('079201002006', 'SV022', '2026-10-21 11:15:00');

-- 8. Xe & Lượt xe
INSERT INTO XE (MaXE, BienSo, LoaiXe, MaSV, NgayDangKy, NgayHetHan, DonGiaThang) VALUES
('XE001', '36B1-12345', 'Xe may', 'SV001', '2026-08-15', '2026-12-31', 100000),
('XE002', '36M1-23456', 'Xe dap dien', 'SV001', '2026-08-15', '2026-12-31', 100000),
('XE003', '29B1-34567', 'Xe may', 'SV002', '2026-09-01', '2026-12-31', 100000),
('XE004', '37M1-45678', 'Xe dap dien', 'SV003', '2026-09-01', '2026-11-30', 100000),
('XE005', '36B2-56789', 'Xe may', 'SV006', '2026-09-01', '2026-12-31', 100000),
('XE006', '36M2-67890', 'Xe dap dien', 'SV007', '2026-10-01', '2026-12-31', 100000),
('XE007', '30B2-78901', 'Xe may', 'SV008', '2026-09-01', '2026-11-30', 100000),
('XE008', '18B1-89012', 'Xe may', 'SV012', '2026-09-01', '2026-12-31', 100000),
('XE009', '29M1-90123', 'Xe dap dien', 'SV013', '2026-09-01', '2026-12-31', 100000),
('XE010', '37B1-01234', 'Xe may', 'SV015', '2026-09-01', '2026-12-31', 100000),
('XE011', '14B1-11223', 'Xe may', 'SV017', '2026-10-01', '2026-12-31', 100000),
('XE012', '99M1-33445', 'Xe dap dien', 'SV020', '2026-10-01', '2026-12-31', 100000);

INSERT INTO LUOT_XE (MaXE, ThoiGianGui, ThoiGianLay, SoTienPhatSinh) VALUES
('XE001', '2026-10-20 08:00:00', '2026-10-20 12:00:00', 0),
('XE001', '2026-10-20 18:00:00', '2026-10-21 08:00:00', 3000),
('XE002', '2026-10-20 07:30:00', '2026-10-20 17:30:00', 0),
('XE003', '2026-10-21 09:00:00', '2026-10-21 20:00:00', 0),
('XE004', '2026-10-21 19:00:00', '2026-10-22 07:00:00', 3000),
('XE005', '2026-10-20 07:45:00', '2026-10-20 17:15:00', 0),
('XE006', '2026-10-20 08:10:00', '2026-10-21 08:20:00', 3000),
('XE007', '2026-10-21 07:50:00', '2026-10-21 18:00:00', 0);
"""

class DatabaseManager:
    _instance = None

    def __new__(cls, db_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db_path = db_path or DEFAULT_DB_PATH
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(SCHEMA_SQL)
            cursor.execute("SELECT COUNT(*) FROM SINHVIEN;")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.executescript(SAMPLE_DATA_SQL)
            conn.commit()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def reset_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript("""
                DROP TRIGGER IF EXISTS trg_Check_SoLuongPhong;
                DROP TRIGGER IF EXISTS trg_Check_MaxXeThang;
                DROP TABLE IF EXISTS LAN_THAM;
                DROP TABLE IF EXISTS KHACH;
                DROP TABLE IF EXISTS LUOT_XE;
                DROP TABLE IF EXISTS XE;
                DROP TABLE IF EXISTS SUDUNG_DICHVU;
                DROP TABLE IF EXISTS DICHVU;
                DROP TABLE IF EXISTS HOADON;
                DROP TABLE IF EXISTS DANGKY_PHONG;
                DROP TABLE IF EXISTS PHONG;
                DROP TABLE IF EXISTS SINHVIEN;
            """)
            cursor.executescript(SCHEMA_SQL)
            cursor.executescript(SAMPLE_DATA_SQL)
            conn.commit()

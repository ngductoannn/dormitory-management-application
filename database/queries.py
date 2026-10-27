# SQL Queries Collection for Dormitory Student Management (Quản lý KTX Sinh viên)

# --- 1. SINHVIEN ---
SQL_GET_ALL_SINHVIEN = """
SELECT 
    sv.MaSV,
    sv.SoCMT,
    sv.NgaySinh,
    sv.Lop,
    sv.QueQuan,
    dk.SoPhong,
    p.LoaiPhong,
    p.DonGia AS DonGiaPhong
FROM SINHVIEN sv
LEFT JOIN DANGKY_PHONG dk ON sv.MaSV = dk.MaSV AND (dk.NgayKetThuc IS NULL OR dk.NgayKetThuc >= '2026-10-01')
LEFT JOIN PHONG p ON dk.SoPhong = p.SoPhong
GROUP BY sv.MaSV
ORDER BY sv.MaSV ASC;
"""

SQL_SEARCH_SINHVIEN = """
SELECT 
    sv.MaSV,
    sv.SoCMT,
    sv.NgaySinh,
    sv.Lop,
    sv.QueQuan,
    dk.SoPhong,
    p.LoaiPhong,
    p.DonGia AS DonGiaPhong
FROM SINHVIEN sv
LEFT JOIN DANGKY_PHONG dk ON sv.MaSV = dk.MaSV AND (dk.NgayKetThuc IS NULL OR dk.NgayKetThuc >= '2026-10-01')
LEFT JOIN PHONG p ON dk.SoPhong = p.SoPhong
WHERE 
    (:search = '' OR sv.MaSV LIKE :search_like OR sv.SoCMT LIKE :search_like OR sv.Lop LIKE :search_like OR sv.QueQuan LIKE :search_like)
    AND (:so_phong = 'Tất cả' OR dk.SoPhong = :so_phong)
GROUP BY sv.MaSV
ORDER BY sv.MaSV ASC;
"""

SQL_INSERT_SINHVIEN = """
INSERT INTO SINHVIEN (MaSV, SoCMT, NgaySinh, Lop, QueQuan)
VALUES (?, ?, ?, ?, ?);
"""

SQL_UPDATE_SINHVIEN = """
UPDATE SINHVIEN
SET SoCMT = ?, NgaySinh = ?, Lop = ?, QueQuan = ?
WHERE MaSV = ?;
"""

SQL_DELETE_SINHVIEN = """
DELETE FROM SINHVIEN WHERE MaSV = ?;
"""

# --- 2. PHÒNG & ĐĂNG KÝ PHÒNG ---
SQL_GET_ALL_PHONG = """
SELECT 
    p.SoPhong,
    p.LoaiPhong,
    p.DonGia,
    p.SoNguoiToiDa,
    COUNT(dk.MaDKPHONG) AS SoNguoiHienTai,
    (p.SoNguoiToiDa - COUNT(dk.MaDKPHONG)) AS SoChoTrong
FROM PHONG p
LEFT JOIN DANGKY_PHONG dk ON p.SoPhong = dk.SoPhong AND (dk.NgayKetThuc IS NULL OR dk.NgayKetThuc >= '2026-10-01')
GROUP BY p.SoPhong
ORDER BY p.SoPhong ASC;
"""

SQL_INSERT_PHONG = """
INSERT INTO PHONG (SoPhong, LoaiPhong, DonGia, SoNguoiToiDa)
VALUES (?, ?, ?, ?);
"""

SQL_DELETE_PHONG = """
DELETE FROM PHONG WHERE SoPhong = ?;
"""

SQL_GET_ALL_DANGKY_PHONG = """
SELECT 
    dk.MaDKPHONG,
    dk.MaSV,
    sv.Lop,
    dk.SoPhong,
    p.LoaiPhong,
    p.DonGia,
    dk.NgayBatDau,
    dk.NgayKetThuc
FROM DANGKY_PHONG dk
JOIN SINHVIEN sv ON dk.MaSV = sv.MaSV
JOIN PHONG p ON dk.SoPhong = p.SoPhong
ORDER BY dk.MaDKPHONG DESC;
"""

SQL_INSERT_DANGKY_PHONG = """
INSERT INTO DANGKY_PHONG (MaSV, SoPhong, NgayBatDau, NgayKetThuc)
VALUES (?, ?, ?, ?);
"""

SQL_DELETE_DANGKY_PHONG = """
DELETE FROM DANGKY_PHONG WHERE MaDKPHONG = ?;
"""

# --- 3. DỊCH VỤ & SỬ DỤNG DỊCH VỤ ---
SQL_GET_ALL_DICHVU = """
SELECT * FROM DICHVU ORDER BY MaDV ASC;
"""

SQL_GET_ALL_SUDUNG_DICHVU = """
SELECT 
    sd.MaLanSD,
    sd.MaSV,
    sv.Lop,
    sd.MaDV,
    dv.TenDV,
    sd.ThoiDiemSD,
    sd.SoLuong,
    sd.DonGiaApDung,
    sd.ThanhTien
FROM SUDUNG_DICHVU sd
JOIN SINHVIEN sv ON sd.MaSV = sv.MaSV
JOIN DICHVU dv ON sd.MaDV = dv.MaDV
ORDER BY sd.ThoiDiemSD DESC;
"""

SQL_INSERT_SUDUNG_DICHVU = """
INSERT INTO SUDUNG_DICHVU (MaSV, MaDV, ThoiDiemSD, SoLuong, DonGiaApDung, ThanhTien)
VALUES (?, ?, ?, ?, ?, ?);
"""

SQL_DELETE_SUDUNG_DICHVU = """
DELETE FROM SUDUNG_DICHVU WHERE MaLanSD = ?;
"""

# --- 4. HOÁ ĐƠN ---
SQL_GET_ALL_HOADON = """
SELECT 
    hd.MaHD,
    hd.MaDKPHONG,
    sv.MaSV,
    sv.Lop,
    dk.SoPhong,
    hd.Thang,
    hd.Nam,
    hd.TienPhong,
    hd.TienDichVu,
    hd.TongTien,
    hd.TrangThai
FROM HOADON hd
JOIN DANGKY_PHONG dk ON hd.MaDKPHONG = dk.MaDKPHONG
JOIN SINHVIEN sv ON dk.MaSV = sv.MaSV
WHERE (:thang = 0 OR hd.Thang = :thang)
  AND (:nam = 0 OR hd.Nam = :nam)
  AND (:trang_thai = 'Tất cả' OR hd.TrangThai = :trang_thai)
ORDER BY hd.Nam DESC, hd.Thang DESC, hd.MaHD DESC;
"""

SQL_INSERT_HOADON = """
INSERT INTO HOADON (MaDKPHONG, Thang, Nam, TienPhong, TienDichVu, TongTien, TrangThai)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SQL_UPDATE_TRANGTHAI_HOADON = """
UPDATE HOADON SET TrangThai = ? WHERE MaHD = ?;
"""

SQL_DELETE_HOADON = """
DELETE FROM HOADON WHERE MaHD = ?;
"""

# --- 5. XE & LƯỢT XE ---
SQL_GET_ALL_XE = """
SELECT 
    x.MaXE,
    x.BienSo,
    x.LoaiXe,
    x.MaSV,
    sv.Lop,
    x.NgayDangKy,
    x.NgayHetHan,
    x.DonGiaThang
FROM XE x
JOIN SINHVIEN sv ON x.MaSV = sv.MaSV
ORDER BY x.MaXE ASC;
"""

SQL_INSERT_XE = """
INSERT INTO XE (MaXE, BienSo, LoaiXe, MaSV, NgayDangKy, NgayHetHan, DonGiaThang)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

SQL_DELETE_XE = """
DELETE FROM XE WHERE MaXE = ?;
"""

SQL_GET_ALL_LUOT_XE = """
SELECT 
    lx.MaLuotXe,
    lx.MaXE,
    x.BienSo,
    x.LoaiXe,
    x.MaSV,
    sv.Lop,
    lx.ThoiGianGui,
    lx.ThoiGianLay,
    lx.SoTienPhatSinh
FROM LUOT_XE lx
JOIN XE x ON lx.MaXE = x.MaXE
JOIN SINHVIEN sv ON x.MaSV = sv.MaSV
ORDER BY lx.ThoiGianGui DESC;
"""

SQL_INSERT_LUOT_XE = """
INSERT INTO LUOT_XE (MaXE, ThoiGianGui, ThoiGianLay, SoTienPhatSinh)
VALUES (?, datetime('now'), NULL, ?);
"""

SQL_CHECKOUT_LUOT_XE = """
UPDATE LUOT_XE SET ThoiGianLay = datetime('now'), SoTienPhatSinh = ? WHERE MaLuotXe = ?;
"""

# --- 6. KHÁCH & LẦN THĂM ---
SQL_GET_ALL_LAN_THAM = """
SELECT 
    lt.MaLanTham,
    lt.SoCMT,
    k.TenKhach,
    k.NgaySinh,
    lt.MaSV,
    sv.Lop,
    dk.SoPhong,
    lt.NgayDen
FROM LAN_THAM lt
JOIN KHACH k ON lt.SoCMT = k.SoCMT
JOIN SINHVIEN sv ON lt.MaSV = sv.MaSV
LEFT JOIN DANGKY_PHONG dk ON sv.MaSV = dk.MaSV AND (dk.NgayKetThuc IS NULL OR dk.NgayKetThuc >= '2026-10-01')
ORDER BY lt.NgayDen DESC;
"""

SQL_INSERT_KHACH = """
INSERT OR IGNORE INTO KHACH (SoCMT, TenKhach, NgaySinh) VALUES (?, ?, ?);
"""

SQL_INSERT_LAN_THAM = """
INSERT INTO LAN_THAM (SoCMT, MaSV, NgayDen) VALUES (?, ?, datetime('now'));
"""

# --- 7. DASHBOARD TỔNG QUAN ---
SQL_GET_DASHBOARD_STATS = """
SELECT 
    (SELECT COUNT(*) FROM SINHVIEN) AS total_sinhvien,
    (SELECT COUNT(*) FROM PHONG) AS total_phong,
    (SELECT COUNT(*) FROM DANGKY_PHONG WHERE NgayKetThuc IS NULL OR NgayKetThuc >= '2026-10-01') AS total_dangky,
    (SELECT COALESCE(SUM(SoNguoiToiDa), 0) FROM PHONG) AS total_capacity,
    (SELECT COUNT(*) FROM XE) AS total_xe,
    (SELECT COALESCE(SUM(TongTien), 0) FROM HOADON WHERE TrangThai LIKE '%Da thanh toan%') AS revenue_paid,
    (SELECT COALESCE(SUM(TongTien), 0) FROM HOADON WHERE TrangThai NOT LIKE '%Da thanh toan%') AS revenue_unpaid;
"""

# =====================================================================
# 4 CÂU TRUY VẤN BÁO CÁO PROJECT
# =====================================================================

# Báo cáo 1: Tổng chi phí mỗi tháng của sinh viên (Tiền phòng + Tiền dịch vụ + Tiền vé xe + Phí gửi xe)
SQL_REPORT_1 = """
SELECT 
    SV.MaSV,
    SV.Lop,
    SV.QueQuan,
    HD.Thang,
    HD.Nam,
    COALESCE(HD.TienPhong, 0) AS TienPhong,
    COALESCE(HD.TienDichVu, 0) AS TienDichVuKhac,
    COALESCE(SUM(X.DonGiaThang), 0) AS TienVeXeThang,
    COALESCE(SUM(LX.SoTienPhatSinh), 0) AS TienPhatGuiXe,
    (COALESCE(HD.TongTien, 0) + COALESCE(SUM(X.DonGiaThang), 0) + COALESCE(SUM(LX.SoTienPhatSinh), 0)) AS TongChiPhiThang
FROM SINHVIEN SV
JOIN DANGKY_PHONG DKP ON SV.MaSV = DKP.MaSV
JOIN HOADON HD ON DKP.MaDKPHONG = HD.MaDKPHONG
LEFT JOIN XE X ON SV.MaSV = X.MaSV 
    AND CAST(strftime('%m', X.NgayDangKy) AS INT) <= HD.Thang 
    AND CAST(strftime('%Y', X.NgayDangKy) AS INT) <= HD.Nam
LEFT JOIN LUOT_XE LX ON X.MaXE = LX.MaXE 
    AND CAST(strftime('%m', LX.ThoiGianGui) AS INT) = HD.Thang 
    AND CAST(strftime('%Y', LX.ThoiGianGui) AS INT) = HD.Nam
GROUP BY SV.MaSV, SV.Lop, SV.QueQuan, HD.Thang, HD.Nam, HD.TienPhong, HD.TienDichVu, HD.TongTien
ORDER BY HD.Nam DESC, HD.Thang DESC, SV.MaSV;
"""

# Báo cáo 2: Sinh viên cùng tên dịch vụ, tổng giá trị mỗi dịch vụ sử dụng từ ngày 2026-09-01 đến 2026-10-31
SQL_REPORT_2 = """
SELECT 
    SV.MaSV,
    SV.Lop,
    DV.MaDV,
    DV.TenDV,
    SUM(SD.SoLuong) AS TongSoLuongSuDung,
    SUM(SD.ThanhTien) AS TongTienThanhToan
FROM SINHVIEN SV
JOIN SUDUNG_DICHVU SD ON SV.MaSV = SD.MaSV
JOIN DICHVU DV ON SD.MaDV = DV.MaDV
WHERE SD.ThoiDiemSD BETWEEN '2026-09-01 00:00:00' AND '2026-10-31 23:59:59'
GROUP BY SV.MaSV, SV.Lop, DV.MaDV, DV.TenDV
ORDER BY SV.MaSV;
"""

# Báo cáo 3: Sinh viên cùng thông tin khách đến thăm trong Tháng 10/2026, kèm số lần đến chơi
SQL_REPORT_3 = """
SELECT 
    SV.MaSV,
    SV.Lop,
    K.SoCMT,
    K.TenKhach,
    K.NgaySinh AS NgaySinhKhach,
    COUNT(LT.MaLanTham) AS SoLanDenChoi
FROM SINHVIEN SV
JOIN LAN_THAM LT ON SV.MaSV = LT.MaSV
JOIN KHACH K ON LT.SoCMT = K.SoCMT
WHERE CAST(strftime('%m', LT.NgayDen) AS INT) = 10 AND CAST(strftime('%Y', LT.NgayDen) AS INT) = 2026
GROUP BY SV.MaSV, SV.Lop, K.SoCMT, K.TenKhach, K.NgaySinh
ORDER BY SoLanDenChoi DESC;
"""

# Báo cáo 4: Danh mục dịch vụ cùng tổng doanh thu trong mỗi tháng
SQL_REPORT_4 = """
SELECT 
    DV.MaDV,
    DV.TenDV,
    CAST(strftime('%m', SD.ThoiDiemSD) AS INT) AS Thang,
    CAST(strftime('%Y', SD.ThoiDiemSD) AS INT) AS Nam,
    SUM(SD.SoLuong) AS TongSoLuongSuDung,
    SUM(SD.ThanhTien) AS TongDoanhThu
FROM DICHVU DV
JOIN SUDUNG_DICHVU SD ON DV.MaDV = SD.MaDV
GROUP BY DV.MaDV, DV.TenDV, CAST(strftime('%m', SD.ThoiDiemSD) AS INT), CAST(strftime('%Y', SD.ThoiDiemSD) AS INT)
ORDER BY Nam DESC, Thang DESC, TongDoanhThu DESC;
"""

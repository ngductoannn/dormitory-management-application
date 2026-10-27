from typing import List, Optional, Tuple, Dict, Any
from database.db_manager import DatabaseManager
from database import queries
from models.ktx_models import (
    SinhVien, Phong, DangKyPhong, HoaDon, DichVu, SuDungDichVu, Xe, LuotXe, LanTham
)

class KTXService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    # --- 1. SINHVIEN ---
    def get_all_sinhvien(self) -> List[SinhVien]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_SINHVIEN)
            return [SinhVien.from_row(r) for r in cursor.fetchall()]

    def search_sinhvien(self, search: str = "", so_phong: str = "Tất cả") -> List[SinhVien]:
        search_str = search.strip()
        search_like = f"%{search_str}%" if search_str else ""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_SEARCH_SINHVIEN, {
                "search": search_str,
                "search_like": search_like,
                "so_phong": so_phong
            })
            return [SinhVien.from_row(r) for r in cursor.fetchall()]

    def create_sinhvien(self, sv: SinhVien) -> Tuple[bool, str]:
        if not sv.MaSV.strip() or not sv.SoCMT.strip():
            return False, "Mã SV và Số CMT/CCCD không được để trống."
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_SINHVIEN, (
                    sv.MaSV.strip().upper(),
                    sv.SoCMT.strip(),
                    sv.NgaySinh.strip() if sv.NgaySinh else None,
                    sv.Lop.strip() if sv.Lop else None,
                    sv.QueQuan.strip() if sv.QueQuan else None
                ))
                conn.commit()
            return True, "Thêm sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def update_sinhvien(self, sv: SinhVien) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_UPDATE_SINHVIEN, (
                    sv.SoCMT.strip(),
                    sv.NgaySinh.strip() if sv.NgaySinh else None,
                    sv.Lop.strip() if sv.Lop else None,
                    sv.QueQuan.strip() if sv.QueQuan else None,
                    sv.MaSV.strip().upper()
                ))
                conn.commit()
            return True, "Cập nhật sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def delete_sinhvien(self, ma_sv: str) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_SINHVIEN, (ma_sv,))
                conn.commit()
            return True, "Xoá sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi xoá: {str(e)}"

    # --- 2. PHÒNG & ĐĂNG KÝ PHÒNG ---
    def get_all_phong(self) -> List[Phong]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_PHONG)
            return [Phong.from_row(r) for r in cursor.fetchall()]

    def create_phong(self, so_phong: str, loai_phong: str, don_gia: float, so_nguoi: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_PHONG, (so_phong.strip().upper(), loai_phong.strip(), don_gia, so_nguoi))
                conn.commit()
            return True, "Thêm phòng thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def delete_phong(self, so_phong: str) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_PHONG, (so_phong,))
                conn.commit()
            return True, "Xoá phòng thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def get_all_dangky_phong(self) -> List[DangKyPhong]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_DANGKY_PHONG)
            return [DangKyPhong.from_row(r) for r in cursor.fetchall()]

    def create_dangky_phong(self, ma_sv: str, so_phong: str, ngay_bd: str, ngay_kt: Optional[str]) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Trigger trg_Check_SoLuongPhong will automatically validate capacity!
                cursor.execute(queries.SQL_INSERT_DANGKY_PHONG, (
                    ma_sv.strip(), so_phong.strip(), ngay_bd.strip(), ngay_kt.strip() if ngay_kt else None
                ))
                conn.commit()
            return True, "Đăng ký phòng cho sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def delete_dangky_phong(self, ma_dk: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_DANGKY_PHONG, (ma_dk,))
                conn.commit()
            return True, "Huỷ đăng ký phòng thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    # --- 3. DỊCH VỤ & SỬ DỤNG DỊCH VỤ ---
    def get_all_dichvu(self) -> List[DichVu]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_DICHVU)
            return [DichVu.from_row(r) for r in cursor.fetchall()]

    def get_all_sudung_dichvu(self) -> List[SuDungDichVu]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_SUDUNG_DICHVU)
            return [SuDungDichVu.from_row(r) for r in cursor.fetchall()]

    def create_sudung_dichvu(self, ma_sv: str, ma_dv: str, so_luong: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DonGia FROM DICHVU WHERE MaDV = ?;", (ma_dv,))
                row = cursor.fetchone()
                if not row:
                    return False, "Không tìm thấy dịch vụ."
                don_gia = row[0]
                thanh_tien = don_gia * so_luong

                cursor.execute(queries.SQL_INSERT_SUDUNG_DICHVU, (
                    ma_sv, ma_dv, '2026-10-27 12:00:00', so_luong, don_gia, thanh_tien
                ))
                conn.commit()
            return True, f"Ghi nhận dịch vụ thành công! Thành tiền: {thanh_tien:,.0f} đ"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def delete_sudung_dichvu(self, ma_lan_sd: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_SUDUNG_DICHVU, (ma_lan_sd,))
                conn.commit()
            return True, "Xoá bản ghi thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    # --- 4. HOÁ ĐƠN ---
    def get_all_hoadon(self, thang: int = 0, nam: int = 0, trang_thai: str = "Tất cả") -> List[HoaDon]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_HOADON, {
                "thang": thang,
                "nam": nam,
                "trang_thai": trang_thai
            })
            return [HoaDon.from_row(r) for r in cursor.fetchall()]

    def create_hoadon(self, ma_dk: int, thang: int, nam: int, tien_phong: float, tien_dv: float) -> Tuple[bool, str]:
        tong = tien_phong + tien_dv
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_HOADON, (
                    ma_dk, thang, nam, tien_phong, tien_dv, tong, "Chua thanh toan"
                ))
                conn.commit()
            return True, "Lập hoá đơn thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def update_trangthai_hoadon(self, ma_hd: int, trang_thai: str) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_UPDATE_TRANGTHAI_HOADON, (trang_thai, ma_hd))
                conn.commit()
            return True, "Cập nhật hoá đơn thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def delete_hoadon(self, ma_hd: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_HOADON, (ma_hd,))
                conn.commit()
            return True, "Xoá hoá đơn thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    # --- 5. XE & LƯỢT XE ---
    def get_all_xe(self) -> List[Xe]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_XE)
            return [Xe.from_row(r) for r in cursor.fetchall()]

    def create_xe(self, ma_xe: str, bien_so: str, loai_xe: str, ma_sv: str, ngay_dk: str, ngay_hh: Optional[str], don_gia: float) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Trigger trg_Check_MaxXeThang will enforce max 2 vehicles per student!
                cursor.execute(queries.SQL_INSERT_XE, (
                    ma_xe.strip().upper(), bien_so.strip().upper(), loai_xe.strip(), ma_sv.strip(),
                    ngay_dk.strip(), ngay_hh.strip() if ngay_hh else None, don_gia
                ))
                conn.commit()
            return True, "Đăng ký xe thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def delete_xe(self, ma_xe: str) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_XE, (ma_xe,))
                conn.commit()
            return True, "Xoá xe thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def get_all_luot_xe(self) -> List[LuotXe]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_LUOT_XE)
            return [LuotXe.from_row(r) for r in cursor.fetchall()]

    def checkin_xe(self, ma_xe: str) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_LUOT_XE, (ma_xe, 0))
                conn.commit()
            return True, f"Xe {ma_xe} đã vào bãi KTX!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    def checkout_xe(self, ma_luot: int, fee: float = 0.0) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_CHECKOUT_LUOT_XE, (fee, ma_luot))
                conn.commit()
            return True, "Xe đã rời bãi!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    # --- 6. KHÁCH & LẦN THĂM ---
    def get_all_lan_tham(self) -> List[LanTham]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_LAN_THAM)
            return [LanTham.from_row(r) for r in cursor.fetchall()]

    def record_visit(self, so_cmt: str, ten_khach: str, ngay_sinh: str, ma_sv: str) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_KHACH, (
                    so_cmt.strip(), ten_khach.strip(), ngay_sinh.strip() if ngay_sinh else None
                ))
                cursor.execute(queries.SQL_INSERT_LAN_THAM, (
                    so_cmt.strip(), ma_sv.strip()
                ))
                conn.commit()
            return True, "Ghi nhận khách đến thăm thành công!"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    # --- 7. DASHBOARD STATS ---
    def get_dashboard_stats(self) -> Dict[str, Any]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_DASHBOARD_STATS)
            row = cursor.fetchone()
            return dict(row) if row else {}

    # --- 8. PROJECT REPORTS ---
    def get_report_1(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_REPORT_1)
            return [dict(r) for r in cursor.fetchall()]

    def get_report_2(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_REPORT_2)
            return [dict(r) for r in cursor.fetchall()]

    def get_report_3(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_REPORT_3)
            return [dict(r) for r in cursor.fetchall()]

    def get_report_4(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_REPORT_4)
            return [dict(r) for r in cursor.fetchall()]

from dataclasses import dataclass
from typing import Optional

@dataclass
class SinhVien:
    MaSV: str = ""
    SoCMT: str = ""
    NgaySinh: str = ""
    Lop: str = ""
    QueQuan: str = ""
    SoPhong: Optional[str] = None
    LoaiPhong: Optional[str] = None
    DonGiaPhong: Optional[float] = None

    @classmethod
    def from_row(cls, row) -> "SinhVien":
        d = dict(row)
        return cls(
            MaSV=d.get("MaSV", ""),
            SoCMT=d.get("SoCMT", "") or "",
            NgaySinh=d.get("NgaySinh", "") or "",
            Lop=d.get("Lop", "") or "",
            QueQuan=d.get("QueQuan", "") or "",
            SoPhong=d.get("SoPhong"),
            LoaiPhong=d.get("LoaiPhong"),
            DonGiaPhong=float(d.get("DonGiaPhong")) if d.get("DonGiaPhong") is not None else None
        )

@dataclass
class Phong:
    SoPhong: str = ""
    LoaiPhong: str = ""
    DonGia: float = 0.0
    SoNguoiToiDa: int = 4
    SoNguoiHienTai: int = 0
    SoChoTrong: int = 4

    @classmethod
    def from_row(cls, row) -> "Phong":
        d = dict(row)
        return cls(
            SoPhong=d.get("SoPhong", ""),
            LoaiPhong=d.get("LoaiPhong", ""),
            DonGia=float(d.get("DonGia", 0.0)),
            SoNguoiToiDa=int(d.get("SoNguoiToiDa", 4)),
            SoNguoiHienTai=int(d.get("SoNguoiHienTai", 0)),
            SoChoTrong=int(d.get("SoChoTrong", 4))
        )

@dataclass
class DangKyPhong:
    MaDKPHONG: Optional[int] = None
    MaSV: str = ""
    Lop: str = ""
    SoPhong: str = ""
    LoaiPhong: str = ""
    DonGia: float = 0.0
    NgayBatDau: str = ""
    NgayKetThuc: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "DangKyPhong":
        d = dict(row)
        return cls(
            MaDKPHONG=d.get("MaDKPHONG"),
            MaSV=d.get("MaSV", ""),
            Lop=d.get("Lop", ""),
            SoPhong=d.get("SoPhong", ""),
            LoaiPhong=d.get("LoaiPhong", ""),
            DonGia=float(d.get("DonGia", 0.0)),
            NgayBatDau=d.get("NgayBatDau", ""),
            NgayKetThuc=d.get("NgayKetThuc")
        )

@dataclass
class HoaDon:
    MaHD: Optional[int] = None
    MaDKPHONG: int = 0
    MaSV: str = ""
    Lop: str = ""
    SoPhong: str = ""
    Thang: int = 1
    Nam: int = 2026
    TienPhong: float = 0.0
    TienDichVu: float = 0.0
    TongTien: float = 0.0
    TrangThai: str = "Chua thanh toan"

    @classmethod
    def from_row(cls, row) -> "HoaDon":
        d = dict(row)
        return cls(
            MaHD=d.get("MaHD"),
            MaDKPHONG=int(d.get("MaDKPHONG", 0)),
            MaSV=d.get("MaSV", ""),
            Lop=d.get("Lop", ""),
            SoPhong=d.get("SoPhong", ""),
            Thang=int(d.get("Thang", 1)),
            Nam=int(d.get("Nam", 2026)),
            TienPhong=float(d.get("TienPhong", 0.0)),
            TienDichVu=float(d.get("TienDichVu", 0.0)),
            TongTien=float(d.get("TongTien", 0.0)),
            TrangThai=d.get("TrangThai", "Chua thanh toan")
        )

@dataclass
class DichVu:
    MaDV: str = ""
    TenDV: str = ""
    DonGia: float = 0.0

    @classmethod
    def from_row(cls, row) -> "DichVu":
        d = dict(row)
        return cls(
            MaDV=d.get("MaDV", ""),
            TenDV=d.get("TenDV", ""),
            DonGia=float(d.get("DonGia", 0.0))
        )

@dataclass
class SuDungDichVu:
    MaLanSD: Optional[int] = None
    MaSV: str = ""
    Lop: str = ""
    MaDV: str = ""
    TenDV: str = ""
    ThoiDiemSD: str = ""
    SoLuong: int = 1
    DonGiaApDung: float = 0.0
    ThanhTien: float = 0.0

    @classmethod
    def from_row(cls, row) -> "SuDungDichVu":
        d = dict(row)
        return cls(
            MaLanSD=d.get("MaLanSD"),
            MaSV=d.get("MaSV", ""),
            Lop=d.get("Lop", ""),
            MaDV=d.get("MaDV", ""),
            TenDV=d.get("TenDV", ""),
            ThoiDiemSD=d.get("ThoiDiemSD", ""),
            SoLuong=int(d.get("SoLuong", 1)),
            DonGiaApDung=float(d.get("DonGiaApDung", 0.0)),
            ThanhTien=float(d.get("ThanhTien", 0.0))
        )

@dataclass
class Xe:
    MaXE: str = ""
    BienSo: str = ""
    LoaiXe: str = ""
    MaSV: str = ""
    Lop: str = ""
    NgayDangKy: str = ""
    NgayHetHan: Optional[str] = None
    DonGiaThang: float = 100000.0

    @classmethod
    def from_row(cls, row) -> "Xe":
        d = dict(row)
        return cls(
            MaXE=d.get("MaXE", ""),
            BienSo=d.get("BienSo", ""),
            LoaiXe=d.get("LoaiXe", ""),
            MaSV=d.get("MaSV", ""),
            Lop=d.get("Lop", ""),
            NgayDangKy=d.get("NgayDangKy", ""),
            NgayHetHan=d.get("NgayHetHan"),
            DonGiaThang=float(d.get("DonGiaThang", 100000.0))
        )

@dataclass
class LuotXe:
    MaLuotXe: Optional[int] = None
    MaXE: str = ""
    BienSo: str = ""
    LoaiXe: str = ""
    MaSV: str = ""
    Lop: str = ""
    ThoiGianGui: str = ""
    ThoiGianLay: Optional[str] = None
    SoTienPhatSinh: float = 0.0

    @classmethod
    def from_row(cls, row) -> "LuotXe":
        d = dict(row)
        return cls(
            MaLuotXe=d.get("MaLuotXe"),
            MaXE=d.get("MaXE", ""),
            BienSo=d.get("BienSo", ""),
            LoaiXe=d.get("LoaiXe", ""),
            MaSV=d.get("MaSV", ""),
            Lop=d.get("Lop", ""),
            ThoiGianGui=d.get("ThoiGianGui", ""),
            ThoiGianLay=d.get("ThoiGianLay"),
            SoTienPhatSinh=float(d.get("SoTienPhatSinh", 0.0))
        )

@dataclass
class LanTham:
    MaLanTham: Optional[int] = None
    SoCMT: str = ""
    TenKhach: str = ""
    NgaySinh: Optional[str] = None
    MaSV: str = ""
    Lop: str = ""
    SoPhong: Optional[str] = None
    NgayDen: str = ""

    @classmethod
    def from_row(cls, row) -> "LanTham":
        d = dict(row)
        return cls(
            MaLanTham=d.get("MaLanTham"),
            SoCMT=d.get("SoCMT", ""),
            TenKhach=d.get("TenKhach", ""),
            NgaySinh=d.get("NgaySinh"),
            MaSV=d.get("MaSV", ""),
            Lop=d.get("Lop", ""),
            SoPhong=d.get("SoPhong"),
            NgayDen=d.get("NgayDen", "")
        )

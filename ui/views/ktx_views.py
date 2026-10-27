import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from services.ktx_service import KTXService
from models.ktx_models import SinhVien, Phong, DangKyPhong, HoaDon, DichVu, SuDungDichVu, Xe
from ui.theme import Theme

# ==========================================
# 1. DASHBOARD VIEW
# ==========================================
class KTXDashboardView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService, nav_callback: Optional[Callable[[str], None]] = None):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self.nav_callback = nav_callback
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_MAIN, padx=24, pady=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="🏛️ TỔNG QUAN KÝ TÚC XÁ SINH VIÊN (QL_KTX)", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)
        btn_refresh = ttk.Button(header, text="🔄 Làm mới", command=self.refresh)
        btn_refresh.pack(side=tk.RIGHT)

        # Metrics cards
        self.cards_frame = tk.Frame(self, bg=Theme.BG_MAIN, padx=24)
        self.cards_frame.pack(fill=tk.X, pady=(0, 20))
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Content split
        content = tk.Frame(self, bg=Theme.BG_MAIN, padx=24)
        content.pack(fill=tk.BOTH, expand=True)
        content.grid_columnconfigure((0, 1), weight=1)

        # Left card: Room status list
        left = tk.Frame(content, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(left, text="🛏️ TÌNH TRẠNG PHÒNG HIỆN TẠI (PHONG)", font=Theme.FONT_HEADER, fg=Theme.TEXT_MAIN, bg=Theme.SURFACE).pack(anchor="w", pady=(0, 10))

        cols1 = ("phong", "loai", "gia", "hientai", "trong")
        self.tree_rooms = ttk.Treeview(left, columns=cols1, show="headings", height=8)
        self.tree_rooms.heading("phong", text="Số phòng")
        self.tree_rooms.heading("loai", text="Loại phòng")
        self.tree_rooms.heading("gia", text="Đơn giá")
        self.tree_rooms.heading("hientai", text="Đang ở")
        self.tree_rooms.heading("trong", text="Còn trống")
        self.tree_rooms.column("phong", width=80, anchor="center")
        self.tree_rooms.column("loai", width=180, anchor="w")
        self.tree_rooms.column("gia", width=95, anchor="center")
        self.tree_rooms.column("hientai", width=70, anchor="center")
        self.tree_rooms.column("trong", width=70, anchor="center")
        self.tree_rooms.pack(fill=tk.BOTH, expand=True)

        # Right card: Recent invoices
        right = tk.Frame(content, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=16)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        tk.Label(right, text="🧾 HOÁ ĐƠN THU TIỀN (HOADON)", font=Theme.FONT_HEADER, fg=Theme.TEXT_MAIN, bg=Theme.SURFACE).pack(anchor="w", pady=(0, 10))

        cols2 = ("sv", "phong", "thang", "tong", "trangthai")
        self.tree_bills = ttk.Treeview(right, columns=cols2, show="headings", height=8)
        self.tree_bills.heading("sv", text="Mã SV")
        self.tree_bills.heading("phong", text="Phòng")
        self.tree_bills.heading("thang", text="Kỳ thu")
        self.tree_bills.heading("tong", text="Tổng tiền")
        self.tree_bills.heading("trangthai", text="Trạng thái")
        self.tree_bills.column("sv", width=90, anchor="center")
        self.tree_bills.column("phong", width=75, anchor="center")
        self.tree_bills.column("thang", width=75, anchor="center")
        self.tree_bills.column("tong", width=100, anchor="center")
        self.tree_bills.column("trangthai", width=120, anchor="center")
        self.tree_bills.pack(fill=tk.BOTH, expand=True)

    def _create_card(self, parent, col, title, value, subtitle, color):
        card = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid", padx=14, pady=12)
        card.grid(row=0, column=col, sticky="nsew", padx=6)
        tk.Frame(card, bg=color, height=3).pack(fill=tk.X, side=tk.TOP, pady=(0, 6))
        tk.Label(card, text=title, font=Theme.FONT_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.SURFACE).pack(anchor="w")
        tk.Label(card, text=str(value), font=Theme.FONT_STAT_NUM, fg=color, bg=Theme.SURFACE).pack(anchor="w", pady=2)
        tk.Label(card, text=subtitle, font=Theme.FONT_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.SURFACE).pack(anchor="w")

    def refresh(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        stats = self.ktx_service.get_dashboard_stats()
        tot_sv = stats.get("total_sinhvien", 0)
        tot_dk = stats.get("total_dangky", 0)
        cap = stats.get("total_capacity", 0) or 1
        pct_occupancy = int((tot_dk / cap) * 100)
        rev_paid = stats.get("revenue_paid", 0) or 0
        rev_unpaid = stats.get("revenue_unpaid", 0) or 0

        self._create_card(self.cards_frame, 0, "SINH VIÊN NỘI TRÚ", f"{tot_dk} SV", f"Trên tổng {tot_sv} sinh viên", Theme.PRIMARY)
        self._create_card(self.cards_frame, 1, "TỶ LỆ LẤP ĐẦY PHÒNG", f"{pct_occupancy}%", f"{tot_dk}/{cap} chỗ ở", Theme.SUCCESS)
        self._create_card(self.cards_frame, 2, "XE ĐĂNG KÝ VÉ THÁNG", f"{stats.get('total_xe', 0)} Xe", "Xe máy, xe đạp điện", Theme.INFO)
        self._create_card(self.cards_frame, 3, "DOANH THU ĐÃ THU", f"{rev_paid:,.0f} đ", f"Chưa thu: {rev_unpaid:,.0f} đ", Theme.WARNING)

        # Refresh rooms
        for r in self.tree_rooms.get_children():
            self.tree_rooms.delete(r)
        for p in self.ktx_service.get_all_phong():
            self.tree_rooms.insert("", "end", values=(
                p.SoPhong, p.LoaiPhong, f"{p.DonGia:,.0f} đ", f"{p.SoNguoiHienTai}/{p.SoNguoiToiDa}", f"{p.SoChoTrong} chỗ"
            ))

        # Refresh bills
        for r in self.tree_bills.get_children():
            self.tree_bills.delete(r)
        for h in self.ktx_service.get_all_hoadon()[:10]:
            self.tree_bills.insert("", "end", values=(
                h.MaSV, h.SoPhong, f"{h.Thang}/{h.Nam}", f"{h.TongTien:,.0f} đ", h.TrangThai
            ))


# ==========================================
# 2. SINH VIÊN VIEW
# ==========================================
class KTXSinhVienView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        action_bar = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        action_bar.pack(fill=tk.X)
        tk.Label(action_bar, text="QUẢN LÝ HỒ SƠ SINH VIÊN (SINHVIEN)", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        btn_box = tk.Frame(action_bar, bg=Theme.BG_MAIN)
        btn_box.pack(side=tk.RIGHT)
        ttk.Button(btn_box, text="➕ Thêm sinh viên", style="Primary.TButton", command=self._add_sv).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_box, text="✏️ Sửa", command=self._edit_sv).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_box, text="🗑️ Xoá", style="Danger.TButton", command=self._delete_sv).pack(side=tk.LEFT, padx=4)

        # Search bar
        search_card = tk.Frame(self, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=12)
        search_card.pack(fill=tk.X, padx=20, pady=(0, 12))

        tk.Label(search_card, text="🔍 Tìm kiếm (Mã SV, Số CMT, Lớp, Quê quán):", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.entry_search = ttk.Entry(search_card)
        self.entry_search.pack(fill=tk.X, pady=(4, 0))
        self.entry_search.bind("<KeyRelease>", lambda e: self.reload_data())

        # Table
        table_frame = tk.Frame(self, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        cols = ("masv", "socmt", "ngaysinh", "lop", "quequan", "sophong", "loaiphong", "dongia")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("masv", text="Mã SV")
        self.tree.heading("socmt", text="Số CMT / CCCD")
        self.tree.heading("ngaysinh", text="Ngày sinh")
        self.tree.heading("lop", text="Lớp")
        self.tree.heading("quequan", text="Quê quán")
        self.tree.heading("sophong", text="Phòng KTX đang ở")
        self.tree.heading("loaiphong", text="Loại phòng")
        self.tree.heading("dongia", text="Đơn giá phòng")

        self.tree.column("masv", width=100, anchor="center")
        self.tree.column("socmt", width=140, anchor="center")
        self.tree.column("ngaysinh", width=110, anchor="center")
        self.tree.column("lop", width=100, anchor="center")
        self.tree.column("quequan", width=160, anchor="w")
        self.tree.column("sophong", width=130, anchor="center")
        self.tree.column("loaiphong", width=180, anchor="w")
        self.tree.column("dongia", width=120, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def reload_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

        kw = self.entry_search.get().strip()
        students = self.ktx_service.search_sinhvien(kw)
        for s in students:
            gia_str = f"{s.DonGiaPhong:,.0f} đ" if s.DonGiaPhong else "--"
            self.tree.insert("", "end", values=(
                s.MaSV, s.SoCMT, s.NgaySinh or "--", s.Lop or "--",
                s.QueQuan or "--", s.SoPhong or "Chưa xếp phòng", s.LoaiPhong or "--", gia_str
            ))

    def _add_sv(self):
        d = SinhVienModal(self)
        self.wait_window(d)
        if d.result:
            ok, msg = self.ktx_service.create_sinhvien(d.result)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _edit_sv(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 sinh viên.", parent=self)
            return
        vals = self.tree.item(sel[0], "values")
        sv = SinhVien(MaSV=vals[0], SoCMT=vals[1], NgaySinh=vals[2], Lop=vals[3], QueQuan=vals[4])
        d = SinhVienModal(self, sv=sv)
        self.wait_window(d)
        if d.result:
            ok, msg = self.ktx_service.update_sinhvien(d.result)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_sv(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 sinh viên cần xoá.", parent=self)
            return
        vals = self.tree.item(sel[0], "values")
        ans = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá sinh viên [{vals[0]}]?", parent=self)
        if ans:
            ok, msg = self.ktx_service.delete_sinhvien(vals[0])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)


class SinhVienModal(tk.Toplevel):
    def __init__(self, parent, sv: Optional[SinhVien] = None):
        super().__init__(parent)
        self.sv = sv
        self.result: Optional[SinhVien] = None
        self.title("Sửa sinh viên" if sv else "Thêm sinh viên mới")
        self.geometry("450x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Mã sinh viên * (Ví dụ: SV034)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_masv = ttk.Entry(body)
        self.entry_masv.pack(fill=tk.X, pady=(0, 8))
        if sv:
            self.entry_masv.insert(0, sv.MaSV)
            self.entry_masv.config(state="disabled")

        tk.Label(body, text="Số CMT / CCCD *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_cmt = ttk.Entry(body)
        self.entry_cmt.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Ngày sinh (YYYY-MM-DD)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_ns = ttk.Entry(body)
        self.entry_ns.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Lớp (Ví dụ: CNTT1)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_lop = ttk.Entry(body)
        self.entry_lop.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Quê quán (Ví dụ: Ha Noi)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_que = ttk.Entry(body)
        self.entry_que.pack(fill=tk.X, pady=(0, 16))

        if sv:
            self.entry_cmt.insert(0, sv.SoCMT)
            self.entry_ns.insert(0, sv.NgaySinh if sv.NgaySinh != "--" else "")
            self.entry_lop.insert(0, sv.Lop if sv.Lop != "--" else "")
            self.entry_que.insert(0, sv.QueQuan if sv.QueQuan != "--" else "")

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Lưu", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        masv = self.entry_masv.get().strip().upper() if not self.sv else self.sv.MaSV
        cmt = self.entry_cmt.get().strip()
        ns = self.entry_ns.get().strip()
        lop = self.entry_lop.get().strip()
        que = self.entry_que.get().strip()

        if not masv or not cmt:
            messagebox.showwarning("Lỗi", "Vui lòng nhập Mã SV và Số CMT.", parent=self)
            return

        self.result = SinhVien(MaSV=masv, SoCMT=cmt, NgaySinh=ns, Lop=lop, QueQuan=que)
        self.destroy()


# ==========================================
# 3. PHÒNG & ĐĂNG KÝ PHÒNG VIEW
# ==========================================
class KTXPhongView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        header.pack(fill=tk.X)
        tk.Label(header, text="QUẢN LÝ PHÒNG & XẾP PHÒNG KTX", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        tab_dk = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_dk, text="📋 Danh sách Đăng ký phòng (DANGKY_PHONG)")
        self._build_tab_dk(tab_dk)

        tab_p = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_p, text="🛏️ Danh mục Phòng KTX (PHONG)")
        self._build_tab_phong(tab_p)

    def _build_tab_dk(self, parent):
        ctrl = tk.Frame(parent, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="➕ Xếp phòng cho sinh viên", style="Primary.TButton", command=self._add_dk).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="🗑️ Huỷ đăng ký phòng", style="Danger.TButton", command=self._delete_dk).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("madk", "masv", "lop", "sophong", "loai", "gia", "ngaybd", "ngaykt")
        self.tree_dk = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_dk.heading("madk", text="Mã ĐK")
        self.tree_dk.heading("masv", text="Mã SV")
        self.tree_dk.heading("lop", text="Lớp")
        self.tree_dk.heading("sophong", text="Số phòng")
        self.tree_dk.heading("loai", text="Loại phòng")
        self.tree_dk.heading("gia", text="Đơn giá")
        self.tree_dk.heading("ngaybd", text="Ngày bắt đầu")
        self.tree_dk.heading("ngaykt", text="Ngày kết thúc")

        self.tree_dk.column("madk", width=70, anchor="center")
        self.tree_dk.column("masv", width=100, anchor="center")
        self.tree_dk.column("lop", width=100, anchor="center")
        self.tree_dk.column("sophong", width=90, anchor="center")
        self.tree_dk.column("loai", width=180, anchor="w")
        self.tree_dk.column("gia", width=110, anchor="center")
        self.tree_dk.column("ngaybd", width=110, anchor="center")
        self.tree_dk.column("ngaykt", width=110, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_dk.yview)
        self.tree_dk.configure(yscrollcommand=vsb.set)
        self.tree_dk.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_phong(self, parent):
        ctrl = tk.Frame(parent, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="➕ Thêm phòng mới", style="Primary.TButton", command=self._add_phong).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="🗑️ Xoá phòng", style="Danger.TButton", command=self._delete_phong).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("sophong", "loai", "dongia", "toida", "hientai", "chotrong")
        self.tree_p = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_p.heading("sophong", text="Số phòng")
        self.tree_p.heading("loai", text="Loại phòng")
        self.tree_p.heading("dongia", text="Đơn giá (VNĐ)")
        self.tree_p.heading("toida", text="Số người tối đa")
        self.tree_p.heading("hientai", text="Số người đang ở")
        self.tree_p.heading("chotrong", text="Số chỗ còn trống")

        self.tree_p.column("sophong", width=100, anchor="center")
        self.tree_p.column("loai", width=260, anchor="w")
        self.tree_p.column("dongia", width=130, anchor="center")
        self.tree_p.column("toida", width=120, anchor="center")
        self.tree_p.column("hientai", width=120, anchor="center")
        self.tree_p.column("chotrong", width=120, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_p.yview)
        self.tree_p.configure(yscrollcommand=vsb.set)
        self.tree_p.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def reload_data(self):
        for r in self.tree_dk.get_children():
            self.tree_dk.delete(r)
        for dk in self.ktx_service.get_all_dangky_phong():
            self.tree_dk.insert("", "end", values=(
                dk.MaDKPHONG, dk.MaSV, dk.Lop, dk.SoPhong,
                dk.LoaiPhong, f"{dk.DonGia:,.0f} đ", dk.NgayBatDau, dk.NgayKetThuc or "--"
            ))

        for r in self.tree_p.get_children():
            self.tree_p.delete(r)
        for p in self.ktx_service.get_all_phong():
            self.tree_p.insert("", "end", values=(
                p.SoPhong, p.LoaiPhong, f"{p.DonGia:,.0f} đ", p.SoNguoiToiDa, p.SoNguoiHienTai, p.SoChoTrong
            ))

    def _add_dk(self):
        students = self.ktx_service.get_all_sinhvien()
        rooms = self.ktx_service.get_all_phong()
        available_rooms = [p for p in rooms if p.SoChoTrong > 0]
        if not available_rooms:
            messagebox.showwarning("Hết phòng", "Tất cả các phòng KTX đã đầy chỗ!", parent=self)
            return

        d = DangKyModal(self, students=students, rooms=available_rooms)
        self.wait_window(d)
        if d.result:
            r = d.result
            ok, msg = self.ktx_service.create_dangky_phong(r["masv"], r["sophong"], r["ngaybd"], r["ngaykt"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_dk(self):
        sel = self.tree_dk.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn bản ghi đăng ký phòng cần huỷ.", parent=self)
            return
        madk = int(self.tree_dk.item(sel[0], "values")[0])
        masv = self.tree_dk.item(sel[0], "values")[1]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn huỷ xếp phòng của sinh viên {masv}?", parent=self):
            ok, msg = self.ktx_service.delete_dangky_phong(madk)
            if ok:
                self.reload_data()

    def _add_phong(self):
        d = PhongModal(self)
        self.wait_window(d)
        if d.result:
            r = d.result
            ok, msg = self.ktx_service.create_phong(r["sophong"], r["loai"], r["gia"], r["songuoi"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_phong(self):
        sel = self.tree_p.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn phòng cần xoá.", parent=self)
            return
        sp = self.tree_p.item(sel[0], "values")[0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá phòng {sp}?", parent=self):
            ok, msg = self.ktx_service.delete_phong(sp)
            if ok:
                self.reload_data()


class DangKyModal(tk.Toplevel):
    def __init__(self, parent, students, rooms):
        super().__init__(parent)
        self.students = students
        self.rooms = rooms
        self.result = None
        self.title("Xếp phòng cho sinh viên")
        self.geometry("450x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Chọn sinh viên *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.sv_opts = [f"{s.MaSV} (Lớp: {s.Lop})" for s in self.students]
        self.sv_var = tk.StringVar(value=self.sv_opts[0] if self.sv_opts else "")
        self.cb_sv = ttk.Combobox(body, textvariable=self.sv_var, values=self.sv_opts, state="readonly")
        self.cb_sv.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Chọn phòng còn chỗ *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.room_opts = [f"{p.SoPhong} - {p.LoaiPhong} (Còn {p.SoChoTrong} chỗ - {p.DonGia:,.0f} đ)" for p in self.rooms]
        self.room_var = tk.StringVar(value=self.room_opts[0] if self.room_opts else "")
        self.cb_room = ttk.Combobox(body, textvariable=self.room_var, values=self.room_opts, state="readonly")
        self.cb_room.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Ngày bắt đầu (YYYY-MM-DD) *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_bd = ttk.Entry(body)
        self.entry_bd.insert(0, "2026-09-01")
        self.entry_bd.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Ngày kết thúc (YYYY-MM-DD)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_kt = ttk.Entry(body)
        self.entry_kt.insert(0, "2027-06-30")
        self.entry_kt.pack(fill=tk.X, pady=(0, 16))

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Xếp phòng", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        sv_str = self.sv_var.get()
        room_str = self.room_var.get()
        bd = self.entry_bd.get().strip()
        kt = self.entry_kt.get().strip()
        masv = sv_str.split(" ")[0]
        sophong = room_str.split(" - ")[0]
        self.result = {"masv": masv, "sophong": sophong, "ngaybd": bd, "ngaykt": kt}
        self.destroy()


class PhongModal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        self.title("Thêm phòng KTX mới")
        self.geometry("400x340")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Số phòng * (Ví dụ: P502)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_sp = ttk.Entry(body)
        self.entry_sp.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Loại phòng *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_loai = ttk.Entry(body)
        self.entry_loai.insert(0, "Phong 4 nguoi")
        self.entry_loai.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Đơn giá phòng / tháng (VNĐ) *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_gia = ttk.Entry(body)
        self.entry_gia.insert(0, "900000")
        self.entry_gia.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Số người tối đa *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_toida = ttk.Spinbox(body, from_=1, to=12)
        self.entry_toida.set(4)
        self.entry_toida.pack(fill=tk.X, pady=(0, 16))

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Lưu phòng", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        sp = self.entry_sp.get().strip().upper()
        loai = self.entry_loai.get().strip()
        try:
            gia = float(self.entry_gia.get().strip())
            toida = int(self.entry_toida.get().strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Đơn giá và số người phải là số.", parent=self)
            return
        if not sp or not loai:
            messagebox.showwarning("Lỗi", "Số phòng và loại phòng không được để trống.", parent=self)
            return
        self.result = {"sophong": sp, "loai": loai, "gia": gia, "songuoi": toida}
        self.destroy()


# ==========================================
# 4. HOÁ ĐƠN & DỊCH VỤ VIEW
# ==========================================
class KTXHoaDonDichVuView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        header.pack(fill=tk.X)
        tk.Label(header, text="QUẢN LÝ HOÁ ĐƠN & DỊCH VỤ (HOADON, DICHVU, SUDUNG_DICHVU)", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        tab_hd = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_hd, text="🧾 Danh sách Hoá Đơn (HOADON)")
        self._build_tab_hd(tab_hd)

        tab_sd = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_sd, text="🧺 Sử Dụng Dịch Vụ (SUDUNG_DICHVU)")
        self._build_tab_sd(tab_sd)

        tab_dv = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_dv, text="🏷️ Bảng Giá Dịch Vụ (DICHVU)")
        self._build_tab_dv(tab_dv)

    def _build_tab_hd(self, parent):
        ctrl = tk.Frame(parent, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="➕ Lập hoá đơn mới", style="Primary.TButton", command=self._add_hd).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="✓ Đánh dấu ĐÃ THANH TOÁN", style="Success.TButton", command=self._mark_paid).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="🗑️ Xoá hoá đơn", style="Danger.TButton", command=self._delete_hd).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("mahd", "madk", "masv", "lop", "sophong", "thang", "tienphong", "tiendv", "tongtien", "trangthai")
        self.tree_hd = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_hd.heading("mahd", text="Mã HĐ")
        self.tree_hd.heading("madk", text="Mã ĐK")
        self.tree_hd.heading("masv", text="Mã SV")
        self.tree_hd.heading("lop", text="Lớp")
        self.tree_hd.heading("sophong", text="Phòng")
        self.tree_hd.heading("thang", text="Kỳ thu")
        self.tree_hd.heading("tienphong", text="Tiền phòng")
        self.tree_hd.heading("tiendv", text="Tiền DV khác")
        self.tree_hd.heading("tongtien", text="Tổng tiền")
        self.tree_hd.heading("trangthai", text="Trạng thái")

        self.tree_hd.column("mahd", width=65, anchor="center")
        self.tree_hd.column("madk", width=65, anchor="center")
        self.tree_hd.column("masv", width=95, anchor="center")
        self.tree_hd.column("lop", width=90, anchor="center")
        self.tree_hd.column("sophong", width=85, anchor="center")
        self.tree_hd.column("thang", width=85, anchor="center")
        self.tree_hd.column("tienphong", width=110, anchor="center")
        self.tree_hd.column("tiendv", width=110, anchor="center")
        self.tree_hd.column("tongtien", width=120, anchor="center")
        self.tree_hd.column("trangthai", width=135, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_hd.yview)
        self.tree_hd.configure(yscrollcommand=vsb.set)
        self.tree_hd.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_sd(self, parent):
        ctrl = tk.Frame(parent, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="➕ Ghi nhận dùng dịch vụ", style="Primary.TButton", command=self._add_sd).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="🗑️ Xoá bản ghi", style="Danger.TButton", command=self._delete_sd).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("masd", "masv", "lop", "madv", "tendv", "thoigian", "soluong", "dongia", "thanhtien")
        self.tree_sd = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_sd.heading("masd", text="Mã Lần SD")
        self.tree_sd.heading("masv", text="Mã SV")
        self.tree_sd.heading("lop", text="Lớp")
        self.tree_sd.heading("madv", text="Mã DV")
        self.tree_sd.heading("tendv", text="Tên dịch vụ")
        self.tree_sd.heading("thoigian", text="Thời điểm SD")
        self.tree_sd.heading("soluong", text="Số lượng")
        self.tree_sd.heading("dongia", text="Đơn giá")
        self.tree_sd.heading("thanhtien", text="Thành tiền")

        self.tree_sd.column("masd", width=70, anchor="center")
        self.tree_sd.column("masv", width=95, anchor="center")
        self.tree_sd.column("lop", width=90, anchor="center")
        self.tree_sd.column("madv", width=85, anchor="center")
        self.tree_sd.column("tendv", width=190, anchor="w")
        self.tree_sd.column("thoigian", width=140, anchor="center")
        self.tree_sd.column("soluong", width=70, anchor="center")
        self.tree_sd.column("dongia", width=95, anchor="center")
        self.tree_sd.column("thanhtien", width=110, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_sd.yview)
        self.tree_sd.configure(yscrollcommand=vsb.set)
        self.tree_sd.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_dv(self, parent):
        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid", pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        cols = ("madv", "tendv", "dongia")
        self.tree_dv = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree_dv.heading("madv", text="Mã Dịch Vụ")
        self.tree_dv.heading("tendv", text="Tên Dịch Vụ")
        self.tree_dv.heading("dongia", text="Đơn Giá Quy Định")

        self.tree_dv.column("madv", width=120, anchor="center")
        self.tree_dv.column("tendv", width=320, anchor="w")
        self.tree_dv.column("dongia", width=150, anchor="center")
        self.tree_dv.pack(fill=tk.BOTH, expand=True)

    def reload_data(self):
        for r in self.tree_hd.get_children():
            self.tree_hd.delete(r)
        for h in self.ktx_service.get_all_hoadon():
            self.tree_hd.insert("", "end", values=(
                h.MaHD, h.MaDKPHONG, h.MaSV, h.Lop, h.SoPhong,
                f"{h.Thang}/{h.Nam}", f"{h.TienPhong:,.0f} đ", f"{h.TienDichVu:,.0f} đ",
                f"{h.TongTien:,.0f} đ", h.TrangThai
            ))

        for r in self.tree_sd.get_children():
            self.tree_sd.delete(r)
        for sd in self.ktx_service.get_all_sudung_dichvu():
            self.tree_sd.insert("", "end", values=(
                sd.MaLanSD, sd.MaSV, sd.Lop, sd.MaDV, sd.TenDV,
                sd.ThoiDiemSD, sd.SoLuong, f"{sd.DonGiaApDung:,.0f} đ", f"{sd.ThanhTien:,.0f} đ"
            ))

        for r in self.tree_dv.get_children():
            self.tree_dv.delete(r)
        for dv in self.ktx_service.get_all_dichvu():
            self.tree_dv.insert("", "end", values=(dv.MaDV, dv.TenDV, f"{dv.DonGia:,.0f} đ"))

    def _mark_paid(self):
        sel = self.tree_hd.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 hoá đơn để thanh toán.", parent=self)
            return
        mahd = int(self.tree_hd.item(sel[0], "values")[0])
        ok, msg = self.ktx_service.update_trangthai_hoadon(mahd, "Da thanh toan")
        if ok:
            messagebox.showinfo("Thành công", "Đã cập nhật trạng thái 'Da thanh toan'!", parent=self)
            self.reload_data()

    def _delete_hd(self):
        sel = self.tree_hd.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 hoá đơn cần xoá.", parent=self)
            return
        mahd = int(self.tree_hd.item(sel[0], "values")[0])
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá hoá đơn #{mahd}?", parent=self):
            ok, msg = self.ktx_service.delete_hoadon(mahd)
            if ok:
                self.reload_data()

    def _add_hd(self):
        dks = self.ktx_service.get_all_dangky_phong()
        if not dks:
            messagebox.showwarning("Trống", "Chưa có sinh viên nào đăng ký phòng.", parent=self)
            return
        d = HoaDonModal(self, dks=dks)
        self.wait_window(d)
        if d.result:
            r = d.result
            ok, msg = self.ktx_service.create_hoadon(r["madk"], r["thang"], r["nam"], r["tienphong"], r["tiendv"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _add_sd(self):
        students = self.ktx_service.get_all_sinhvien()
        dvs = self.ktx_service.get_all_dichvu()
        d = SuDungDVModal(self, students=students, dvs=dvs)
        self.wait_window(d)
        if d.result:
            r = d.result
            ok, msg = self.ktx_service.create_sudung_dichvu(r["masv"], r["madv"], r["soluong"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()

    def _delete_sd(self):
        sel = self.tree_sd.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 bản ghi sử dụng dịch vụ cần xoá.", parent=self)
            return
        masd = int(self.tree_sd.item(sel[0], "values")[0])
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xoá bản ghi này?", parent=self):
            ok, msg = self.ktx_service.delete_sudung_dichvu(masd)
            if ok:
                self.reload_data()


class HoaDonModal(tk.Toplevel):
    def __init__(self, parent, dks):
        super().__init__(parent)
        self.dks = dks
        self.result = None
        self.title("Lập hoá đơn mới")
        self.geometry("450x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Chọn sinh viên nội trú *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.dk_opts = [f"{dk.MaDKPHONG} - {dk.MaSV} (Phòng {dk.SoPhong} - {dk.DonGia:,.0f} đ)" for dk in self.dks]
        self.dk_var = tk.StringVar(value=self.dk_opts[0])
        self.cb_dk = ttk.Combobox(body, textvariable=self.dk_var, values=self.dk_opts, state="readonly")
        self.cb_dk.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Tháng (1 - 12) *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_thang = ttk.Spinbox(body, from_=1, to=12)
        self.entry_thang.set(10)
        self.entry_thang.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Năm *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_nam = ttk.Entry(body)
        self.entry_nam.insert(0, "2026")
        self.entry_nam.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Tiền dịch vụ phát sinh (VNĐ)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_tiendv = ttk.Entry(body)
        self.entry_tiendv.insert(0, "0")
        self.entry_tiendv.pack(fill=tk.X, pady=(0, 16))

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Tạo hoá đơn", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        dk_str = self.dk_var.get()
        madk = int(dk_str.split(" - ")[0])
        selected_dk = next((dk for dk in self.dks if dk.MaDKPHONG == madk), None)
        tien_phong = selected_dk.DonGia if selected_dk else 0.0

        try:
            thang = int(self.entry_thang.get().strip())
            nam = int(self.entry_nam.get().strip())
            tiendv = float(self.entry_tiendv.get().strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Tháng, năm và tiền dịch vụ phải là số.", parent=self)
            return

        self.result = {"madk": madk, "thang": thang, "nam": nam, "tienphong": tien_phong, "tiendv": tiendv}
        self.destroy()


class SuDungDVModal(tk.Toplevel):
    def __init__(self, parent, students, dvs):
        super().__init__(parent)
        self.students = students
        self.dvs = dvs
        self.result = None
        self.title("Ghi nhận sử dụng dịch vụ")
        self.geometry("450x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Chọn sinh viên *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.sv_opts = [f"{s.MaSV} (Lớp: {s.Lop})" for s in self.students]
        self.sv_var = tk.StringVar(value=self.sv_opts[0] if self.sv_opts else "")
        self.cb_sv = ttk.Combobox(body, textvariable=self.sv_var, values=self.sv_opts, state="readonly")
        self.cb_sv.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Chọn dịch vụ *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.dv_opts = [f"{dv.MaDV} - {dv.TenDV} ({dv.DonGia:,.0f} đ)" for dv in self.dvs]
        self.dv_var = tk.StringVar(value=self.dv_opts[0] if self.dv_opts else "")
        self.cb_dv = ttk.Combobox(body, textvariable=self.dv_var, values=self.dv_opts, state="readonly")
        self.cb_dv.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Số lượng *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_sl = ttk.Spinbox(body, from_=1, to=100)
        self.entry_sl.set(1)
        self.entry_sl.pack(fill=tk.X, pady=(0, 16))

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Xác nhận", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        sv_str = self.sv_var.get()
        dv_str = self.dv_var.get()
        masv = sv_str.split(" ")[0]
        madv = dv_str.split(" - ")[0]
        try:
            sl = int(self.entry_sl.get().strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số nguyên dương.", parent=self)
            return
        self.result = {"masv": masv, "madv": madv, "soluong": sl}
        self.destroy()


# ==========================================
# 5. XE & LƯỢT XE VIEW
# ==========================================
class KTXParkingView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        header.pack(fill=tk.X)
        tk.Label(header, text="QUẢN LÝ GỬI XE & LƯỢT RA VÀO (XE, LUOT_XE)", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        tab_xe = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_xe, text="🛵 Danh sách Xe vé tháng (XE)")
        self._build_tab_xe(tab_xe)

        tab_lx = tk.Frame(notebook, bg=Theme.BG_MAIN)
        notebook.add(tab_lx, text="⏱️ Lịch sử Lượt xe ra vào (LUOT_XE)")
        self._build_tab_lx(tab_lx)

    def _build_tab_xe(self, parent):
        ctrl = tk.Frame(parent, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="➕ Đăng ký xe mới", style="Primary.TButton", command=self._add_xe).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="🗑️ Huỷ đăng ký xe", style="Danger.TButton", command=self._delete_xe).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="📥 Xe Vào Bãi (Check-in)", command=self._checkin_selected).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("maxe", "bienso", "loaixe", "masv", "lop", "ngaydk", "ngayhh", "dongia")
        self.tree_xe = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_xe.heading("maxe", text="Mã Xe")
        self.tree_xe.heading("bienso", text="Biển số")
        self.tree_xe.heading("loaixe", text="Loại xe")
        self.tree_xe.heading("masv", text="Mã SV chủ xe")
        self.tree_xe.heading("lop", text="Lớp")
        self.tree_xe.heading("ngaydk", text="Ngày đăng ký")
        self.tree_xe.heading("ngayhh", text="Ngày hết hạn")
        self.tree_xe.heading("dongia", text="Phí tháng")

        self.tree_xe.column("maxe", width=85, anchor="center")
        self.tree_xe.column("bienso", width=120, anchor="center")
        self.tree_xe.column("loaixe", width=170, anchor="w")
        self.tree_xe.column("masv", width=110, anchor="center")
        self.tree_xe.column("lop", width=95, anchor="center")
        self.tree_xe.column("ngaydk", width=105, anchor="center")
        self.tree_xe.column("ngayhh", width=105, anchor="center")
        self.tree_xe.column("dongia", width=105, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_xe.yview)
        self.tree_xe.configure(yscrollcommand=vsb.set)
        self.tree_xe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab_lx(self, parent):
        ctrl = tk.Frame(parent, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="📤 Xe Ra Bãi (Check-out)", style="Primary.TButton", command=self._checkout_selected).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("maluot", "maxe", "bienso", "loaixe", "masv", "thoigiangui", "thoigianlay", "sotien")
        self.tree_lx = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_lx.heading("maluot", text="Mã Lượt")
        self.tree_lx.heading("maxe", text="Mã Xe")
        self.tree_lx.heading("bienso", text="Biển số")
        self.tree_lx.heading("loaixe", text="Loại xe")
        self.tree_lx.heading("masv", text="Mã SV chủ xe")
        self.tree_lx.heading("thoigiangui", text="Thời gian gửi (Vào)")
        self.tree_lx.heading("thoigianlay", text="Thời gian lấy (Ra)")
        self.tree_lx.heading("sotien", text="Phí phát sinh")

        self.tree_lx.column("maluot", width=70, anchor="center")
        self.tree_lx.column("maxe", width=85, anchor="center")
        self.tree_lx.column("bienso", width=120, anchor="center")
        self.tree_lx.column("loaixe", width=160, anchor="w")
        self.tree_lx.column("masv", width=100, anchor="center")
        self.tree_lx.column("thoigiangui", width=150, anchor="center")
        self.tree_lx.column("thoigianlay", width=150, anchor="center")
        self.tree_lx.column("sotien", width=105, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_lx.yview)
        self.tree_lx.configure(yscrollcommand=vsb.set)
        self.tree_lx.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def reload_data(self):
        for r in self.tree_xe.get_children():
            self.tree_xe.delete(r)
        for x in self.ktx_service.get_all_xe():
            self.tree_xe.insert("", "end", values=(
                x.MaXE, x.BienSo, x.LoaiXe, x.MaSV, x.Lop, x.NgayDangKy, x.NgayHetHan or "--", f"{x.DonGiaThang:,.0f} đ"
            ))

        for r in self.tree_lx.get_children():
            self.tree_lx.delete(r)
        for lx in self.ktx_service.get_all_luot_xe():
            self.tree_lx.insert("", "end", values=(
                lx.MaLuotXe, lx.MaXE, lx.BienSo, lx.LoaiXe, lx.MaSV,
                lx.ThoiGianGui, lx.ThoiGianLay or "Đang gửi trong bãi", f"{lx.SoTienPhatSinh:,.0f} đ"
            ))

    def _add_xe(self):
        students = self.ktx_service.get_all_sinhvien()
        d = XeModal(self, students=students)
        self.wait_window(d)
        if d.result:
            r = d.result
            ok, msg = self.ktx_service.create_xe(r["maxe"], r["bienso"], r["loaixe"], r["masv"], r["ngaydk"], r["ngayhh"], r["dongia"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_xe(self):
        sel = self.tree_xe.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 xe cần huỷ.", parent=self)
            return
        mx = self.tree_xe.item(sel[0], "values")[0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn huỷ xe {mx}?", parent=self):
            ok, msg = self.ktx_service.delete_xe(mx)
            if ok:
                self.reload_data()

    def _checkin_selected(self):
        sel = self.tree_xe.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn xe để Check-in vào bãi.", parent=self)
            return
        mx = self.tree_xe.item(sel[0], "values")[0]
        ok, msg = self.ktx_service.checkin_xe(mx)
        if ok:
            messagebox.showinfo("Check-in thành công", msg, parent=self)
            self.reload_data()

    def _checkout_selected(self):
        sel = self.tree_lx.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 lượt xe để Check-out.", parent=self)
            return
        vals = self.tree_lx.item(sel[0], "values")
        if vals[6] != "Đang gửi trong bãi":
            messagebox.showinfo("Thông báo", "Lượt xe này đã lấy xe ra trước đó rồi.", parent=self)
            return
        maluot = int(vals[0])
        ok, msg = self.ktx_service.checkout_xe(maluot, fee=0.0)
        if ok:
            messagebox.showinfo("Check-out thành công", msg, parent=self)
            self.reload_data()


class XeModal(tk.Toplevel):
    def __init__(self, parent, students):
        super().__init__(parent)
        self.students = students
        self.result = None
        self.title("Đăng ký gửi xe cho sinh viên")
        self.geometry("450x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Mã xe * (Ví dụ: XE013)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_mx = ttk.Entry(body)
        self.entry_mx.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Biển số xe * (Ví dụ: 29A-99999)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_bs = ttk.Entry(body)
        self.entry_bs.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Loại xe * (Ví dụ: Xe may)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_lx = ttk.Entry(body)
        self.entry_lx.insert(0, "Xe may")
        self.entry_lx.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Sinh viên chủ xe *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.sv_opts = [f"{s.MaSV} (Lớp: {s.Lop})" for s in self.students]
        self.sv_var = tk.StringVar(value=self.sv_opts[0] if self.sv_opts else "")
        self.cb_sv = ttk.Combobox(body, textvariable=self.sv_var, values=self.sv_opts, state="readonly")
        self.cb_sv.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Đơn giá tháng (VNĐ)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_gia = ttk.Entry(body)
        self.entry_gia.insert(0, "100000")
        self.entry_gia.pack(fill=tk.X, pady=(0, 16))

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Đăng ký", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        mx = self.entry_mx.get().strip().upper()
        bs = self.entry_bs.get().strip().upper()
        lx = self.entry_lx.get().strip()
        sv_str = self.sv_var.get()
        masv = sv_str.split(" ")[0]
        try:
            gia = float(self.entry_gia.get().strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Đơn giá phải là số.", parent=self)
            return

        self.result = {"maxe": mx, "bienso": bs, "loaixe": lx, "masv": masv, "ngaydk": "2026-09-01", "ngayhh": "2026-12-31", "dongia": gia}
        self.destroy()


# ==========================================
# 6. KHÁCH ĐẾN THĂM VIEW
# ==========================================
class KTXVisitorsView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        header.pack(fill=tk.X)
        tk.Label(header, text="QUẢN LÝ KHÁCH ĐẾN THĂM (KHACH, LAN_THAM)", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        btn_box = tk.Frame(header, bg=Theme.BG_MAIN)
        btn_box.pack(side=tk.RIGHT)
        ttk.Button(btn_box, text="➕ Ghi nhận khách đến thăm", style="Primary.TButton", command=self._add_visit).pack(side=tk.LEFT, padx=4)

        table_frame = tk.Frame(self, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        cols = ("malan", "socmt", "tenkhach", "ngaysinh", "masv", "lop", "sophong", "ngayden")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("malan", text="Mã Lần")
        self.tree.heading("socmt", text="Số CMT Khách")
        self.tree.heading("tenkhach", text="Tên khách đến thăm")
        self.tree.heading("ngaysinh", text="Ngày sinh")
        self.tree.heading("masv", text="Mã SV thăm")
        self.tree.heading("lop", text="Lớp")
        self.tree.heading("sophong", text="Phòng KTX")
        self.tree.heading("ngayden", text="Thời gian đến thăm")

        self.tree.column("malan", width=65, anchor="center")
        self.tree.column("socmt", width=120, anchor="center")
        self.tree.column("tenkhach", width=180, anchor="w")
        self.tree.column("ngaysinh", width=100, anchor="center")
        self.tree.column("masv", width=95, anchor="center")
        self.tree.column("lop", width=90, anchor="center")
        self.tree.column("sophong", width=95, anchor="center")
        self.tree.column("ngayden", width=155, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def reload_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for lt in self.ktx_service.get_all_lan_tham():
            self.tree.insert("", "end", values=(
                lt.MaLanTham, lt.SoCMT, lt.TenKhach, lt.NgaySinh or "--",
                lt.MaSV, lt.Lop, lt.SoPhong or "--", lt.NgayDen
            ))

    def _add_visit(self):
        students = self.ktx_service.get_all_sinhvien()
        d = VisitModal(self, students=students)
        self.wait_window(d)
        if d.result:
            r = d.result
            ok, msg = self.ktx_service.record_visit(r["socmt"], r["tenkhach"], r["ngaysinh"], r["masv"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)


class VisitModal(tk.Toplevel):
    def __init__(self, parent, students):
        super().__init__(parent)
        self.students = students
        self.result = None
        self.title("Ghi nhận khách đến thăm KTX")
        self.geometry("450x340")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="Số CMT / CCCD Khách *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_cmt = ttk.Entry(body)
        self.entry_cmt.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Tên khách đến thăm *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_name = ttk.Entry(body)
        self.entry_name.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Ngày sinh khách (YYYY-MM-DD)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.entry_ns = ttk.Entry(body)
        self.entry_ns.pack(fill=tk.X, pady=(0, 8))

        tk.Label(body, text="Sinh viên đến thăm *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE).pack(anchor="w")
        self.sv_opts = [f"{s.MaSV} (Lớp: {s.Lop})" for s in self.students]
        self.sv_var = tk.StringVar(value=self.sv_opts[0] if self.sv_opts else "")
        self.cb_sv = ttk.Combobox(body, textvariable=self.sv_var, values=self.sv_opts, state="readonly")
        self.cb_sv.pack(fill=tk.X, pady=(0, 16))

        btn_box = tk.Frame(body, bg=Theme.SURFACE)
        btn_box.pack(fill=tk.X)
        ttk.Button(btn_box, text="Ghi nhận", style="Primary.TButton", command=self._save).pack(side=tk.RIGHT, padx=4)
        ttk.Button(btn_box, text="Huỷ", command=self.destroy).pack(side=tk.RIGHT, padx=4)

    def _save(self):
        cmt = self.entry_cmt.get().strip()
        name = self.entry_name.get().strip()
        ns = self.entry_ns.get().strip()
        sv_str = self.sv_var.get()
        masv = sv_str.split(" ")[0]
        self.result = {"socmt": cmt, "tenkhach": name, "ngaysinh": ns, "masv": masv}
        self.destroy()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from services.ktx_service import KTXService
from ui.theme import Theme

class KTXReportView(tk.Frame):
    def __init__(self, parent, ktx_service: KTXService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.ktx_service = ktx_service
        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="📑 4 BÁO CÁO PROJECT KÝ TÚC XÁ",
            font=Theme.FONT_TITLE,
            fg=Theme.TEXT_MAIN,
            bg=Theme.BG_MAIN
        ).pack(side=tk.LEFT)

        btn_refresh = ttk.Button(header, text="🔄 Làm mới báo cáo", command=self.reload_data)
        btn_refresh.pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        # Tab 1
        self.tab1 = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab1, text="1. Chi phí tháng SV")
        self._build_tab1()

        # Tab 2
        self.tab2 = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab2, text="2. Dịch vụ (09-10/2026)")
        self._build_tab2()

        # Tab 3
        self.tab3 = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab3, text="3. Khách thăm (T10/2026)")
        self._build_tab3()

        # Tab 4
        self.tab4 = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab4, text="4. Doanh thu dịch vụ theo tháng")
        self._build_tab4()

    def _build_tab1(self):
        ctrl = tk.Frame(self.tab1, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        tk.Label(ctrl, text="💡 Báo cáo 1: Tổng chi phí mỗi tháng của sinh viên (Tiền phòng + Tiền DV + Tiền vé xe + Phí gửi xe phát sinh)", font=Theme.FONT_SUBTITLE, fg=Theme.PRIMARY, bg=Theme.BG_MAIN).pack(side=tk.LEFT)
        ttk.Button(ctrl, text="📤 Xuất CSV", command=lambda: self._export_tree_csv(self.tree1, "bao_cao_1_chi_phi_thang.csv")).pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.tab1, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("masv", "lop", "quequan", "kythu", "tienphong", "tiendv", "tienvexe", "tienphatxe", "tongchi")
        self.tree1 = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree1.heading("masv", text="Mã SV")
        self.tree1.heading("lop", text="Lớp")
        self.tree1.heading("quequan", text="Quê quán")
        self.tree1.heading("kythu", text="Kỳ thu")
        self.tree1.heading("tienphong", text="Tiền phòng")
        self.tree1.heading("tiendv", text="Tiền DV khác")
        self.tree1.heading("tienvexe", text="Tiền vé xe tháng")
        self.tree1.heading("tienphatxe", text="Phí gửi xe phát sinh")
        self.tree1.heading("tongchi", text="Tổng chi phí tháng")

        self.tree1.column("masv", width=85, anchor="center")
        self.tree1.column("lop", width=85, anchor="center")
        self.tree1.column("quequan", width=110, anchor="w")
        self.tree1.column("kythu", width=75, anchor="center")
        self.tree1.column("tienphong", width=105, anchor="center")
        self.tree1.column("tiendv", width=105, anchor="center")
        self.tree1.column("tienvexe", width=115, anchor="center")
        self.tree1.column("tienphatxe", width=125, anchor="center")
        self.tree1.column("tongchi", width=130, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=vsb.set)
        self.tree1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab2(self):
        ctrl = tk.Frame(self.tab2, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        tk.Label(ctrl, text="💡 Báo cáo 2: Sinh viên cùng tên dịch vụ, tổng giá trị mỗi dịch vụ sử dụng từ ngày 2026-09-01 đến 2026-10-31", font=Theme.FONT_SUBTITLE, fg=Theme.PRIMARY, bg=Theme.BG_MAIN).pack(side=tk.LEFT)
        ttk.Button(ctrl, text="📤 Xuất CSV", command=lambda: self._export_tree_csv(self.tree2, "bao_cao_2_dich_vu_su_dung.csv")).pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.tab2, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("masv", "lop", "madv", "tendv", "soluong", "thanhtien")
        self.tree2 = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree2.heading("masv", text="Mã SV")
        self.tree2.heading("lop", text="Lớp")
        self.tree2.heading("madv", text="Mã DV")
        self.tree2.heading("tendv", text="Tên dịch vụ")
        self.tree2.heading("soluong", text="Tổng số lượng SD")
        self.tree2.heading("thanhtien", text="Tổng tiền thanh toán")

        self.tree2.column("masv", width=95, anchor="center")
        self.tree2.column("lop", width=95, anchor="center")
        self.tree2.column("madv", width=95, anchor="center")
        self.tree2.column("tendv", width=220, anchor="w")
        self.tree2.column("soluong", width=130, anchor="center")
        self.tree2.column("thanhtien", width=150, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=vsb.set)
        self.tree2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab3(self):
        ctrl = tk.Frame(self.tab3, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        tk.Label(ctrl, text="💡 Báo cáo 3: Sinh viên cùng thông tin khách đến thăm trong Tháng 10/2026, kèm số lần đến chơi", font=Theme.FONT_SUBTITLE, fg=Theme.PRIMARY, bg=Theme.BG_MAIN).pack(side=tk.LEFT)
        ttk.Button(ctrl, text="📤 Xuất CSV", command=lambda: self._export_tree_csv(self.tree3, "bao_cao_3_khach_den_tham.csv")).pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.tab3, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("masv", "lop", "socmt", "tenkhach", "ngaysinh", "solan")
        self.tree3 = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree3.heading("masv", text="Mã SV")
        self.tree3.heading("lop", text="Lớp")
        self.tree3.heading("socmt", text="Số CMT Khách")
        self.tree3.heading("tenkhach", text="Tên khách đến thăm")
        self.tree3.heading("ngaysinh", text="Ngày sinh khách")
        self.tree3.heading("solan", text="Số lần đến chơi")

        self.tree3.column("masv", width=95, anchor="center")
        self.tree3.column("lop", width=95, anchor="center")
        self.tree3.column("socmt", width=130, anchor="center")
        self.tree3.column("tenkhach", width=180, anchor="w")
        self.tree3.column("ngaysinh", width=110, anchor="center")
        self.tree3.column("solan", width=110, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree3.yview)
        self.tree3.configure(yscrollcommand=vsb.set)
        self.tree3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_tab4(self):
        ctrl = tk.Frame(self.tab4, bg=Theme.BG_MAIN, pady=10)
        ctrl.pack(fill=tk.X)
        tk.Label(ctrl, text="💡 Báo cáo 4: Danh mục dịch vụ cùng tổng doanh thu trong mỗi tháng", font=Theme.FONT_SUBTITLE, fg=Theme.PRIMARY, bg=Theme.BG_MAIN).pack(side=tk.LEFT)
        ttk.Button(ctrl, text="📤 Xuất CSV", command=lambda: self._export_tree_csv(self.tree4, "bao_cao_4_doanh_thu_dich_vu.csv")).pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.tab4, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("madv", "tendv", "kythu", "soluong", "doanhthu")
        self.tree4 = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree4.heading("madv", text="Mã DV")
        self.tree4.heading("tendv", text="Tên dịch vụ")
        self.tree4.heading("kythu", text="Tháng/Năm")
        self.tree4.heading("soluong", text="Tổng số lượng SD")
        self.tree4.heading("doanhthu", text="Tổng doanh thu")

        self.tree4.column("madv", width=100, anchor="center")
        self.tree4.column("tendv", width=240, anchor="w")
        self.tree4.column("kythu", width=100, anchor="center")
        self.tree4.column("soluong", width=130, anchor="center")
        self.tree4.column("doanhthu", width=150, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree4.yview)
        self.tree4.configure(yscrollcommand=vsb.set)
        self.tree4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def reload_data(self):
        # 1. Report 1
        for r in self.tree1.get_children():
            self.tree1.delete(r)
        r1 = self.ktx_service.get_report_1()
        for item in r1:
            self.tree1.insert("", "end", values=(
                item["MaSV"], item["Lop"], item["QueQuan"], f"{item['Thang']}/{item['Nam']}",
                f"{item['TienPhong']:,.0f} đ", f"{item['TienDichVuKhac']:,.0f} đ",
                f"{item['TienVeXeThang']:,.0f} đ", f"{item['TienPhatGuiXe']:,.0f} đ",
                f"{item['TongChiPhiThang']:,.0f} đ"
            ))

        # 2. Report 2
        for r in self.tree2.get_children():
            self.tree2.delete(r)
        r2 = self.ktx_service.get_report_2()
        for item in r2:
            self.tree2.insert("", "end", values=(
                item["MaSV"], item["Lop"], item["MaDV"], item["TenDV"],
                item["TongSoLuongSuDung"], f"{item['TongTienThanhToan']:,.0f} đ"
            ))

        # 3. Report 3
        for r in self.tree3.get_children():
            self.tree3.delete(r)
        r3 = self.ktx_service.get_report_3()
        for item in r3:
            self.tree3.insert("", "end", values=(
                item["MaSV"], item["Lop"], item["SoCMT"], item["TenKhach"],
                item["NgaySinhKhach"] or "--", f"{item['SoLanDenChoi']} lần"
            ))

        # 4. Report 4
        for r in self.tree4.get_children():
            self.tree4.delete(r)
        r4 = self.ktx_service.get_report_4()
        for item in r4:
            self.tree4.insert("", "end", values=(
                item["MaDV"], item["TenDV"], f"{item['Thang']}/{item['Nam']}",
                item["TongSoLuongSuDung"], f"{item['TongDoanhThu']:,.0f} đ"
            ))

    def _export_tree_csv(self, tree: ttk.Treeview, default_name: str):
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Lưu báo cáo ra CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=default_name
        )
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                columns = tree["columns"]
                headers = [tree.heading(col)["text"] for col in columns]
                writer.writerow(headers)

                for row_id in tree.get_children():
                    writer.writerow(tree.item(row_id)["values"])

            messagebox.showinfo("Thành công", f"Đã xuất báo cáo ra file:\n{file_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}", parent=self)

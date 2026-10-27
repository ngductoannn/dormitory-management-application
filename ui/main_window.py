import tkinter as tk
from tkinter import messagebox
from database.db_manager import DatabaseManager
from services.ktx_service import KTXService
from ui.theme import Theme
from ui.views.ktx_views import (
    KTXDashboardView,
    KTXSinhVienView,
    KTXPhongView,
    KTXHoaDonDichVuView,
    KTXParkingView,
    KTXVisitorsView
)
from ui.views.report_view import KTXReportView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hệ Thống Quản Lý Ký Túc Xá Sinh Viên (QL_KTX)")
        self.geometry("1260x800")
        self.minsize(1050, 700)
        self.configure(bg=Theme.BG_MAIN)

        # Center on screen
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w = 1260
        h = 800
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{max(0, x)}+{max(0, y)}")

        # Services
        self.db = DatabaseManager()
        self.ktx_service = KTXService(self.db)

        # Theme
        Theme.apply_theme(self)

        self._build_layout()
        self._switch_view("dashboard")

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=Theme.SIDEBAR_BG, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Main content
        self.content_container = tk.Frame(self, bg=Theme.BG_MAIN)
        self.content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_sidebar()
        self._build_views()

    def _build_sidebar(self):
        # Brand
        brand_frame = tk.Frame(self.sidebar, bg=Theme.SIDEBAR_BG, padx=20, pady=22)
        brand_frame.pack(fill=tk.X)

        tk.Label(
            brand_frame,
            text="🏛️ QL_KTX",
            font=("Helvetica Neue", 16, "bold"),
            fg="#60A5FA",
            bg=Theme.SIDEBAR_BG
        ).pack(anchor="w")

        tk.Label(
            brand_frame,
            text="Hệ Thống Ký Túc Xá Sinh Viên",
            font=("Helvetica Neue", 10),
            fg=Theme.SIDEBAR_MUTED,
            bg=Theme.SIDEBAR_BG
        ).pack(anchor="w", pady=(2, 0))

        # Divider
        tk.Frame(self.sidebar, bg="#334155", height=1).pack(fill=tk.X, padx=16, pady=(0, 12))

        # Navigation menu
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊  Tổng quan KTX"),
            ("sinhvien", "👥  Hồ sơ Sinh viên"),
            ("phong", "🛏️  Phòng & Xếp phòng"),
            ("hoadon", "🧾  Hoá đơn & Dịch vụ"),
            ("xe", "🛵  Quản lý Xe KTX"),
            ("khach", "🧑‍🤝‍🧑  Khách đến thăm"),
            ("report", "📑  4 Báo Cáo Project"),
        ]

        for key, label in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {label}",
                font=("Helvetica Neue", 11, "bold"),
                fg=Theme.SIDEBAR_TEXT,
                bg=Theme.SIDEBAR_BG,
                activebackground=Theme.SIDEBAR_ITEM,
                activeforeground=Theme.TEXT_WHITE,
                bd=0,
                padx=16,
                pady=10,
                anchor="w",
                cursor="hand2",
                command=lambda k=key: self._switch_view(k)
            )
            btn.pack(fill=tk.X, pady=2, padx=8)
            self.nav_buttons[key] = btn

        # Bottom info
        bottom = tk.Frame(self.sidebar, bg=Theme.SIDEBAR_BG, padx=16, pady=18)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)

        badge = tk.Frame(bottom, bg="#1E293B", padx=10, pady=8)
        badge.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            badge,
            text="● SQLite: 10 Bảng + 2 Triggers",
            font=("Helvetica Neue", 9),
            fg="#34D399",
            bg="#1E293B"
        ).pack(anchor="w")

        btn_reset = tk.Button(
            bottom,
            text="↻ Khôi phục CSDL mẫu (33 SV)",
            font=("Helvetica Neue", 9),
            fg=Theme.SIDEBAR_MUTED,
            bg=Theme.SIDEBAR_BG,
            activeforeground="#EF4444",
            bd=0,
            cursor="hand2",
            command=self._reset_db_prompt
        )
        btn_reset.pack(anchor="w")

    def _build_views(self):
        self.views = {
            "dashboard": KTXDashboardView(self.content_container, self.ktx_service, nav_callback=self._switch_view),
            "sinhvien": KTXSinhVienView(self.content_container, self.ktx_service),
            "phong": KTXPhongView(self.content_container, self.ktx_service),
            "hoadon": KTXHoaDonDichVuView(self.content_container, self.ktx_service),
            "xe": KTXParkingView(self.content_container, self.ktx_service),
            "khach": KTXVisitorsView(self.content_container, self.ktx_service),
            "report": KTXReportView(self.content_container, self.ktx_service),
        }

    def _switch_view(self, key: str):
        for k, v in self.views.items():
            if k == key:
                v.pack(fill=tk.BOTH, expand=True)
                if hasattr(v, "reload_data"):
                    v.reload_data()
                elif hasattr(v, "refresh"):
                    v.refresh()
            else:
                v.pack_forget()

        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(bg=Theme.SIDEBAR_ACTIVE, fg=Theme.TEXT_WHITE)
            else:
                btn.configure(bg=Theme.SIDEBAR_BG, fg=Theme.SIDEBAR_TEXT)

    def _reset_db_prompt(self):
        ans = messagebox.askyesno(
            "Khôi phục CSDL mẫu",
            "Bạn có chắc muốn đặt lại cơ sở dữ liệu về trạng thái ban đầu?\nToàn bộ dữ liệu bạn tự thêm sẽ bị xoá.",
            parent=self
        )
        if ans:
            self.db.reset_database()
            messagebox.showinfo("Thành công", "Đã khởi tạo lại 10 bảng CSDL QL_KTX với đầy đủ 33 sinh viên và các triggers!", parent=self)
            self._switch_view("dashboard")

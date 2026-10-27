import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from services.grade_service import GradeService
from services.student_service import StudentService
from ui.theme import Theme

class DashboardView(tk.Frame):
    def __init__(
        self,
        parent,
        student_service: StudentService,
        grade_service: GradeService,
        nav_callback: Optional[Callable[[str], None]] = None
    ):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.student_service = student_service
        self.grade_service = grade_service
        self.nav_callback = nav_callback

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # Scrollable Canvas container for dashboard
        self.canvas = tk.Canvas(self, bg=Theme.BG_MAIN, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=Theme.BG_MAIN, padx=24, pady=20)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(xscrollcommand=None, yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Title bar
        title_frame = tk.Frame(self.scrollable_frame, bg=Theme.BG_MAIN)
        title_frame.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            title_frame,
            text="BẢNG ĐIỀU KHIỂN TRUNG TÂM (DASHBOARD)",
            font=Theme.FONT_TITLE,
            fg=Theme.TEXT_MAIN,
            bg=Theme.BG_MAIN
        ).pack(side=tk.LEFT)

        btn_refresh = ttk.Button(title_frame, text="🔄 Làm mới dữ liệu", command=self.refresh)
        btn_refresh.pack(side=tk.RIGHT)

        # 4 Metric Cards Frame
        self.cards_frame = tk.Frame(self.scrollable_frame, bg=Theme.BG_MAIN)
        self.cards_frame.pack(fill=tk.X, pady=(0, 20))
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Content 2 columns
        self.grid_frame = tk.Frame(self.scrollable_frame, bg=Theme.BG_MAIN)
        self.grid_frame.pack(fill=tk.BOTH, expand=True)
        self.grid_frame.grid_columnconfigure(0, weight=6)
        self.grid_frame.grid_columnconfigure(1, weight=4)

        # Left Column: Top Students Table
        left_card = tk.Frame(self.grid_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=16)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(left_card, text="🏆 TOP SINH VIÊN XUẤT SẮC (GPA CAO NHẤT)", font=Theme.FONT_HEADER, fg=Theme.TEXT_MAIN, bg=Theme.SURFACE).pack(anchor="w", pady=(0, 12))

        cols = ("rank", "code", "name", "class", "faculty", "gpa", "credits")
        self.tree_top = ttk.Treeview(left_card, columns=cols, show="headings", height=6)
        self.tree_top.heading("rank", text="Top")
        self.tree_top.heading("code", text="MSSV")
        self.tree_top.heading("name", text="Họ và tên")
        self.tree_top.heading("class", text="Lớp")
        self.tree_top.heading("faculty", text="Khoa")
        self.tree_top.heading("gpa", text="GPA / 4.0")
        self.tree_top.heading("credits", text="Số TC")

        self.tree_top.column("rank", width=45, anchor="center")
        self.tree_top.column("code", width=100, anchor="center")
        self.tree_top.column("name", width=150, anchor="w")
        self.tree_top.column("class", width=90, anchor="center")
        self.tree_top.column("faculty", width=120, anchor="w")
        self.tree_top.column("gpa", width=75, anchor="center")
        self.tree_top.column("credits", width=60, anchor="center")
        self.tree_top.pack(fill=tk.BOTH, expand=True)

        # Right Column: Academic Ranking Chart (Canvas)
        right_card = tk.Frame(self.grid_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=16)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        tk.Label(right_card, text="📊 PHÂN BỐ XẾP LOẠI HỌC LỰC", font=Theme.FONT_HEADER, fg=Theme.TEXT_MAIN, bg=Theme.SURFACE).pack(anchor="w", pady=(0, 12))

        self.chart_canvas = tk.Canvas(right_card, bg=Theme.SURFACE, height=220, highlightthickness=0)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True)

    def _create_card(self, parent, col, title, value, subtitle, icon_color):
        card = tk.Frame(parent, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=14)
        card.grid(row=0, column=col, sticky="nsew", padx=6)

        # Top line accent
        accent = tk.Frame(card, bg=icon_color, height=4)
        accent.pack(fill=tk.X, side=tk.TOP, pady=(0, 8))

        tk.Label(card, text=title, font=Theme.FONT_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.SURFACE).pack(anchor="w")
        tk.Label(card, text=str(value), font=Theme.FONT_STAT_NUM, fg=icon_color, bg=Theme.SURFACE).pack(anchor="w", pady=4)
        tk.Label(card, text=subtitle, font=Theme.FONT_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.SURFACE).pack(anchor="w")

    def refresh(self):
        # Refresh Cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        stats = self.grade_service.get_overview_stats()
        self._create_card(self.cards_frame, 0, "TỔNG SINH VIÊN", stats.get("total_students", 0), "Hồ sơ trong hệ thống", Theme.PRIMARY)
        self._create_card(self.cards_frame, 1, "GPA TRUNG BÌNH TOÀN TRƯỜNG", f"{stats.get('overall_avg_gpa') or 0.0:.2f}", "Thang điểm 4.0", Theme.SUCCESS)
        self._create_card(self.cards_frame, 2, "TỔNG SỐ HỌC PHẦN", stats.get("total_courses", 0), "Môn học đào tạo", Theme.WARNING)
        self._create_card(self.cards_frame, 3, "TỔNG SỐ LỚP HỌC", stats.get("total_classes", 0), "Lớp sinh hoạt", Theme.INFO)

        # Refresh Top Students
        for row in self.tree_top.get_children():
            self.tree_top.delete(row)

        top_list = self.grade_service.get_top_students(limit=6)
        rank_medals = ["🥇 1", "🥈 2", "🥉 3", "4", "5", "6"]
        for idx, s in enumerate(top_list):
            rank = rank_medals[idx] if idx < len(rank_medals) else str(idx + 1)
            self.tree_top.insert("", "end", values=(
                rank,
                s["student_code"],
                s["full_name"],
                s["class_code"] or "--",
                s["faculty_name"] or "--",
                f"{s['gpa']:.2f}",
                s["total_credits"]
            ))

        # Refresh Ranking Bars on Canvas
        self._draw_ranking_chart()

    def _draw_ranking_chart(self):
        self.chart_canvas.delete("all")
        dist = self.grade_service.get_grade_distribution()
        
        # Standard buckets
        buckets = [
            ("Xuất sắc (3.6 - 4.0)", Theme.SUCCESS),
            ("Giỏi (3.2 - 3.59)", Theme.PRIMARY),
            ("Khá (2.5 - 3.19)", Theme.INFO),
            ("Trung bình (2.0 - 2.49)", Theme.WARNING),
            ("Yếu / Kém (< 2.0)", Theme.DANGER)
        ]
        counts_map = {d["ranking"]: d["count"] for d in dist}
        total = sum(counts_map.values()) or 1

        canvas_width = self.chart_canvas.winfo_width() or 340
        start_y = 15
        row_height = 40

        for idx, (label, color) in enumerate(buckets):
            cnt = counts_map.get(label, 0)
            pct = (cnt / total) * 100
            y = start_y + idx * row_height

            # Label + count
            self.chart_canvas.create_text(
                10, y,
                anchor="w",
                text=f"{label}: {cnt} SV ({pct:.0f}%)",
                font=Theme.FONT_SMALL,
                fill=Theme.TEXT_MAIN
            )

            # Progress Bar Background
            bar_y = y + 14
            bar_width = max(100, canvas_width - 30)
            self.chart_canvas.create_rectangle(
                10, bar_y, 10 + bar_width, bar_y + 12,
                fill="#F1F5F9", outline="#E2E8F0"
            )

            # Fill Progress
            fill_len = (pct / 100.0) * bar_width
            if fill_len > 0:
                self.chart_canvas.create_rectangle(
                    10, bar_y, 10 + fill_len, bar_y + 12,
                    fill=color, outline=""
                )

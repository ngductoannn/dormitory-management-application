import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.grade_service import GradeService
from services.course_service import CourseService
from ui.theme import Theme

class StatsView(tk.Frame):
    def __init__(self, parent, grade_service: GradeService, course_service: CourseService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.grade_service = grade_service
        self.course_service = course_service

        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        # Action Bar
        action_bar = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        action_bar.pack(fill=tk.X)

        tk.Label(action_bar, text="BÁO CÁO & THỐNG KÊ CHI TIẾT", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        btn_box = tk.Frame(action_bar, bg=Theme.BG_MAIN)
        btn_box.pack(side=tk.RIGHT)

        btn_refresh = ttk.Button(btn_box, text="🔄 Làm mới", command=self.reload_data)
        btn_refresh.pack(side=tk.LEFT, padx=4)

        btn_export = ttk.Button(btn_box, text="📥 Xuất báo cáo TXT", command=self._export_report)
        btn_export.pack(side=tk.LEFT, padx=4)

        # Content 2 Column Panels
        content_frame = tk.Frame(self, bg=Theme.BG_MAIN, padx=20)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Panel 1: Sinh viên theo Khoa
        p1 = tk.Frame(content_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=16)
        p1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(p1, text="🏛️ PHÂN BỐ SINH VIÊN THEO KHOA", font=Theme.FONT_HEADER, fg=Theme.TEXT_MAIN, bg=Theme.SURFACE).pack(anchor="w", pady=(0, 10))

        cols1 = ("faculty", "students", "percent")
        self.tree_fac = ttk.Treeview(p1, columns=cols1, show="headings", height=8)
        self.tree_fac.heading("faculty", text="Khoa đào tạo")
        self.tree_fac.heading("students", text="Số lượng SV")
        self.tree_fac.heading("percent", text="Tỷ lệ %")

        self.tree_fac.column("faculty", width=220, anchor="w")
        self.tree_fac.column("students", width=100, anchor="center")
        self.tree_fac.column("percent", width=100, anchor="center")
        self.tree_fac.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        self.canvas_fac = tk.Canvas(p1, bg=Theme.SURFACE, height=140, highlightthickness=0)
        self.canvas_fac.pack(fill=tk.BOTH, expand=True)

        # Panel 2: Xếp loại học lực
        p2 = tk.Frame(content_frame, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=16)
        p2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        tk.Label(p2, text="🎖️ XẾP LOẠI HỌC LỰC TOÀN TRƯỜNG", font=Theme.FONT_HEADER, fg=Theme.TEXT_MAIN, bg=Theme.SURFACE).pack(anchor="w", pady=(0, 10))

        cols2 = ("rank", "count", "percent")
        self.tree_rank = ttk.Treeview(p2, columns=cols2, show="headings", height=8)
        self.tree_rank.heading("rank", text="Xếp loại (Thang điểm 4)")
        self.tree_rank.heading("count", text="Số lượng SV")
        self.tree_rank.heading("percent", text="Tỷ lệ %")

        self.tree_rank.column("rank", width=220, anchor="w")
        self.tree_rank.column("count", width=100, anchor="center")
        self.tree_rank.column("percent", width=100, anchor="center")
        self.tree_rank.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        self.canvas_rank = tk.Canvas(p2, bg=Theme.SURFACE, height=140, highlightthickness=0)
        self.canvas_rank.pack(fill=tk.BOTH, expand=True)

    def reload_data(self):
        # 1. Faculty Stats
        for r in self.tree_fac.get_children():
            self.tree_fac.delete(r)

        fac_dist = self.grade_service.get_faculty_distribution()
        total_fac_sv = sum(f["count"] for f in fac_dist) or 1

        for f in fac_dist:
            cnt = f["count"]
            pct = (cnt / total_fac_sv) * 100
            self.tree_fac.insert("", "end", values=(f["faculty_name"], f"{cnt} SV", f"{pct:.1f}%"))

        self._draw_bars(self.canvas_fac, [(f["faculty_name"], f["count"]) for f in fac_dist], total_fac_sv, Theme.PRIMARY)

        # 2. Grade Ranking Stats
        for r in self.tree_rank.get_children():
            self.tree_rank.delete(r)

        rank_dist = self.grade_service.get_grade_distribution()
        total_ranked = sum(r["count"] for r in rank_dist) or 1

        for r in rank_dist:
            cnt = r["count"]
            pct = (cnt / total_ranked) * 100
            self.tree_rank.insert("", "end", values=(r["ranking"], f"{cnt} SV", f"{pct:.1f}%"))

        self._draw_bars(self.canvas_rank, [(r["ranking"], r["count"]) for r in rank_dist], total_ranked, Theme.SUCCESS)

    def _draw_bars(self, canvas: tk.Canvas, data_items, total, bar_color):
        canvas.delete("all")
        w = canvas.winfo_width() or 340
        y = 12
        h = 24

        for label, count in data_items:
            pct = (count / total) * 100
            canvas.create_text(10, y, anchor="w", text=f"{label} ({count})", font=Theme.FONT_SMALL, fill=Theme.TEXT_MAIN)
            
            bar_y = y + 10
            bar_w = max(100, w - 24)
            canvas.create_rectangle(10, bar_y, 10 + bar_w, bar_y + 8, fill="#F1F5F9", outline="#E2E8F0")
            fill_w = (pct / 100.0) * bar_w
            if fill_w > 0:
                canvas.create_rectangle(10, bar_y, 10 + fill_w, bar_y + 8, fill=bar_color, outline="")
            y += h + 10

    def _export_report(self):
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Lưu báo cáo thống kê",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="bao_cao_thong_ke_sinh_vien.txt"
        )
        if not file_path:
            return

        try:
            stats = self.grade_service.get_overview_stats()
            fac_dist = self.grade_service.get_faculty_distribution()
            rank_dist = self.grade_service.get_grade_distribution()
            top_students = self.grade_service.get_top_students(10)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("      BÁO CÁO TỔNG HỢP HỆ THỐNG QUẢN LÝ SINH VIÊN\n")
                f.write("=" * 60 + "\n\n")

                f.write("1. TỔNG QUAN HỆ THỐNG:\n")
                f.write(f"- Tổng số sinh viên: {stats.get('total_students', 0)}\n")
                f.write(f"- Tổng số môn học: {stats.get('total_courses', 0)}\n")
                f.write(f"- Tổng số lớp sinh hoạt: {stats.get('total_classes', 0)}\n")
                f.write(f"- Điểm GPA trung bình toàn trường: {stats.get('overall_avg_gpa', 0.0):.2f} / 4.0\n\n")

                f.write("2. PHÂN BỐ SINH VIÊN THEO KHOA:\n")
                for item in fac_dist:
                    f.write(f"- {item['faculty_name']}: {item['count']} sinh viên\n")
                f.write("\n")

                f.write("3. PHÂN BỐ XẾP LOẠI HỌC LỰC:\n")
                for item in rank_dist:
                    f.write(f"- {item['ranking']}: {item['count']} sinh viên\n")
                f.write("\n")

                f.write("4. TOP 10 SINH VIÊN XUẤT SẮC NHẤT:\n")
                for idx, s in enumerate(top_students, 1):
                    f.write(f"{idx}. [{s['student_code']}] {s['full_name']} | Lớp: {s['class_code']} | GPA: {s['gpa']:.2f} ({s['total_credits']} TC)\n")

            messagebox.showinfo("Thành công", f"Đã xuất báo cáo ra file:\n{file_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất báo cáo: {str(e)}", parent=self)

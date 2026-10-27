import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
from services.grade_service import GradeService
from services.student_service import StudentService
from services.course_service import CourseService
from services.export_service import ExportService
from ui.dialogs.grade_dialog import GradeDialog
from ui.theme import Theme
from models.grade import Grade

class GradeView(tk.Frame):
    def __init__(
        self,
        parent,
        student_service: StudentService,
        grade_service: GradeService,
        course_service: CourseService
    ):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.student_service = student_service
        self.grade_service = grade_service
        self.course_service = course_service

        self.all_grades = []
        self.courses = []
        self.students = []

        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        # Action Bar
        action_bar = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        action_bar.pack(fill=tk.X)

        tk.Label(action_bar, text="QUẢN LÝ ĐIỂM SỐ & KẾT QUẢ HỌC TẬP", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        btn_box = tk.Frame(action_bar, bg=Theme.BG_MAIN)
        btn_box.pack(side=tk.RIGHT)

        btn_add = ttk.Button(btn_box, text="➕ Nhập điểm môn", style="Primary.TButton", command=self._add_grade)
        btn_add.pack(side=tk.LEFT, padx=4)

        btn_edit = ttk.Button(btn_box, text="✏️ Chỉnh sửa", command=self._edit_selected)
        btn_edit.pack(side=tk.LEFT, padx=4)

        btn_del = ttk.Button(btn_box, text="🗑️ Xoá điểm", style="Danger.TButton", command=self._delete_selected)
        btn_del.pack(side=tk.LEFT, padx=4)

        btn_export = ttk.Button(btn_box, text="📤 Xuất bảng điểm CSV", command=self._export_csv)
        btn_export.pack(side=tk.LEFT, padx=4)

        # Notebook tabs: "Toàn bộ điểm" and "Bảng điểm cá nhân"
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        # Tab 1: All Grades
        self.tab_all = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab_all, text="📋 Danh sách điểm môn học")
        self._build_tab_all()

        # Tab 2: Individual Student Transcript
        self.tab_individual = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab_individual, text="🎓 Tra cứu bảng điểm cá nhân")
        self._build_tab_individual()

    def _build_tab_all(self):
        # Filter frame
        filter_card = tk.Frame(self.tab_all, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=12)
        filter_card.pack(fill=tk.X, pady=(12, 10))

        # Search Entry
        f_search = tk.Frame(filter_card, bg=Theme.SURFACE)
        f_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(f_search, text="🔍 Tìm sinh viên (MSSV, Họ tên):", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.entry_search = ttk.Entry(f_search)
        self.entry_search.pack(fill=tk.X, pady=(2, 0))
        self.entry_search.bind("<Return>", lambda e: self.reload_data())

        # Course Filter
        f_course = tk.Frame(filter_card, bg=Theme.SURFACE, width=200)
        f_course.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(f_course, text="Môn học:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.course_var = tk.StringVar(value="Tất cả môn")
        self.cb_course = ttk.Combobox(f_course, textvariable=self.course_var, state="readonly", width=22)
        self.cb_course.pack(pady=(2, 0))
        self.cb_course.bind("<<ComboboxSelected>>", lambda e: self.reload_data())

        # Semester Filter
        f_sem = tk.Frame(filter_card, bg=Theme.SURFACE, width=140)
        f_sem.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(f_sem, text="Học kỳ:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.sem_var = tk.StringVar(value="Tất cả")
        self.cb_sem = ttk.Combobox(f_sem, textvariable=self.sem_var, state="readonly", width=14)
        self.cb_sem.pack(pady=(2, 0))
        self.cb_sem.bind("<<ComboboxSelected>>", lambda e: self.reload_data())

        btn_filter = ttk.Button(filter_card, text="Lọc", command=self.reload_data)
        btn_filter.pack(side=tk.LEFT, pady=(14, 0))

        # Table
        table_frame = tk.Frame(self.tab_all, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = (
            "id", "student_code", "student_name", "class_code", "course_code",
            "course_name", "credits", "semester", "att", "mid", "final",
            "total", "gpa", "letter"
        )
        self.tree_all = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_all.heading("id", text="ID")
        self.tree_all.heading("student_code", text="MSSV")
        self.tree_all.heading("student_name", text="Họ và tên")
        self.tree_all.heading("class_code", text="Lớp")
        self.tree_all.heading("course_code", text="Mã môn")
        self.tree_all.heading("course_name", text="Tên môn học")
        self.tree_all.heading("credits", text="Số TC")
        self.tree_all.heading("semester", text="Học kỳ")
        self.tree_all.heading("att", text="CC (10%)")
        self.tree_all.heading("mid", text="GK (30%)")
        self.tree_all.heading("final", text="CK (60%)")
        self.tree_all.heading("total", text="Điểm TK")
        self.tree_all.heading("gpa", text="Hệ 4")
        self.tree_all.heading("letter", text="Điểm chữ")

        self.tree_all.column("id", width=35, anchor="center")
        self.tree_all.column("student_code", width=100, anchor="center")
        self.tree_all.column("student_name", width=150, anchor="w")
        self.tree_all.column("class_code", width=85, anchor="center")
        self.tree_all.column("course_code", width=80, anchor="center")
        self.tree_all.column("course_name", width=160, anchor="w")
        self.tree_all.column("credits", width=55, anchor="center")
        self.tree_all.column("semester", width=85, anchor="center")
        self.tree_all.column("att", width=65, anchor="center")
        self.tree_all.column("mid", width=65, anchor="center")
        self.tree_all.column("final", width=65, anchor="center")
        self.tree_all.column("total", width=70, anchor="center")
        self.tree_all.column("gpa", width=60, anchor="center")
        self.tree_all.column("letter", width=65, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_all.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree_all.xview)
        self.tree_all.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree_all.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree_all.bind("<Double-1>", lambda e: self._edit_selected())

    def _build_tab_individual(self):
        top_ctrl = tk.Frame(self.tab_individual, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=12)
        top_ctrl.pack(fill=tk.X, pady=(12, 10))

        tk.Label(top_ctrl, text="Chọn sinh viên để tra cứu toàn bộ bảng điểm:", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(side=tk.LEFT, padx=(0, 10))
        self.indiv_student_var = tk.StringVar()
        self.cb_indiv_student = ttk.Combobox(top_ctrl, textvariable=self.indiv_student_var, state="readonly", width=36)
        self.cb_indiv_student.pack(side=tk.LEFT, padx=(0, 10))
        self.cb_indiv_student.bind("<<ComboboxSelected>>", lambda e: self._load_individual_transcript())

        # Student Summary Header
        self.indiv_summary_card = tk.Frame(self.tab_individual, bg="#F0FDF4", bd=1, relief="solid", padx=16, pady=12)
        self.indiv_summary_card.pack(fill=tk.X, pady=(0, 10))

        self.lbl_indiv_info = tk.Label(
            self.indiv_summary_card,
            text="Vui lòng chọn sinh viên để xem kết quả học tập.",
            font=Theme.FONT_HEADER,
            fg="#15803D",
            bg="#F0FDF4"
        )
        self.lbl_indiv_info.pack(anchor="w")

        # Table for single student grades
        indiv_table_frame = tk.Frame(self.tab_individual, bg=Theme.SURFACE, bd=1, relief="solid")
        indiv_table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("sem", "code", "name", "credits", "att", "mid", "final", "total", "gpa", "letter")
        self.tree_indiv = ttk.Treeview(indiv_table_frame, columns=cols, show="headings")
        self.tree_indiv.heading("sem", text="Học kỳ")
        self.tree_indiv.heading("code", text="Mã môn")
        self.tree_indiv.heading("name", text="Tên môn học")
        self.tree_indiv.heading("credits", text="Số TC")
        self.tree_indiv.heading("att", text="CC (10%)")
        self.tree_indiv.heading("mid", text="GK (30%)")
        self.tree_indiv.heading("final", text="CK (60%)")
        self.tree_indiv.heading("total", text="Điểm TK (Hệ 10)")
        self.tree_indiv.heading("gpa", text="Điểm hệ 4")
        self.tree_indiv.heading("letter", text="Điểm chữ")

        self.tree_indiv.column("sem", width=90, anchor="center")
        self.tree_indiv.column("code", width=85, anchor="center")
        self.tree_indiv.column("name", width=200, anchor="w")
        self.tree_indiv.column("credits", width=60, anchor="center")
        self.tree_indiv.column("att", width=80, anchor="center")
        self.tree_indiv.column("mid", width=80, anchor="center")
        self.tree_indiv.column("final", width=80, anchor="center")
        self.tree_indiv.column("total", width=110, anchor="center")
        self.tree_indiv.column("gpa", width=90, anchor="center")
        self.tree_indiv.column("letter", width=80, anchor="center")

        vsb2 = ttk.Scrollbar(indiv_table_frame, orient="vertical", command=self.tree_indiv.yview)
        self.tree_indiv.configure(yscrollcommand=vsb2.set)

        self.tree_indiv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb2.pack(side=tk.RIGHT, fill=tk.Y)

    def reload_data(self):
        self.courses = self.course_service.get_all_courses()
        self.students = self.student_service.get_all_students()

        # Update Course Filter Combobox
        course_opts = ["Tất cả môn"] + [f"{c.code} - {c.name}" for c in self.courses]
        self.cb_course["values"] = course_opts

        # Update Semester Combobox
        sems = ["Tất cả"] + self.grade_service.get_distinct_semesters()
        self.cb_sem["values"] = sems

        # Update Individual Student Combobox
        stu_opts = [f"{s.student_code} - {s.full_name}" for s in self.students]
        self.cb_indiv_student["values"] = stu_opts
        if stu_opts and not self.indiv_student_var.get():
            self.indiv_student_var.set(stu_opts[0])
            self._load_individual_transcript()

        # Filter All Grades
        keyword = self.entry_search.get().strip()
        course_id = None
        sel_c = self.course_var.get()
        for c in self.courses:
            if sel_c.startswith(c.code + " -"):
                course_id = c.id
                break

        semester = self.sem_var.get()

        self.all_grades = self.grade_service.get_all_grades(
            keyword=keyword,
            course_id=course_id,
            semester=semester
        )

        for row in self.tree_all.get_children():
            self.tree_all.delete(row)

        for g in self.all_grades:
            tag = "pass" if (g.total_score or 0) >= 4.0 else "fail"
            self.tree_all.insert("", "end", values=(
                g.id,
                g.student_code,
                g.student_name,
                g.class_code or "--",
                g.course_code,
                g.course_name,
                g.credits,
                g.semester,
                f"{g.attendance_score:.1f}" if g.attendance_score is not None else "--",
                f"{g.midterm_score:.1f}" if g.midterm_score is not None else "--",
                f"{g.final_score:.1f}" if g.final_score is not None else "--",
                f"{g.total_score:.2f}" if g.total_score is not None else "--",
                f"{g.gpa_score:.1f}" if g.gpa_score is not None else "--",
                g.letter_grade or "--"
            ), tags=(tag,))

        self.tree_all.tag_configure("pass", foreground=Theme.TEXT_MAIN)
        self.tree_all.tag_configure("fail", foreground=Theme.DANGER)

    def select_student(self, student_id: int):
        self.reload_data()
        for idx, s in enumerate(self.students):
            if s.id == student_id:
                opt = f"{s.student_code} - {s.full_name}"
                self.indiv_student_var.set(opt)
                self.notebook.select(self.tab_individual)
                self._load_individual_transcript()
                break

    def _load_individual_transcript(self):
        sel = self.indiv_student_var.get()
        if not sel:
            return

        student_code = sel.split(" - ")[0]
        student = next((s for s in self.students if s.student_code == student_code), None)
        if not student:
            return

        grades = self.grade_service.get_grades_by_student(student.id)

        for row in self.tree_indiv.get_children():
            self.tree_indiv.delete(row)

        total_credits = 0
        total_points = 0.0

        for g in grades:
            self.tree_indiv.insert("", "end", values=(
                g.semester,
                g.course_code,
                g.course_name,
                g.credits,
                f"{g.attendance_score:.1f}" if g.attendance_score is not None else "--",
                f"{g.midterm_score:.1f}" if g.midterm_score is not None else "--",
                f"{g.final_score:.1f}" if g.final_score is not None else "--",
                f"{g.total_score:.2f}" if g.total_score is not None else "--",
                f"{g.gpa_score:.1f}" if g.gpa_score is not None else "--",
                g.letter_grade or "--"
            ))
            if g.gpa_score is not None and g.credits:
                total_credits += g.credits
                total_points += g.gpa_score * g.credits

        gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
        rank = Grade.get_classification(gpa)

        summary_text = (
            f"👤 Sinh viên: {student.full_name} ({student.student_code})  |  "
            f"Lớp: {student.class_code or '--'}  |  "
            f"Tích luỹ: {total_credits} tín chỉ  |  "
            f"GPA: {gpa:.2f} / 4.0  |  "
            f"Xếp loại: {rank}"
        )
        self.lbl_indiv_info.config(text=summary_text)

    def _add_grade(self):
        dialog = GradeDialog(self, students=self.students, courses=self.courses)
        self.wait_window(dialog)
        if dialog.result:
            r = dialog.result
            ok, msg = self.grade_service.save_grade(
                r["student_id"], r["course_id"], r["semester"],
                r["attendance"], r["midterm"], r["final"]
            )
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
                self._load_individual_transcript()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _edit_selected(self):
        sel = self.tree_all.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 bản ghi điểm trong bảng.", parent=self)
            return

        grade_id = int(self.tree_all.item(sel[0], "values")[0])
        grade = next((g for g in self.all_grades if g.id == grade_id), None)
        if not grade:
            return

        dialog = GradeDialog(self, students=self.students, courses=self.courses, grade_data=grade)
        self.wait_window(dialog)
        if dialog.result:
            r = dialog.result
            ok, msg = self.grade_service.save_grade(
                r["student_id"], r["course_id"], r["semester"],
                r["attendance"], r["midterm"], r["final"]
            )
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
                self._load_individual_transcript()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_selected(self):
        sel = self.tree_all.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 bản ghi điểm cần xoá.", parent=self)
            return

        vals = self.tree_all.item(sel[0], "values")
        grade_id = int(vals[0])
        student_name = vals[2]
        course_name = vals[5]

        ans = messagebox.askyesno(
            "Xác nhận xoá",
            f"Bạn có chắc chắn muốn xoá điểm môn '{course_name}' của sinh viên '{student_name}'?",
            parent=self
        )
        if ans:
            ok, msg = self.grade_service.delete_grade(grade_id)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
                self._load_individual_transcript()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _export_csv(self):
        if not self.all_grades:
            messagebox.showwarning("Trống", "Không có dữ liệu điểm để xuất file.", parent=self)
            return

        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Lưu bảng điểm ra file CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="bang_diem_sinh_vien.csv"
        )
        if file_path:
            ok, msg = ExportService.export_grades_to_csv(file_path, self.all_grades)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

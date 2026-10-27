import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict, Any
from models.student import Student
from models.course import Course
from models.grade import Grade
from ui.theme import Theme

class GradeDialog(tk.Toplevel):
    def __init__(
        self,
        parent,
        students: List[Student],
        courses: List[Course],
        default_student_id: Optional[int] = None,
        grade_data: Optional[Grade] = None
    ):
        super().__init__(parent)
        self.students = students
        self.courses = courses
        self.grade_data = grade_data
        self.result: Optional[Dict[str, Any]] = None

        self.title("Cập nhật điểm sinh viên" if grade_data else "Nhập điểm môn học")
        self.geometry("500x560")
        self.resizable(False, False)
        self.configure(bg=Theme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._build_ui(default_student_id)

        # Center
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(10, x)}+{max(10, y)}")

    def _build_ui(self, default_student_id: Optional[int]):
        header = tk.Frame(self, bg=Theme.PRIMARY, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = "Chỉnh sửa điểm môn học" if self.grade_data else "Nhập điểm môn học"
        tk.Label(header, text=title, font=Theme.FONT_HEADER, fg=Theme.TEXT_WHITE, bg=Theme.PRIMARY).pack(side=tk.LEFT, padx=20, pady=15)

        body = tk.Frame(self, bg=Theme.SURFACE, padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Student select
        tk.Label(body, text="Sinh viên *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.student_options = [f"{s.student_code} - {s.full_name}" for s in self.students]
        self.student_map = {f"{s.student_code} - {s.full_name}": s.id for s in self.students}
        
        default_idx = 0
        if self.grade_data:
            for idx, s in enumerate(self.students):
                if s.id == self.grade_data.student_id:
                    default_idx = idx
                    break
        elif default_student_id:
            for idx, s in enumerate(self.students):
                if s.id == default_student_id:
                    default_idx = idx
                    break

        self.student_var = tk.StringVar(value=self.student_options[default_idx] if self.student_options else "")
        self.cb_student = ttk.Combobox(body, textvariable=self.student_var, values=self.student_options, state="readonly")
        self.cb_student.pack(fill=tk.X, pady=(0, 10))

        # Course select
        tk.Label(body, text="Môn học *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.course_options = [f"{c.code} - {c.name} ({c.credits} TC)" for c in self.courses]
        self.course_map = {f"{c.code} - {c.name} ({c.credits} TC)": c.id for c in self.courses}
        
        course_default_idx = 0
        if self.grade_data:
            for idx, c in enumerate(self.courses):
                if c.id == self.grade_data.course_id:
                    course_default_idx = idx
                    break

        self.course_var = tk.StringVar(value=self.course_options[course_default_idx] if self.course_options else "")
        self.cb_course = ttk.Combobox(body, textvariable=self.course_var, values=self.course_options, state="readonly")
        self.cb_course.pack(fill=tk.X, pady=(0, 10))

        # Semester
        tk.Label(body, text="Học kỳ * (Ví dụ: HK1-2024, HK2-2024)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_semester = ttk.Entry(body)
        self.entry_semester.pack(fill=tk.X, pady=(0, 14))
        if self.grade_data:
            self.entry_semester.insert(0, self.grade_data.semester)
        else:
            self.entry_semester.insert(0, "HK1-2024")

        # Score Inputs (Grid 3 cols)
        score_frame = tk.Frame(body, bg=Theme.SURFACE)
        score_frame.pack(fill=tk.X, pady=6)

        # Attendance (10%)
        col1 = tk.Frame(score_frame, bg=Theme.SURFACE)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(col1, text="Chuyên cần (10%)", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w", pady=(0, 2))
        self.entry_att = ttk.Entry(col1)
        self.entry_att.pack(fill=tk.X)
        self.entry_att.insert(0, str(self.grade_data.attendance_score if self.grade_data and self.grade_data.attendance_score is not None else "10.0"))

        # Midterm (30%)
        col2 = tk.Frame(score_frame, bg=Theme.SURFACE)
        col2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        tk.Label(col2, text="Giữa kỳ (30%)", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w", pady=(0, 2))
        self.entry_mid = ttk.Entry(col2)
        self.entry_mid.pack(fill=tk.X)
        self.entry_mid.insert(0, str(self.grade_data.midterm_score if self.grade_data and self.grade_data.midterm_score is not None else "8.0"))

        # Final (60%)
        col3 = tk.Frame(score_frame, bg=Theme.SURFACE)
        col3.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))
        tk.Label(col3, text="Cuối kỳ (60%)", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w", pady=(0, 2))
        self.entry_fin = ttk.Entry(col3)
        self.entry_fin.pack(fill=tk.X)
        self.entry_fin.insert(0, str(self.grade_data.final_score if self.grade_data and self.grade_data.final_score is not None else "8.0"))

        # Preview Result Box
        self.preview_box = tk.Frame(body, bg="#EFF6FF", bd=1, relief="solid", padx=12, pady=10)
        self.preview_box.pack(fill=tk.X, pady=(16, 6))

        self.lbl_preview = tk.Label(
            self.preview_box,
            text="Điểm tổng kết: -- | Điểm hệ 4: -- | Điểm chữ: --",
            font=Theme.FONT_BODY_BOLD,
            fg=Theme.PRIMARY,
            bg="#EFF6FF"
        )
        self.lbl_preview.pack()

        # Bind live update
        self.entry_att.bind("<KeyRelease>", lambda e: self._update_preview())
        self.entry_mid.bind("<KeyRelease>", lambda e: self._update_preview())
        self.entry_fin.bind("<KeyRelease>", lambda e: self._update_preview())
        self._update_preview()

        # Buttons
        btn_frame = tk.Frame(self, bg=Theme.BG_MAIN, pady=12)
        btn_frame.pack(fill=tk.X, padx=16)

        btn_save = ttk.Button(btn_frame, text="✓ Lưu điểm", style="Primary.TButton", command=self._on_save)
        btn_save.pack(side=tk.RIGHT, padx=6)

        btn_cancel = ttk.Button(btn_frame, text="Huỷ bỏ", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=6)

    def _update_preview(self):
        try:
            att = float(self.entry_att.get().strip() or 0)
            mid = float(self.entry_mid.get().strip() or 0)
            fin = float(self.entry_fin.get().strip() or 0)
            if 0 <= att <= 10 and 0 <= mid <= 10 and 0 <= fin <= 10:
                tot, gpa, letter = Grade.calculate_summary(att, mid, fin)
                self.lbl_preview.config(
                    text=f"Điểm tổng kết: {tot:.2f}  |  Điểm hệ 4: {gpa:.1f}  |  Điểm chữ: {letter}",
                    fg=Theme.PRIMARY
                )
            else:
                self.lbl_preview.config(text="Điểm phải nằm trong khoảng từ 0 đến 10", fg=Theme.DANGER)
        except ValueError:
            self.lbl_preview.config(text="Vui lòng nhập điểm dạng số hợp lệ", fg=Theme.WARNING)

    def _on_save(self):
        student_val = self.student_var.get()
        course_val = self.course_var.get()
        semester = self.entry_semester.get().strip()

        if not student_val or not course_val or not semester:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn đầy đủ Sinh viên, Môn học và Học kỳ.", parent=self)
            return

        try:
            att = float(self.entry_att.get().strip())
            mid = float(self.entry_mid.get().strip())
            fin = float(self.entry_fin.get().strip())
        except ValueError:
            messagebox.showerror("Sai dữ liệu", "Điểm số phải là giá trị số thực (ví dụ: 8.5).", parent=self)
            return

        if not (0 <= att <= 10 and 0 <= mid <= 10 and 0 <= fin <= 10):
            messagebox.showerror("Sai khoảng điểm", "Điểm phải nằm trong khoảng từ 0.0 đến 10.0.", parent=self)
            return

        self.result = {
            "student_id": self.student_map[student_val],
            "course_id": self.course_map[course_val],
            "semester": semester,
            "attendance": att,
            "midterm": mid,
            "final": fin
        }
        self.destroy()

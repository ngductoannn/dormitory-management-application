import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict, Any
from models.course import Course
from models.department import Faculty, StudentClass
from ui.theme import Theme

class CourseDialog(tk.Toplevel):
    def __init__(self, parent, faculties: List[Faculty], course: Optional[Course] = None):
        super().__init__(parent)
        self.faculties = faculties
        self.course = course
        self.result: Optional[Dict[str, Any]] = None

        self.title("Sửa môn học" if course else "Thêm môn học mới")
        self.geometry("450x420")
        self.resizable(False, False)
        self.configure(bg=Theme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        if course:
            self._populate(course)

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(10, x)}+{max(10, y)}")

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.PRIMARY, height=55)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = "Sửa môn học" if self.course else "Thêm môn học mới"
        tk.Label(header, text=title, font=Theme.FONT_HEADER, fg=Theme.TEXT_WHITE, bg=Theme.PRIMARY).pack(side=tk.LEFT, padx=20, pady=12)

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        tk.Label(body, text="Mã môn học * (Ví dụ: INT101)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_code = ttk.Entry(body)
        self.entry_code.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Tên môn học *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_name = ttk.Entry(body)
        self.entry_name.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Số tín chỉ (1 - 10) *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_credits = ttk.Spinbox(body, from_=1, to=10)
        self.entry_credits.set(3)
        self.entry_credits.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Khoa phụ trách", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fac_options = ["-- Không phân khoa --"] + [f"{f.code} - {f.name}" for f in self.faculties]
        self.fac_var = tk.StringVar(value=self.fac_options[0])
        self.cb_faculty = ttk.Combobox(body, textvariable=self.fac_var, values=self.fac_options, state="readonly")
        self.cb_faculty.pack(fill=tk.X, pady=(0, 10))

        btn_frame = tk.Frame(self, bg=Theme.BG_MAIN, pady=10)
        btn_frame.pack(fill=tk.X, padx=16)
        btn_save = ttk.Button(btn_frame, text="✓ Lưu môn học", style="Primary.TButton", command=self._on_save)
        btn_save.pack(side=tk.RIGHT, padx=6)
        btn_cancel = ttk.Button(btn_frame, text="Huỷ", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=6)

    def _populate(self, c: Course):
        self.entry_code.insert(0, c.code)
        self.entry_name.insert(0, c.name)
        self.entry_credits.set(c.credits)
        if c.faculty_id:
            for idx, f in enumerate(self.faculties, start=1):
                if f.id == c.faculty_id:
                    self.fac_var.set(self.fac_options[idx])
                    break

    def _on_save(self):
        code = self.entry_code.get().strip().upper()
        name = self.entry_name.get().strip()
        try:
            credits = int(self.entry_credits.get().strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Số tín chỉ phải là số nguyên dương.", parent=self)
            return

        if not code or not name:
            messagebox.showwarning("Lỗi", "Mã môn học và Tên môn không được để trống.", parent=self)
            return

        faculty_id = None
        sel_fac = self.fac_var.get()
        for f in self.faculties:
            if sel_fac.startswith(f.code + " -"):
                faculty_id = f.id
                break

        self.result = {
            "code": code,
            "name": name,
            "credits": credits,
            "faculty_id": faculty_id
        }
        self.destroy()


class ClassDialog(tk.Toplevel):
    def __init__(self, parent, faculties: List[Faculty], sclass: Optional[StudentClass] = None):
        super().__init__(parent)
        self.faculties = faculties
        self.sclass = sclass
        self.result: Optional[Dict[str, Any]] = None

        self.title("Sửa lớp học" if sclass else "Thêm lớp học mới")
        self.geometry("450x420")
        self.resizable(False, False)
        self.configure(bg=Theme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        if sclass:
            self._populate(sclass)

        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(10, x)}+{max(10, y)}")

    def _build_ui(self):
        header = tk.Frame(self, bg=Theme.PRIMARY, height=55)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = "Sửa lớp học" if self.sclass else "Thêm lớp học mới"
        tk.Label(header, text=title, font=Theme.FONT_HEADER, fg=Theme.TEXT_WHITE, bg=Theme.PRIMARY).pack(side=tk.LEFT, padx=20, pady=12)

        body = tk.Frame(self, bg=Theme.SURFACE, padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        tk.Label(body, text="Mã lớp * (Ví dụ: CNTT-K19A)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_code = ttk.Entry(body)
        self.entry_code.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Tên lớp * (Ví dụ: Kỹ thuật phần mềm 1)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_name = ttk.Entry(body)
        self.entry_name.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Khoa trực thuộc *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fac_options = [f"{f.code} - {f.name}" for f in self.faculties]
        self.fac_var = tk.StringVar(value=self.fac_options[0] if self.fac_options else "")
        self.cb_faculty = ttk.Combobox(body, textvariable=self.fac_var, values=self.fac_options, state="readonly")
        self.cb_faculty.pack(fill=tk.X, pady=(0, 10))

        tk.Label(body, text="Khoá học / Niên khoá * (Ví dụ: 2023-2027)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.entry_year = ttk.Entry(body)
        self.entry_year.pack(fill=tk.X, pady=(0, 10))
        self.entry_year.insert(0, "2023-2027")

        btn_frame = tk.Frame(self, bg=Theme.BG_MAIN, pady=10)
        btn_frame.pack(fill=tk.X, padx=16)
        btn_save = ttk.Button(btn_frame, text="✓ Lưu lớp", style="Primary.TButton", command=self._on_save)
        btn_save.pack(side=tk.RIGHT, padx=6)
        btn_cancel = ttk.Button(btn_frame, text="Huỷ", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=6)

    def _populate(self, sc: StudentClass):
        self.entry_code.insert(0, sc.code)
        self.entry_name.insert(0, sc.name)
        self.entry_year.delete(0, tk.END)
        self.entry_year.insert(0, sc.academic_year)
        if sc.faculty_id:
            for idx, f in enumerate(self.faculties):
                if f.id == sc.faculty_id:
                    self.fac_var.set(self.fac_options[idx])
                    break

    def _on_save(self):
        code = self.entry_code.get().strip().upper()
        name = self.entry_name.get().strip()
        year = self.entry_year.get().strip()
        fac_str = self.fac_var.get()

        if not code or not name or not year or not fac_str:
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ các thông tin bắt buộc.", parent=self)
            return

        faculty_id = None
        for f in self.faculties:
            if fac_str.startswith(f.code + " -"):
                faculty_id = f.id
                break

        self.result = {
            "code": code,
            "name": name,
            "faculty_id": faculty_id,
            "academic_year": year
        }
        self.destroy()

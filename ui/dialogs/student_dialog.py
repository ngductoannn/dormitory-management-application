import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List
from models.student import Student
from models.department import StudentClass
from ui.theme import Theme

class StudentDialog(tk.Toplevel):
    def __init__(self, parent, student: Optional[Student] = None, classes: Optional[List[StudentClass]] = None):
        super().__init__(parent)
        self.student = student
        self.classes = classes or []
        self.result: Optional[Student] = None

        self.title("Sửa thông tin sinh viên" if student else "Thêm sinh viên mới")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(bg=Theme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        if student:
            self._populate_fields(student)

        # Center dialog
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(10, x)}+{max(10, y)}")

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self, bg=Theme.PRIMARY, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_text = "Chỉnh sửa thông tin sinh viên" if self.student else "Thêm mới sinh viên"
        tk.Label(
            header_frame,
            text=title_text,
            font=Theme.FONT_HEADER,
            fg=Theme.TEXT_WHITE,
            bg=Theme.PRIMARY
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # Body container
        body = tk.Frame(self, bg=Theme.SURFACE, padx=24, pady=20)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Form fields
        self.fields = {}

        # Row 1: MSSV & Giới tính
        r1 = tk.Frame(body, bg=Theme.SURFACE)
        r1.pack(fill=tk.X, pady=6)
        
        f_code = tk.Frame(r1, bg=Theme.SURFACE)
        f_code.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(f_code, text="Mã sinh viên (MSSV) *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fields["student_code"] = ttk.Entry(f_code)
        self.fields["student_code"].pack(fill=tk.X)

        f_gender = tk.Frame(r1, bg=Theme.SURFACE, width=140)
        f_gender.pack(side=tk.RIGHT)
        tk.Label(f_gender, text="Giới tính", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.gender_var = tk.StringVar(value="Nam")
        self.fields["gender"] = ttk.Combobox(f_gender, textvariable=self.gender_var, values=["Nam", "Nữ", "Khác"], state="readonly", width=10)
        self.fields["gender"].pack(fill=tk.X)

        # Row 2: Họ và tên
        r2 = tk.Frame(body, bg=Theme.SURFACE)
        r2.pack(fill=tk.X, pady=6)
        tk.Label(r2, text="Họ và tên *", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fields["full_name"] = ttk.Entry(r2)
        self.fields["full_name"].pack(fill=tk.X)

        # Row 3: Ngày sinh & Lớp học
        r3 = tk.Frame(body, bg=Theme.SURFACE)
        r3.pack(fill=tk.X, pady=6)

        f_dob = tk.Frame(r3, bg=Theme.SURFACE)
        f_dob.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(f_dob, text="Ngày sinh (YYYY-MM-DD)", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fields["dob"] = ttk.Entry(f_dob)
        self.fields["dob"].pack(fill=tk.X)
        self.fields["dob"].insert(0, "2004-01-01")

        f_class = tk.Frame(r3, bg=Theme.SURFACE)
        f_class.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        tk.Label(f_class, text="Lớp sinh hoạt", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        
        self.class_options = ["-- Chưa phân lớp --"] + [f"{c.code} - {c.name}" for c in self.classes]
        self.class_var = tk.StringVar(value=self.class_options[0])
        self.fields["class"] = ttk.Combobox(f_class, textvariable=self.class_var, values=self.class_options, state="readonly")
        self.fields["class"].pack(fill=tk.X)

        # Row 4: Email & Số điện thoại
        r4 = tk.Frame(body, bg=Theme.SURFACE)
        r4.pack(fill=tk.X, pady=6)

        f_email = tk.Frame(r4, bg=Theme.SURFACE)
        f_email.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(f_email, text="Email", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fields["email"] = ttk.Entry(f_email)
        self.fields["email"].pack(fill=tk.X)

        f_phone = tk.Frame(r4, bg=Theme.SURFACE)
        f_phone.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        tk.Label(f_phone, text="Số điện thoại", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fields["phone"] = ttk.Entry(f_phone)
        self.fields["phone"].pack(fill=tk.X)

        # Row 5: Địa chỉ
        r5 = tk.Frame(body, bg=Theme.SURFACE)
        r5.pack(fill=tk.X, pady=6)
        tk.Label(r5, text="Địa chỉ / Quê quán", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.fields["address"] = ttk.Entry(r5)
        self.fields["address"].pack(fill=tk.X)

        # Row 6: Trạng thái học tập
        r6 = tk.Frame(body, bg=Theme.SURFACE)
        r6.pack(fill=tk.X, pady=6)
        tk.Label(r6, text="Trạng thái", font=Theme.FONT_SUBTITLE, bg=Theme.SURFACE, fg=Theme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))
        self.status_var = tk.StringVar(value="Đang học")
        self.fields["status"] = ttk.Combobox(
            r6,
            textvariable=self.status_var,
            values=["Đang học", "Bảo lưu", "Đã tốt nghiệp", "Thôi học"],
            state="readonly"
        )
        self.fields["status"].pack(fill=tk.X)

        # Action Buttons
        btn_frame = tk.Frame(self, bg=Theme.BG_MAIN, pady=12)
        btn_frame.pack(fill=tk.X, padx=16)

        btn_save = ttk.Button(btn_frame, text="✓ Lưu thông tin", style="Primary.TButton", command=self._on_save)
        btn_save.pack(side=tk.RIGHT, padx=6)

        btn_cancel = ttk.Button(btn_frame, text="Huỷ bỏ", command=self.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=6)

    def _populate_fields(self, s: Student):
        self.fields["student_code"].delete(0, tk.END)
        self.fields["student_code"].insert(0, s.student_code)

        self.gender_var.set(s.gender or "Nam")

        self.fields["full_name"].delete(0, tk.END)
        self.fields["full_name"].insert(0, s.full_name)

        self.fields["dob"].delete(0, tk.END)
        self.fields["dob"].insert(0, s.dob or "")

        self.fields["email"].delete(0, tk.END)
        self.fields["email"].insert(0, s.email or "")

        self.fields["phone"].delete(0, tk.END)
        self.fields["phone"].insert(0, s.phone or "")

        self.fields["address"].delete(0, tk.END)
        self.fields["address"].insert(0, s.address or "")

        self.status_var.set(s.status or "Đang học")

        if s.class_id:
            for idx, c in enumerate(self.classes, start=1):
                if c.id == s.class_id:
                    self.class_var.set(self.class_options[idx])
                    break

    def _on_save(self):
        code = self.fields["student_code"].get().strip().upper()
        name = self.fields["full_name"].get().strip()
        dob = self.fields["dob"].get().strip()
        gender = self.gender_var.get()
        email = self.fields["email"].get().strip()
        phone = self.fields["phone"].get().strip()
        address = self.fields["address"].get().strip()
        status = self.status_var.get()

        if not code:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã sinh viên (MSSV).", parent=self)
            self.fields["student_code"].focus_set()
            return

        if not name:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Họ và tên sinh viên.", parent=self)
            self.fields["full_name"].focus_set()
            return

        # Get class_id
        selected_class_text = self.class_var.get()
        class_id = None
        for c in self.classes:
            if selected_class_text.startswith(c.code + " -"):
                class_id = c.id
                break

        res_id = self.student.id if self.student else None
        self.result = Student(
            id=res_id,
            student_code=code,
            full_name=name,
            dob=dob,
            gender=gender,
            email=email,
            phone=phone,
            address=address,
            class_id=class_id,
            status=status
        )
        self.destroy()

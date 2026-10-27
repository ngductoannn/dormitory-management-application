import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable
from services.student_service import StudentService
from services.course_service import CourseService
from services.export_service import ExportService
from ui.dialogs.student_dialog import StudentDialog
from ui.theme import Theme
from models.student import Student

class StudentView(tk.Frame):
    def __init__(
        self,
        parent,
        student_service: StudentService,
        course_service: CourseService,
        on_view_grades: Optional[Callable[[int], None]] = None
    ):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.student_service = student_service
        self.course_service = course_service
        self.on_view_grades = on_view_grades

        self.faculties = []
        self.classes = []
        self.students = []

        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        # Top Action Bar
        action_bar = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        action_bar.pack(fill=tk.X)

        title_lbl = tk.Label(action_bar, text="QUẢN LÝ HỒ SƠ SINH VIÊN", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN)
        title_lbl.pack(side=tk.LEFT)

        btn_box = tk.Frame(action_bar, bg=Theme.BG_MAIN)
        btn_box.pack(side=tk.RIGHT)

        btn_add = ttk.Button(btn_box, text="➕ Thêm mới", style="Primary.TButton", command=self._add_student)
        btn_add.pack(side=tk.LEFT, padx=4)

        btn_edit = ttk.Button(btn_box, text="✏️ Chỉnh sửa", command=self._edit_selected)
        btn_edit.pack(side=tk.LEFT, padx=4)

        btn_del = ttk.Button(btn_box, text="🗑️ Xoá", style="Danger.TButton", command=self._delete_selected)
        btn_del.pack(side=tk.LEFT, padx=4)

        btn_grades = ttk.Button(btn_box, text="📊 Xem điểm", command=self._view_grades_selected)
        btn_grades.pack(side=tk.LEFT, padx=4)

        btn_export = ttk.Button(btn_box, text="📤 Xuất CSV", command=self._export_csv)
        btn_export.pack(side=tk.LEFT, padx=4)

        btn_import = ttk.Button(btn_box, text="📥 Nhập CSV", command=self._import_csv)
        btn_import.pack(side=tk.LEFT, padx=4)

        # Filter & Search Panel
        filter_card = tk.Frame(self, bg=Theme.SURFACE, bd=1, relief="solid", padx=16, pady=12)
        filter_card.pack(fill=tk.X, padx=20, pady=(0, 12))

        # Search Entry
        f_search = tk.Frame(filter_card, bg=Theme.SURFACE)
        f_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Label(f_search, text="🔍 Tìm kiếm (MSSV, Họ tên, Email, SĐT):", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.entry_search = ttk.Entry(f_search)
        self.entry_search.pack(fill=tk.X, pady=(2, 0))
        self.entry_search.bind("<Return>", lambda e: self.reload_data())

        # Faculty Filter
        f_fac = tk.Frame(filter_card, bg=Theme.SURFACE, width=170)
        f_fac.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(f_fac, text="Khoa đào tạo:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.faculty_var = tk.StringVar(value="Tất cả khoa")
        self.cb_faculty = ttk.Combobox(f_fac, textvariable=self.faculty_var, state="readonly", width=18)
        self.cb_faculty.pack(pady=(2, 0))
        self.cb_faculty.bind("<<ComboboxSelected>>", lambda e: self._on_faculty_change())

        # Class Filter
        f_cls = tk.Frame(filter_card, bg=Theme.SURFACE, width=150)
        f_cls.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(f_cls, text="Lớp sinh hoạt:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.class_var = tk.StringVar(value="Tất cả lớp")
        self.cb_class = ttk.Combobox(f_cls, textvariable=self.class_var, state="readonly", width=16)
        self.cb_class.pack(pady=(2, 0))
        self.cb_class.bind("<<ComboboxSelected>>", lambda e: self.reload_data())

        # Status Filter
        f_stat = tk.Frame(filter_card, bg=Theme.SURFACE, width=130)
        f_stat.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(f_stat, text="Trạng thái:", font=Theme.FONT_SMALL, bg=Theme.SURFACE, fg=Theme.TEXT_MUTED).pack(anchor="w")
        self.status_var = tk.StringVar(value="Tất cả")
        self.cb_status = ttk.Combobox(
            f_stat,
            textvariable=self.status_var,
            values=["Tất cả", "Đang học", "Bảo lưu", "Đã tốt nghiệp", "Thôi học"],
            state="readonly",
            width=14
        )
        self.cb_status.pack(pady=(2, 0))
        self.cb_status.bind("<<ComboboxSelected>>", lambda e: self.reload_data())

        # Filter Action Buttons
        btn_apply = ttk.Button(filter_card, text="Lọc", command=self.reload_data)
        btn_apply.pack(side=tk.LEFT, pady=(14, 0), padx=(0, 4))

        btn_reset = ttk.Button(filter_card, text="Đặt lại", command=self._reset_filters)
        btn_reset.pack(side=tk.LEFT, pady=(14, 0))

        # Main Table Area
        table_frame = tk.Frame(self, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 8))

        columns = (
            "id", "code", "name", "gender", "dob", "class", "faculty",
            "gpa", "credits", "email", "phone", "status"
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("code", text="MSSV", command=lambda: self._sort_by("student_code"))
        self.tree.heading("name", text="Họ và tên", command=lambda: self._sort_by("full_name"))
        self.tree.heading("gender", text="Giới tính")
        self.tree.heading("dob", text="Ngày sinh")
        self.tree.heading("class", text="Lớp", command=lambda: self._sort_by("class_code"))
        self.tree.heading("faculty", text="Khoa")
        self.tree.heading("gpa", text="GPA (Hệ 4)", command=lambda: self._sort_by("gpa"))
        self.tree.heading("credits", text="Số TC")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Số ĐT")
        self.tree.heading("status", text="Trạng thái")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("code", width=105, anchor="center")
        self.tree.column("name", width=160, anchor="w")
        self.tree.column("gender", width=65, anchor="center")
        self.tree.column("dob", width=95, anchor="center")
        self.tree.column("class", width=95, anchor="center")
        self.tree.column("faculty", width=140, anchor="w")
        self.tree.column("gpa", width=80, anchor="center")
        self.tree.column("credits", width=60, anchor="center")
        self.tree.column("email", width=170, anchor="w")
        self.tree.column("phone", width=105, anchor="center")
        self.tree.column("status", width=105, anchor="center")

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", lambda e: self._edit_selected())

        # Status Footer
        footer_frame = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=4)
        footer_frame.pack(fill=tk.X)

        self.lbl_status = tk.Label(footer_frame, text="Đang tải dữ liệu...", font=Theme.FONT_SMALL, fg=Theme.TEXT_MUTED, bg=Theme.BG_MAIN)
        self.lbl_status.pack(side=tk.LEFT)

        btn_tpl = ttk.Button(footer_frame, text="📄 Tải file mẫu CSV để nhập", command=self._download_template)
        btn_tpl.pack(side=tk.RIGHT)

        self.sort_column = "student_code"
        self.sort_desc = False

    def reload_data(self):
        # Refresh Dropdowns
        self.faculties = self.course_service.get_all_faculties()
        self.classes = self.course_service.get_all_classes()

        fac_options = ["Tất cả khoa"] + [f"{f.code} - {f.name}" for f in self.faculties]
        self.cb_faculty["values"] = fac_options

        self._refresh_class_dropdown()

        # Parse filters
        keyword = self.entry_search.get().strip()
        faculty_id = None
        sel_fac = self.faculty_var.get()
        for f in self.faculties:
            if sel_fac.startswith(f.code + " -"):
                faculty_id = f.id
                break

        class_id = None
        sel_cls = self.class_var.get()
        for c in self.classes:
            if sel_cls.startswith(c.code + " -"):
                class_id = c.id
                break

        status = self.status_var.get()

        self.students = self.student_service.search_students(
            keyword=keyword,
            faculty_id=faculty_id,
            class_id=class_id,
            status=status,
            sort_by=self.sort_column,
            sort_order="DESC" if self.sort_desc else "ASC"
        )

        for row in self.tree.get_children():
            self.tree.delete(row)

        for s in self.students:
            # Color tag for status
            tag = "normal"
            if s.status == "Bảo lưu":
                tag = "warning"
            elif s.status == "Đã tốt nghiệp":
                tag = "success"
            elif s.status == "Thôi học":
                tag = "danger"

            self.tree.insert("", "end", values=(
                s.id,
                s.student_code,
                s.full_name,
                s.gender,
                s.dob or "--",
                s.class_code or "--",
                s.faculty_name or "--",
                f"{s.gpa:.2f}",
                s.total_credits,
                s.email or "--",
                s.phone or "--",
                s.status
            ), tags=(tag,))

        self.tree.tag_configure("normal", foreground=Theme.TEXT_MAIN)
        self.tree.tag_configure("warning", foreground="#B45309")
        self.tree.tag_configure("success", foreground="#047857")
        self.tree.tag_configure("danger", foreground="#B91C1C")

        self.lbl_status.config(text=f"Hiển thị: {len(self.students)} sinh viên. Sắp xếp theo: {self.sort_column} ({'Giảm dần' if self.sort_desc else 'Tăng dần'})")

    def _on_faculty_change(self):
        self._refresh_class_dropdown()
        self.reload_data()

    def _refresh_class_dropdown(self):
        sel_fac = self.faculty_var.get()
        faculty_id = None
        for f in self.faculties:
            if sel_fac.startswith(f.code + " -"):
                faculty_id = f.id
                break

        if faculty_id:
            filtered_classes = [c for c in self.classes if c.faculty_id == faculty_id]
        else:
            filtered_classes = self.classes

        cls_options = ["Tất cả lớp"] + [f"{c.code} - {c.name}" for c in filtered_classes]
        self.cb_class["values"] = cls_options
        if self.class_var.get() not in cls_options:
            self.class_var.set("Tất cả lớp")

    def _reset_filters(self):
        self.entry_search.delete(0, tk.END)
        self.faculty_var.set("Tất cả khoa")
        self.class_var.set("Tất cả lớp")
        self.status_var.set("Tất cả")
        self.reload_data()

    def _sort_by(self, column: str):
        if self.sort_column == column:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_column = column
            self.sort_desc = False
        self.reload_data()

    def _get_selected_student(self) -> Optional[Student]:
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Chưa chọn", "Vui lòng chọn 1 sinh viên trong danh sách.", parent=self)
            return None
        student_id = int(self.tree.item(sel[0], "values")[0])
        return self.student_service.get_student_by_id(student_id)

    def _add_student(self):
        dialog = StudentDialog(self, classes=self.classes)
        self.wait_window(dialog)
        if dialog.result:
            ok, msg = self.student_service.create_student(dialog.result)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _edit_selected(self):
        student = self._get_selected_student()
        if not student:
            return
        dialog = StudentDialog(self, student=student, classes=self.classes)
        self.wait_window(dialog)
        if dialog.result:
            ok, msg = self.student_service.update_student(dialog.result)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_selected(self):
        student = self._get_selected_student()
        if not student:
            return
        ans = messagebox.askyesno(
            "Xác nhận xoá",
            f"Bạn có chắc chắn muốn xoá sinh viên:\n[{student.student_code}] {student.full_name}?\n\n(Dữ liệu điểm của sinh viên này cũng sẽ bị xoá)",
            parent=self
        )
        if ans:
            ok, msg = self.student_service.delete_student(student.id)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _view_grades_selected(self):
        student = self._get_selected_student()
        if student and self.on_view_grades:
            self.on_view_grades(student.id)

    def _export_csv(self):
        if not self.students:
            messagebox.showwarning("Không có dữ liệu", "Không có sinh viên nào để xuất.", parent=self)
            return

        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Lưu danh sách sinh viên ra file CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="danh_sach_sinh_vien.csv"
        )
        if file_path:
            ok, msg = ExportService.export_students_to_csv(file_path, self.students)
            if ok:
                messagebox.showinfo("Xuất thành công", msg, parent=self)
            else:
                messagebox.showerror("Lỗi xuất file", msg, parent=self)

    def _import_csv(self):
        file_path = filedialog.askopenfilename(
            parent=self,
            title="Chọn file CSV chứa danh sách sinh viên",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        class_map = {c.code.upper(): c.id for c in self.classes}
        success_cnt, err_cnt, err_list = ExportService.import_students_from_csv(
            file_path, self.student_service, class_map
        )

        msg = f"Đã nhập thành công: {success_cnt} sinh viên.\nThất bại: {err_cnt} bản ghi."
        if err_list:
            msg += "\n\nChi tiết lỗi:\n" + "\n".join(err_list[:5])
            if len(err_list) > 5:
                msg += f"\n... và {len(err_list) - 5} lỗi khác."

        if err_cnt == 0:
            messagebox.showinfo("Nhập CSV thành công", msg, parent=self)
        else:
            messagebox.showwarning("Nhập CSV hoàn tất có lỗi", msg, parent=self)

        self.reload_data()

    def _download_template(self):
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Lưu file mẫu CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="mau_nhap_sinh_vien.csv"
        )
        if file_path:
            ok, msg = ExportService.generate_student_template_csv(file_path)
            if ok:
                messagebox.showinfo("Thành công", f"File mẫu đã được lưu tại:\n{file_path}", parent=self)
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

import tkinter as tk
from tkinter import ttk, messagebox
from services.course_service import CourseService
from ui.dialogs.course_dialog import CourseDialog, ClassDialog
from ui.theme import Theme

class CourseView(tk.Frame):
    def __init__(self, parent, course_service: CourseService):
        super().__init__(parent, bg=Theme.BG_MAIN)
        self.course_service = course_service

        self.courses = []
        self.classes = []
        self.faculties = []

        self._build_ui()
        self.reload_data()

    def _build_ui(self):
        # Action Bar
        action_bar = tk.Frame(self, bg=Theme.BG_MAIN, padx=20, pady=16)
        action_bar.pack(fill=tk.X)

        tk.Label(action_bar, text="QUẢN LÝ MÔN HỌC, LỚP HỌC & KHOA", font=Theme.FONT_TITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_MAIN).pack(side=tk.LEFT)

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        # Tab 1: Courses
        self.tab_courses = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab_courses, text="📚 Quản lý Môn học")
        self._build_courses_tab()

        # Tab 2: Classes
        self.tab_classes = tk.Frame(self.notebook, bg=Theme.BG_MAIN)
        self.notebook.add(self.tab_classes, text="🏫 Quản lý Lớp học & Khoa")
        self._build_classes_tab()

    def _build_courses_tab(self):
        ctrl_bar = tk.Frame(self.tab_courses, bg=Theme.BG_MAIN, pady=10)
        ctrl_bar.pack(fill=tk.X)

        btn_add = ttk.Button(ctrl_bar, text="➕ Thêm môn học", style="Primary.TButton", command=self._add_course)
        btn_add.pack(side=tk.LEFT, padx=(0, 6))

        btn_edit = ttk.Button(ctrl_bar, text="✏️ Sửa môn", command=self._edit_course)
        btn_edit.pack(side=tk.LEFT, padx=6)

        btn_del = ttk.Button(ctrl_bar, text="🗑️ Xoá môn", style="Danger.TButton", command=self._delete_course)
        btn_del.pack(side=tk.LEFT, padx=6)

        table_frame = tk.Frame(self.tab_courses, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("id", "code", "name", "credits", "faculty", "enrolled", "avg_score")
        self.tree_courses = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_courses.heading("id", text="ID")
        self.tree_courses.heading("code", text="Mã môn")
        self.tree_courses.heading("name", text="Tên môn học")
        self.tree_courses.heading("credits", text="Số tín chỉ")
        self.tree_courses.heading("faculty", text="Khoa phụ trách")
        self.tree_courses.heading("enrolled", text="Lượt học")
        self.tree_courses.heading("avg_score", text="Điểm TB môn")

        self.tree_courses.column("id", width=40, anchor="center")
        self.tree_courses.column("code", width=100, anchor="center")
        self.tree_courses.column("name", width=240, anchor="w")
        self.tree_courses.column("credits", width=80, anchor="center")
        self.tree_courses.column("faculty", width=180, anchor="w")
        self.tree_courses.column("enrolled", width=90, anchor="center")
        self.tree_courses.column("avg_score", width=100, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_courses.yview)
        self.tree_courses.configure(yscrollcommand=vsb.set)

        self.tree_courses.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_courses.bind("<Double-1>", lambda e: self._edit_course())

    def _build_classes_tab(self):
        ctrl_bar = tk.Frame(self.tab_classes, bg=Theme.BG_MAIN, pady=10)
        ctrl_bar.pack(fill=tk.X)

        btn_add = ttk.Button(ctrl_bar, text="➕ Thêm lớp mới", style="Primary.TButton", command=self._add_class)
        btn_add.pack(side=tk.LEFT, padx=(0, 6))

        btn_edit = ttk.Button(ctrl_bar, text="✏️ Sửa lớp", command=self._edit_class)
        btn_edit.pack(side=tk.LEFT, padx=6)

        btn_del = ttk.Button(ctrl_bar, text="🗑️ Xoá lớp", style="Danger.TButton", command=self._delete_class)
        btn_del.pack(side=tk.LEFT, padx=6)

        table_frame = tk.Frame(self.tab_classes, bg=Theme.SURFACE, bd=1, relief="solid")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("id", "code", "name", "faculty", "year", "students")
        self.tree_classes = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_classes.heading("id", text="ID")
        self.tree_classes.heading("code", text="Mã lớp")
        self.tree_classes.heading("name", text="Tên lớp sinh hoạt")
        self.tree_classes.heading("faculty", text="Khoa trực thuộc")
        self.tree_classes.heading("year", text="Niên khoá")
        self.tree_classes.heading("students", text="Sĩ số sinh viên")

        self.tree_classes.column("id", width=40, anchor="center")
        self.tree_classes.column("code", width=110, anchor="center")
        self.tree_classes.column("name", width=220, anchor="w")
        self.tree_classes.column("faculty", width=180, anchor="w")
        self.tree_classes.column("year", width=110, anchor="center")
        self.tree_classes.column("students", width=110, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_classes.yview)
        self.tree_classes.configure(yscrollcommand=vsb.set)

        self.tree_classes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_classes.bind("<Double-1>", lambda e: self._edit_class())

    def reload_data(self):
        self.faculties = self.course_service.get_all_faculties()
        self.courses = self.course_service.get_all_courses()
        self.classes = self.course_service.get_all_classes()

        # Reload Courses Table
        for r in self.tree_courses.get_children():
            self.tree_courses.delete(r)

        for c in self.courses:
            avg_str = f"{c.average_score:.2f}" if c.average_score is not None else "--"
            self.tree_courses.insert("", "end", values=(
                c.id,
                c.code,
                c.name,
                c.credits,
                c.faculty_name or "--",
                c.enrolled_count,
                avg_str
            ))

        # Reload Classes Table
        for r in self.tree_classes.get_children():
            self.tree_classes.delete(r)

        for cl in self.classes:
            self.tree_classes.insert("", "end", values=(
                cl.id,
                cl.code,
                cl.name,
                cl.faculty_name or "--",
                cl.academic_year,
                f"{cl.student_count} SV"
            ))

    def _add_course(self):
        dialog = CourseDialog(self, faculties=self.faculties)
        self.wait_window(dialog)
        if dialog.result:
            r = dialog.result
            ok, msg = self.course_service.create_course(r["code"], r["name"], r["credits"], r["faculty_id"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _edit_course(self):
        sel = self.tree_courses.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 môn học.", parent=self)
            return

        cid = int(self.tree_courses.item(sel[0], "values")[0])
        course = next((c for c in self.courses if c.id == cid), None)
        if not course:
            return

        dialog = CourseDialog(self, faculties=self.faculties, course=course)
        self.wait_window(dialog)
        if dialog.result:
            r = dialog.result
            ok, msg = self.course_service.update_course(cid, r["code"], r["name"], r["credits"], r["faculty_id"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_course(self):
        sel = self.tree_courses.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 môn học cần xoá.", parent=self)
            return

        cid = int(self.tree_courses.item(sel[0], "values")[0])
        cname = self.tree_courses.item(sel[0], "values")[2]
        ans = messagebox.askyesno(
            "Xác nhận xoá môn",
            f"Bạn có chắc muốn xoá môn học: {cname}?\n(Tất cả điểm số liên quan đến môn này sẽ bị xoá)",
            parent=self
        )
        if ans:
            ok, msg = self.course_service.delete_course(cid)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _add_class(self):
        dialog = ClassDialog(self, faculties=self.faculties)
        self.wait_window(dialog)
        if dialog.result:
            r = dialog.result
            ok, msg = self.course_service.create_class(r["code"], r["name"], r["faculty_id"], r["academic_year"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _edit_class(self):
        sel = self.tree_classes.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 lớp học.", parent=self)
            return

        clid = int(self.tree_classes.item(sel[0], "values")[0])
        sclass = next((c for c in self.classes if c.id == clid), None)
        if not sclass:
            return

        dialog = ClassDialog(self, faculties=self.faculties, sclass=sclass)
        self.wait_window(dialog)
        if dialog.result:
            r = dialog.result
            ok, msg = self.course_service.update_class(clid, r["code"], r["name"], r["faculty_id"], r["academic_year"])
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi", msg, parent=self)

    def _delete_class(self):
        sel = self.tree_classes.selection()
        if not sel:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 lớp học.", parent=self)
            return

        clid = int(self.tree_classes.item(sel[0], "values")[0])
        cname = self.tree_classes.item(sel[0], "values")[2]
        ans = messagebox.askyesno(
            "Xác nhận xoá",
            f"Bạn có chắc muốn xoá lớp: {cname}?",
            parent=self
        )
        if ans:
            ok, msg = self.course_service.delete_class(clid)
            if ok:
                messagebox.showinfo("Thành công", msg, parent=self)
                self.reload_data()
            else:
                messagebox.showerror("Lỗi xoá lớp", msg, parent=self)

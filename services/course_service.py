from typing import List, Optional, Tuple
from database.db_manager import DatabaseManager
from database import queries
from models.course import Course
from models.department import Faculty, StudentClass

class CourseService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    # --- COURSES ---
    def get_all_courses(self) -> List[Course]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_COURSES)
            return [Course.from_row(r) for r in cursor.fetchall()]

    def create_course(self, code: str, name: str, credits: int, faculty_id: Optional[int]) -> Tuple[bool, str]:
        code = code.strip().upper()
        name = name.strip()
        if not code or not name:
            return False, "Mã môn học và tên môn học không được để trống."
        if credits <= 0:
            return False, "Số tín chỉ phải lớn hơn 0."

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_COURSE, (code, name, credits, faculty_id))
                conn.commit()
            return True, "Thêm môn học thành công!"
        except Exception as e:
            return False, f"Lỗi thêm môn học: {str(e)}"

    def update_course(self, course_id: int, code: str, name: str, credits: int, faculty_id: Optional[int]) -> Tuple[bool, str]:
        code = code.strip().upper()
        name = name.strip()
        if not code or not name:
            return False, "Mã môn học và tên môn học không được để trống."
        if credits <= 0:
            return False, "Số tín chỉ phải lớn hơn 0."

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_UPDATE_COURSE, (code, name, credits, faculty_id, course_id))
                conn.commit()
            return True, "Cập nhật môn học thành công!"
        except Exception as e:
            return False, f"Lỗi cập nhật môn học: {str(e)}"

    def delete_course(self, course_id: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_COURSE, (course_id,))
                conn.commit()
            return True, "Xoá môn học thành công!"
        except Exception as e:
            return False, f"Lỗi xoá môn học: {str(e)}"

    # --- CLASSES ---
    def get_all_classes(self) -> List[StudentClass]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_CLASSES)
            return [StudentClass.from_row(r) for r in cursor.fetchall()]

    def create_class(self, code: str, name: str, faculty_id: int, academic_year: str) -> Tuple[bool, str]:
        code = code.strip().upper()
        name = name.strip()
        if not code or not name or not academic_year:
            return False, "Mã lớp, tên lớp và khoá học không được để trống."

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_CLASS, (code, name, faculty_id, academic_year.strip()))
                conn.commit()
            return True, "Thêm lớp học thành công!"
        except Exception as e:
            return False, f"Lỗi thêm lớp học: {str(e)}"

    def update_class(self, class_id: int, code: str, name: str, faculty_id: int, academic_year: str) -> Tuple[bool, str]:
        code = code.strip().upper()
        name = name.strip()
        if not code or not name:
            return False, "Mã lớp và tên lớp không được để trống."

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_UPDATE_CLASS, (code, name, faculty_id, academic_year.strip(), class_id))
                conn.commit()
            return True, "Cập nhật lớp học thành công!"
        except Exception as e:
            return False, f"Lỗi cập nhật: {str(e)}"

    def delete_class(self, class_id: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                # Check if students exist
                cursor.execute("SELECT COUNT(*) FROM students WHERE class_id = ?;", (class_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    return False, f"Không thể xoá lớp này vì đang có {count} sinh viên theo học."
                cursor.execute(queries.SQL_DELETE_CLASS, (class_id,))
                conn.commit()
            return True, "Xoá lớp học thành công!"
        except Exception as e:
            return False, f"Lỗi xoá lớp học: {str(e)}"

    # --- FACULTIES ---
    def get_all_faculties(self) -> List[Faculty]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_FACULTIES)
            return [Faculty.from_row(r) for r in cursor.fetchall()]

    def create_faculty(self, code: str, name: str, description: str = "") -> Tuple[bool, str]:
        code = code.strip().upper()
        name = name.strip()
        if not code or not name:
            return False, "Mã khoa và tên khoa không được để trống."

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_FACULTY, (code, name, description.strip()))
                conn.commit()
            return True, "Thêm khoa thành công!"
        except Exception as e:
            return False, f"Lỗi thêm khoa: {str(e)}"

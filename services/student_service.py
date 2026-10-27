import re
from typing import List, Optional, Tuple
from database.db_manager import DatabaseManager
from database import queries
from models.student import Student

class StudentService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    def get_all_students(self) -> List[Student]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_STUDENTS)
            rows = cursor.fetchall()
            return [Student.from_row(row) for row in rows]

    def search_students(
        self,
        keyword: str = "",
        faculty_id: Optional[int] = None,
        class_id: Optional[int] = None,
        status: str = "Tất cả",
        sort_by: str = "student_code",
        sort_order: str = "ASC"
    ) -> List[Student]:
        valid_sort_fields = {
            "student_code": "s.student_code",
            "full_name": "s.full_name",
            "class_code": "c.code",
            "gpa": "gpa",
            "created_at": "s.created_at"
        }
        order_col = valid_sort_fields.get(sort_by, "s.student_code")
        direction = "DESC" if sort_order.upper() == "DESC" else "ASC"

        query = queries.SQL_SEARCH_STUDENTS + f"\nORDER BY {order_col} {direction};"

        search_str = keyword.strip()
        search_like = f"%{search_str}%" if search_str else ""

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, {
                "search": search_str,
                "search_like": search_like,
                "faculty_id": faculty_id,
                "class_id": class_id,
                "status": status
            })
            rows = cursor.fetchall()
            return [Student.from_row(row) for row in rows]

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_STUDENT_BY_ID, (student_id,))
            row = cursor.fetchone()
            return Student.from_row(row) if row else None

    def validate_student(self, student: Student, exclude_id: Optional[int] = None) -> Tuple[bool, str]:
        code = student.student_code.strip()
        if not code:
            return False, "Mã sinh viên (MSSV) không được để trống."
        if len(code) < 3 or len(code) > 20:
            return False, "Mã sinh viên phải từ 3 đến 20 ký tự."

        name = student.full_name.strip()
        if not name:
            return False, "Họ và tên không được để trống."

        if student.email:
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, student.email.strip()):
                return False, "Email không đúng định dạng hợp lệ."

        if student.phone:
            phone_pattern = r"^[0-9+ \-\(\)]{8,15}$"
            if not re.match(phone_pattern, student.phone.strip()):
                return False, "Số điện thoại không hợp lệ (8 - 15 số)."

        # Check unique student code
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_CHECK_STUDENT_CODE_EXISTS, {
                "code": code,
                "exclude_id": exclude_id
            })
            if cursor.fetchone():
                return False, f"Mã sinh viên '{code}' đã tồn tại trong hệ thống."

        return True, ""

    def create_student(self, student: Student) -> Tuple[bool, str]:
        valid, msg = self.validate_student(student, exclude_id=None)
        if not valid:
            return False, msg

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_STUDENT, (
                    student.student_code.strip().upper(),
                    student.full_name.strip(),
                    student.dob.strip() if student.dob else None,
                    student.gender,
                    student.email.strip() if student.email else None,
                    student.phone.strip() if student.phone else None,
                    student.address.strip() if student.address else None,
                    student.class_id,
                    student.status
                ))
                conn.commit()
            return True, "Thêm sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi cơ sở dữ liệu: {str(e)}"

    def update_student(self, student: Student) -> Tuple[bool, str]:
        if not student.id:
            return False, "Không tìm thấy ID sinh viên cần cập nhật."

        valid, msg = self.validate_student(student, exclude_id=student.id)
        if not valid:
            return False, msg

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_UPDATE_STUDENT, (
                    student.student_code.strip().upper(),
                    student.full_name.strip(),
                    student.dob.strip() if student.dob else None,
                    student.gender,
                    student.email.strip() if student.email else None,
                    student.phone.strip() if student.phone else None,
                    student.address.strip() if student.address else None,
                    student.class_id,
                    student.status,
                    student.id
                ))
                conn.commit()
            return True, "Cập nhật sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi cơ sở dữ liệu: {str(e)}"

    def delete_student(self, student_id: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_STUDENT, (student_id,))
                conn.commit()
            return True, "Xoá sinh viên thành công!"
        except Exception as e:
            return False, f"Lỗi cơ sở dữ liệu: {str(e)}"

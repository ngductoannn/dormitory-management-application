from typing import List, Optional, Tuple, Dict, Any
from database.db_manager import DatabaseManager
from database import queries
from models.grade import Grade

class GradeService:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    def get_grades_by_student(self, student_id: int) -> List[Grade]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_GRADES_BY_STUDENT, (student_id,))
            rows = cursor.fetchall()
            return [Grade.from_row(row) for row in rows]

    def get_all_grades(
        self,
        keyword: str = "",
        course_id: Optional[int] = None,
        semester: str = "Tất cả"
    ) -> List[Grade]:
        search_str = keyword.strip()
        search_like = f"%{search_str}%" if search_str else ""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_ALL_GRADES, {
                "search": search_str,
                "search_like": search_like,
                "course_id": course_id,
                "semester": semester
            })
            rows = cursor.fetchall()
            return [Grade.from_row(row) for row in rows]

    def save_grade(
        self,
        student_id: int,
        course_id: int,
        semester: str,
        attendance: float,
        midterm: float,
        final: float
    ) -> Tuple[bool, str]:
        # Validate scores
        for score_name, score in [("chuyên cần", attendance), ("giữa kỳ", midterm), ("cuối kỳ", final)]:
            if score < 0 or score > 10:
                return False, f"Điểm {score_name} phải nằm trong thang điểm từ 0 đến 10."

        if not semester.strip():
            return False, "Vui lòng nhập học kỳ (ví dụ: HK1-2024)."

        total, gpa, letter = Grade.calculate_summary(attendance, midterm, final)

        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_INSERT_OR_REPLACE_GRADE, (
                    student_id,
                    course_id,
                    semester.strip(),
                    round(attendance, 2),
                    round(midterm, 2),
                    round(final, 2),
                    total,
                    gpa,
                    letter
                ))
                conn.commit()
            return True, "Lưu điểm thành công!"
        except Exception as e:
            return False, f"Lỗi lưu điểm: {str(e)}"

    def delete_grade(self, grade_id: int) -> Tuple[bool, str]:
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SQL_DELETE_GRADE, (grade_id,))
                conn.commit()
            return True, "Xoá điểm thành công!"
        except Exception as e:
            return False, f"Lỗi cơ sở dữ liệu: {str(e)}"

    def get_distinct_semesters(self) -> List[str]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT semester FROM grades ORDER BY semester DESC;")
            return [row[0] for row in cursor.fetchall() if row[0]]

    def get_overview_stats(self) -> Dict[str, Any]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_STATISTICS_OVERVIEW)
            row = cursor.fetchone()
            return dict(row) if row else {
                "total_students": 0,
                "total_courses": 0,
                "total_classes": 0,
                "total_faculties": 0,
                "overall_avg_gpa": 0.0
            }

    def get_grade_distribution(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_GRADE_RANKING_DISTRIBUTION)
            return [dict(r) for r in cursor.fetchall()]

    def get_top_students(self, limit: int = 5) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_TOP_STUDENTS, {"limit": limit})
            return [dict(r) for r in cursor.fetchall()]

    def get_faculty_distribution(self) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SQL_GET_STUDENTS_PER_FACULTY)
            return [dict(r) for r in cursor.fetchall()]

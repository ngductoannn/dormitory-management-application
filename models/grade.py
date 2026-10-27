from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class Grade:
    id: Optional[int] = None
    student_id: int = 0
    course_id: int = 0
    semester: str = ""
    attendance_score: Optional[float] = None
    midterm_score: Optional[float] = None
    final_score: Optional[float] = None
    total_score: Optional[float] = None
    gpa_score: Optional[float] = None
    letter_grade: Optional[str] = None
    
    # Extended fields from JOINs
    student_code: Optional[str] = None
    student_name: Optional[str] = None
    class_code: Optional[str] = None
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    credits: int = 0

    @staticmethod
    def calculate_summary(attendance: float, midterm: float, final: float) -> Tuple[float, float, str]:
        """
        Calculates:
        - total_score (scale 10): 10% CC + 30% GK + 60% CK
        - gpa_score (scale 4)
        - letter_grade (A, B+, B, C+, C, D+, D, F)
        """
        total = round(attendance * 0.10 + midterm * 0.30 + final * 0.60, 2)
        
        if total >= 8.5:
            gpa = 4.0
            letter = 'A'
        elif total >= 8.0:
            gpa = 3.5
            letter = 'B+'
        elif total >= 7.0:
            gpa = 3.0
            letter = 'B'
        elif total >= 6.5:
            gpa = 2.5
            letter = 'C+'
        elif total >= 5.5:
            gpa = 2.0
            letter = 'C'
        elif total >= 5.0:
            gpa = 1.5
            letter = 'D+'
        elif total >= 4.0:
            gpa = 1.0
            letter = 'D'
        else:
            gpa = 0.0
            letter = 'F'
            
        return total, gpa, letter

    @staticmethod
    def get_classification(gpa: float) -> str:
        """Academic ranking based on cumulative GPA (scale 4)"""
        if gpa >= 3.6:
            return "Xuất sắc"
        elif gpa >= 3.2:
            return "Giỏi"
        elif gpa >= 2.5:
            return "Khá"
        elif gpa >= 2.0:
            return "Trung bình"
        elif gpa >= 1.0:
            return "Yếu"
        else:
            return "Kém"

    @classmethod
    def from_row(cls, row) -> "Grade":
        d = dict(row)
        return cls(
            id=d.get("id"),
            student_id=d.get("student_id", 0),
            course_id=d.get("course_id", 0),
            semester=d.get("semester", ""),
            attendance_score=d.get("attendance_score"),
            midterm_score=d.get("midterm_score"),
            final_score=d.get("final_score"),
            total_score=d.get("total_score"),
            gpa_score=d.get("gpa_score"),
            letter_grade=d.get("letter_grade"),
            student_code=d.get("student_code"),
            student_name=d.get("student_name"),
            class_code=d.get("class_code"),
            course_code=d.get("course_code"),
            course_name=d.get("course_name"),
            credits=int(d.get("credits", 0) or 0)
        )

from dataclasses import dataclass
from typing import Optional

@dataclass
class Student:
    id: Optional[int] = None
    student_code: str = ""
    full_name: str = ""
    dob: str = ""
    gender: str = "Nam"
    email: str = ""
    phone: str = ""
    address: str = ""
    class_id: Optional[int] = None
    status: str = "Đang học"
    class_code: Optional[str] = None
    faculty_name: Optional[str] = None
    gpa: float = 0.0
    total_credits: int = 0

    @classmethod
    def from_row(cls, row) -> "Student":
        d = dict(row)
        return cls(
            id=d.get("id"),
            student_code=d.get("student_code", ""),
            full_name=d.get("full_name", ""),
            dob=d.get("dob", "") or "",
            gender=d.get("gender", "Nam"),
            email=d.get("email", "") or "",
            phone=d.get("phone", "") or "",
            address=d.get("address", "") or "",
            class_id=d.get("class_id"),
            status=d.get("status", "Đang học"),
            class_code=d.get("class_code"),
            faculty_name=d.get("faculty_name"),
            gpa=float(d.get("gpa", 0.0) or 0.0),
            total_credits=int(d.get("total_credits", 0) or 0)
        )

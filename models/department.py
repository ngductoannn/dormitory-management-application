from dataclasses import dataclass
from typing import Optional

@dataclass
class Faculty:
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    description: str = ""
    class_count: int = 0
    student_count: int = 0

    @classmethod
    def from_row(cls, row) -> "Faculty":
        d = dict(row)
        return cls(
            id=d.get("id"),
            code=d.get("code", ""),
            name=d.get("name", ""),
            description=d.get("description", "") or "",
            class_count=int(d.get("class_count", 0) or 0),
            student_count=int(d.get("student_count", 0) or 0)
        )

@dataclass
class StudentClass:
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    faculty_id: Optional[int] = None
    faculty_name: Optional[str] = None
    academic_year: str = ""
    student_count: int = 0

    @classmethod
    def from_row(cls, row) -> "StudentClass":
        d = dict(row)
        return cls(
            id=d.get("id"),
            code=d.get("code", ""),
            name=d.get("name", ""),
            faculty_id=d.get("faculty_id"),
            faculty_name=d.get("faculty_name"),
            academic_year=d.get("academic_year", ""),
            student_count=int(d.get("student_count", 0) or 0)
        )

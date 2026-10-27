from dataclasses import dataclass
from typing import Optional

@dataclass
class Course:
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    credits: int = 3
    faculty_id: Optional[int] = None
    faculty_name: Optional[str] = None
    enrolled_count: int = 0
    average_score: Optional[float] = None

    @classmethod
    def from_row(cls, row) -> "Course":
        d = dict(row)
        return cls(
            id=d.get("id"),
            code=d.get("code", ""),
            name=d.get("name", ""),
            credits=int(d.get("credits", 3)),
            faculty_id=d.get("faculty_id"),
            faculty_name=d.get("faculty_name"),
            enrolled_count=int(d.get("enrolled_count", 0) or 0),
            average_score=float(d.get("average_score")) if d.get("average_score") is not None else None
        )

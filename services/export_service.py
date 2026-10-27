import csv
from typing import List, Tuple, Dict
from models.student import Student
from models.grade import Grade

class ExportService:
    @staticmethod
    def export_students_to_csv(file_path: str, students: List[Student]) -> Tuple[bool, str]:
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                # Header
                writer.writerow([
                    "Mã sinh viên",
                    "Họ và tên",
                    "Ngày sinh",
                    "Giới tính",
                    "Lớp",
                    "Khoa",
                    "Email",
                    "Số điện thoại",
                    "Địa chỉ",
                    "Điểm GPA (Hệ 4)",
                    "Số tín chỉ",
                    "Trạng thái"
                ])
                for s in students:
                    writer.writerow([
                        s.student_code,
                        s.full_name,
                        s.dob,
                        s.gender,
                        s.class_code or "",
                        s.faculty_name or "",
                        s.email,
                        s.phone,
                        s.address,
                        s.gpa,
                        s.total_credits,
                        s.status
                    ])
            return True, f"Xuất thành công {len(students)} sinh viên ra file: {file_path}"
        except Exception as e:
            return False, f"Lỗi xuất file: {str(e)}"

    @staticmethod
    def export_grades_to_csv(file_path: str, grades: List[Grade]) -> Tuple[bool, str]:
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Mã SV",
                    "Họ tên SV",
                    "Lớp",
                    "Mã môn",
                    "Tên môn học",
                    "Số tín chỉ",
                    "Học kỳ",
                    "Chuyên cần (10%)",
                    "Giữa kỳ (30%)",
                    "Cuối kỳ (60%)",
                    "Điểm tổng kết",
                    "Điểm hệ 4",
                    "Điểm chữ"
                ])
                for g in grades:
                    writer.writerow([
                        g.student_code or "",
                        g.student_name or "",
                        g.class_code or "",
                        g.course_code or "",
                        g.course_name or "",
                        g.credits,
                        g.semester,
                        g.attendance_score if g.attendance_score is not None else "",
                        g.midterm_score if g.midterm_score is not None else "",
                        g.final_score if g.final_score is not None else "",
                        g.total_score if g.total_score is not None else "",
                        g.gpa_score if g.gpa_score is not None else "",
                        g.letter_grade or ""
                    ])
            return True, f"Xuất bảng điểm thành công {len(grades)} bản ghi!"
        except Exception as e:
            return False, f"Lỗi xuất bảng điểm: {str(e)}"

    @staticmethod
    def generate_student_template_csv(file_path: str) -> Tuple[bool, str]:
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Mã sinh viên",
                    "Họ và tên",
                    "Ngày sinh (YYYY-MM-DD)",
                    "Giới tính (Nam/Nữ/Khác)",
                    "Mã lớp",
                    "Email",
                    "Số điện thoại",
                    "Địa chỉ",
                    "Trạng thái"
                ])
                writer.writerow([
                    "B24DCCN999",
                    "Lê Minh Tâm",
                    "2006-05-15",
                    "Nam",
                    "CNTT-K18A",
                    "tam.le@email.edu.vn",
                    "0918112233",
                    "Hà Nội",
                    "Đang học"
                ])
            return True, "Tạo file mẫu thành công!"
        except Exception as e:
            return False, f"Lỗi tạo file mẫu: {str(e)}"

    @staticmethod
    def import_students_from_csv(
        file_path: str,
        student_service,
        class_map_by_code: Dict[str, int]
    ) -> Tuple[int, int, List[str]]:
        success_count = 0
        error_count = 0
        errors = []

        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    return 0, 0, ["File CSV trống!"]

                row_idx = 1
                for row in reader:
                    row_idx += 1
                    if not row or not any(field.strip() for field in row):
                        continue
                    try:
                        code = row[0].strip()
                        name = row[1].strip() if len(row) > 1 else ""
                        dob = row[2].strip() if len(row) > 2 else ""
                        gender = row[3].strip() if len(row) > 3 else "Nam"
                        class_code = row[4].strip() if len(row) > 4 else ""
                        email = row[5].strip() if len(row) > 5 else ""
                        phone = row[6].strip() if len(row) > 6 else ""
                        address = row[7].strip() if len(row) > 7 else ""
                        status = row[8].strip() if len(row) > 8 else "Đang học"

                        class_id = class_map_by_code.get(class_code.upper())

                        student = Student(
                            student_code=code,
                            full_name=name,
                            dob=dob,
                            gender=gender if gender in ["Nam", "Nữ", "Khác"] else "Nam",
                            class_id=class_id,
                            email=email,
                            phone=phone,
                            address=address,
                            status=status if status in ["Đang học", "Bảo lưu", "Đã tốt nghiệp", "Thôi học"] else "Đang học"
                        )
                        ok, msg = student_service.create_student(student)
                        if ok:
                            success_count += 1
                        else:
                            error_count += 1
                            errors.append(f"Dòng {row_idx} ({code}): {msg}")
                    except Exception as ex:
                        error_count += 1
                        errors.append(f"Dòng {row_idx}: {str(ex)}")
        except Exception as e:
            return 0, 0, [f"Lỗi đọc file CSV: {str(e)}"]

        return success_count, error_count, errors

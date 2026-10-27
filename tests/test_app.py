import os
import unittest
import tempfile
from database.db_manager import DatabaseManager
from services.ktx_service import KTXService
from models.ktx_models import SinhVien

class TestKTXApp(unittest.TestCase):
    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        DatabaseManager._instance = None
        self.db = DatabaseManager(self.temp_db_path)
        self.service = KTXService(self.db)

    def tearDown(self):
        os.close(self.temp_db_fd)
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)
        DatabaseManager._instance = None

    def test_schema_and_sample_data(self):
        students = self.service.get_all_sinhvien()
        self.assertEqual(len(students), 33)
        rooms = self.service.get_all_phong()
        self.assertEqual(len(rooms), 9)
        dks = self.service.get_all_dangky_phong()
        self.assertEqual(len(dks), 35)
        hoadons = self.service.get_all_hoadon()
        self.assertEqual(len(hoadons), 31)
        xes = self.service.get_all_xe()
        self.assertEqual(len(xes), 12)

    def test_trigger_max_2_xe(self):
        # SV001 already has XE001 and XE002 (2 vehicles)
        ok, msg = self.service.create_xe("XE999", "29A-99999", "Xe may", "SV001", "2026-09-01", None, 100000)
        self.assertFalse(ok)
        self.assertIn("Moi sinh vien chi duoc phep dang ky toi da 2 xe ve thang", msg)

    def test_project_reports(self):
        r1 = self.service.get_report_1()
        self.assertGreater(len(r1), 0)

        r2 = self.service.get_report_2()
        self.assertGreater(len(r2), 0)

        r3 = self.service.get_report_3()
        self.assertGreater(len(r3), 0)

        r4 = self.service.get_report_4()
        self.assertGreater(len(r4), 0)

if __name__ == "__main__":
    unittest.main()

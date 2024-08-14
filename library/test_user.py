import unittest

from main import User, SessionLocal

class TestUser(unittest.TestCase):

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_add_user(self):
        new_user = User(username="test_user", fullname="Test User")
        self.db.add(new_user)
        self.db.commit()

        user = self.db.query(User).filter_by(username="test_user").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.fullname, "Test User")

        # ลบสมาชิกออกหลังการทดสอบเพื่อไม่ให้ข้อมูลจริงในฐานข้อมูลเสียหาย
        self.db.delete(user)
        self.db.commit()

    def test_delete_user(self):
        # สร้างสมาชิกใหม่ก่อน
        new_user = User(username="test_user", fullname="Test User")
        self.db.add(new_user)
        self.db.commit()

        # ลบสมาชิกออก
        self.db.delete(new_user)
        self.db.commit()

        deleted_user = self.db.query(User).filter_by(username="test_user").first()
        self.assertIsNone(deleted_user)

if __name__ == "__main__":
    unittest.main()

import unittest
from fastapi.testclient import TestClient
from main import app, SessionLocal, Base, engine

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # สร้างตารางในฐานข้อมูล
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        # ลบตารางในฐานข้อมูล
        Base.metadata.drop_all(bind=engine)
        cls.db.close()

    def test_create_borrowlist(self):
        """
        ทดสอบการสร้างรายการยืมหนังสือ
        """
        # สร้างผู้ใช้
        response_user = self.client.post("/users/", params={"username": "test_user", "fullname": "Test User"})
        self.assertEqual(response_user.status_code, 200, msg=response_user.json())
        user_id = response_user.json()["id"]

        # สร้างหนังสือ
        response_book = self.client.post("/books/", params={"title": "Test Book", "firstauthor": "Author", "isbn": "1234567890"})
        self.assertEqual(response_book.status_code, 200, msg=response_book.json())
        book_id = response_book.json()["id"]

        # สร้างรายการยืมหนังสือ
        response_borrow = self.client.post("/borrowlist/", params={"user_id": user_id, "book_id": book_id})
        self.assertEqual(response_borrow.status_code, 200, msg=response_borrow.json())
        borrow_id = response_borrow.json()["id"]
        self.assertIsNotNone(borrow_id)

    def test_get_borrowlist(self):
        """
        ทดสอบการดึงข้อมูลรายการยืมหนังสือของผู้ใช้
        """
        # สร้างผู้ใช้ใหม่
        response_user = self.client.post("/users/", params={"username": "test_user2", "fullname": "Test User 2"})
        self.assertEqual(response_user.status_code, 200, msg=response_user.json())
        user_id = response_user.json()["id"]

        # สร้างหนังสือใหม่
        response_book = self.client.post("/books/", params={"title": "Another Book", "firstauthor": "Another Author", "isbn": "0987654321"})
        self.assertEqual(response_book.status_code, 200, msg=response_book.json())
        book_id = response_book.json()["id"]

        # สร้างรายการยืมหนังสือ
        response_borrow = self.client.post("/borrowlist/", params={"user_id": user_id, "book_id": book_id})
        self.assertEqual(response_borrow.status_code, 200, msg=response_borrow.json())

        # ดึงข้อมูลรายการยืมหนังสือของผู้ใช้
        response_get_borrow = self.client.get(f"/borrowlist/{user_id}")
        self.assertEqual(response_get_borrow.status_code, 200, msg=response_get_borrow.json())

        borrow_list = response_get_borrow.json()
        self.assertGreater(len(borrow_list), 0)
        self.assertEqual(borrow_list[0]["user_id"], user_id)
        self.assertEqual(borrow_list[0]["book_id"], book_id)

if __name__ == "__main__":
    unittest.main()

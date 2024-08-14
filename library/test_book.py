import unittest
from main import Book, SessionLocal

class TestBook(unittest.TestCase):

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_add_book(self):
        new_book = Book(title="Test Book", firstauthor="John Doe", isbn="1234567890")
        self.db.add(new_book)
        self.db.commit()

        book = self.db.query(Book).filter_by(isbn="1234567890").first()
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.firstauthor, "John Doe")
        self.assertEqual(book.isbn, "1234567890")

        # ลบหนังสือออกหลังการทดสอบเพื่อไม่ให้ข้อมูลจริงในฐานข้อมูลเสียหาย
        self.db.delete(book)
        self.db.commit()

    def test_delete_book(self):

        # สร้างหนังสือใหม่ก่อน
        new_book = Book(title="Test Book", firstauthor="John Doe", isbn="1234567890")
        self.db.add(new_book)
        self.db.commit()

        # ลบหนังสือออก
        self.db.delete(new_book)
        self.db.commit()

        deleted_book = self.db.query(Book).filter_by(isbn="1234567890").first()
        self.assertIsNone(deleted_book)

if __name__ == "__main__":
    unittest.main()

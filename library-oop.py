import unittest

class User:
    '''
    Represents a Library User.
    '''
    _next_id = 1  # User ID incrementer

    def __init__(self, name_):
        self._name = name_
        self._user_id = User._next_id
        User._next_id += 1

    def __str__(self):
        return f"USERNAME: {self._name}  ID: {self._user_id}"

class Book:
    '''
    Represents a book in the library.
    '''
    def __init__(self, title_, author_, isbn_):
        self._title = title_
        self._author = author_
        self._isbn = isbn_

    def __str__(self):
        return f"TITLE: {self._title}, AUTHOR {self._author}, ISBN {self._isbn} "


class Library:
    '''
    Represents Library Checkout System.
    '''
    def __init__(self):
        self._library_book_list = []
        self._borrowed_books = {}

    # Add book to library.
    def add_book(self, book_) -> None:
        self._library_book_list.append(book_)
        print(f"The book, {book_._title}, has been added.")

    def does_library_have_book(self, isbn_: str) -> bool:
        for book in self._library_book_list:
            if book._isbn == isbn_:
                print(f"The library has a copy: {book._title}")
                return True
        print(f"The library does not own a book with ISBN: {isbn_}")
        return False

    def is_book_borrowed(self, isbn_: str) -> bool:
        if isbn_ in self._borrowed_books:
            print(f"The book: {isbn_} is currently loaned out.")
            return True
        print(f"The book with ISBN {isbn_} is available to be borrowed.")
        return False

    def isbn_to_book_title(self, isbn_) -> None:
        for book in self._library_book_list:
            if book._isbn == isbn_:
                return book._title

    # Allows a user to borrow a book by ISBN.
    def borrow_book(self, isbn_: str, borrower_: str) -> None:
        # Find whether the book is available at library
        _at_library = self.does_library_have_book(isbn_)  # Does library have?
        _borrowed = self.is_book_borrowed(isbn_)  # Currently borrowed?

        if _at_library and not _borrowed:
            self._borrowed_books[isbn_] = borrower_
        else:
            print("Book currently unavailable.")

    # Allows a user to return a borrowed book by ISBN.
    def return_book(self, isbn_) -> None:
        result =  self.is_book_borrowed(isbn_)
        if result:
            del self._borrowed_books[isbn_]
        else:
            print(f"ISBN: {isbn_} not found!")


    # Lists all books that are currently available in the library.
    def list_available_books(self) -> None:
        print("Here are the books in the library.")
        for book in self._library_book_list:
            print(f"{book._title}")


    # 	Lists all borrowed books. If a user is provided, only list books
    def list_borrowed_books(self) -> None:
        if not self._borrowed_books:
            print(f"There are currently no books borrowed.")
        else:
            print(f"Here are the books out on loan.")
            for isbn, borrower in self._borrowed_books.items():
                _title = self.isbn_to_book_title(isbn)
                print(f"Book with ISBN {isbn} is borrowed by {borrower}")


# UNIT TESTS
class TestUser(unittest.TestCase):
    def setUp(self):
        self.test_user = User("Alice")

    def test_user_creation(self):
        self.assertEqual(self.test_user._name, "Alice")  # Test that _name gets set to "Alice"
        self.assertEqual(self.test_user._user_id, 1)  # Test that the first _user_id is, in fact, 1.

class TestBook(unittest.TestCase):
    def setUp(self):
        self.test_book = Book(title_="The Great Gatsby", author_="F. Scott Fitzgerald", isbn_="1234567890")

    def test_book_creation(self):
        self.assertEqual(self.test_book._title, "The Great Gatsby")
        self.assertEqual(self.test_book._author, "F. Scott Fitzgerald")
        self.assertEqual(self.test_book._isbn, "1234567890")


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        # Create book object to be added by add_book().
        self.book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
        self.book2 = Book("1984", "George Orwell", "0987654321")
        # Add book objects
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        # Borrow books - creating dictionary entries for each
        self.library.borrow_book("1234567890", "Alice")
        self.library.borrow_book("0987654321", "Paul")

    def test_add_book(self):
        self.assertIn(self.book1, self.library._library_book_list)
        self.assertIn(self.book2, self.library._library_book_list)

    def test_does_library_have_book(self):
        self.assertTrue(self.library.does_library_have_book("1234567890"))
        self.assertTrue(self.library.does_library_have_book("0987654321"))
        self.assertFalse(self.library.does_library_have_book("1111111111"))

    def test_is_book_borrowed(self):
        self.assertTrue(self.library.is_book_borrowed("1234567890"))
        self.assertTrue(self.library.is_book_borrowed("0987654321"))

    def test_isbn_to_book_title(self):
        self.assertTrue(self.library.does_library_have_book("1234567890"))
        self.assertTrue(self.library.does_library_have_book("0987654321"))
        self.assertFalse(self.library.does_library_have_book("1111111111"))

    def test_borrow_book(self):
        # Assert that the correct ISBN/NAME attributes were set as expected.
        self.assertEqual(self.library._borrowed_books["1234567890"], "Alice")
        self.assertEqual(self.library._borrowed_books["0987654321"], "Paul")

    def test_return_book(self):
        # Assert the ISBNs have been removed
        self.library.return_book("1234567890")
        self.assertNotIn("1234567890", self.library._borrowed_books)
        self.library.return_book("0987654321")
        self.assertNotIn("0987654321", self.library._borrowed_books)


    def test_list_available_books(self):
        """Tests probably not needed"""


    def test_list_borrowed_books(self):
        """Tests probably not needed"""


if __name__ == '__main__':
    # Run the unit tests
    unittest.main()

# Create some books
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
book2 = Book("1984", "George Orwell", "0987654321")

# Create a library and add books to it
library = Library()
library.add_book(book1)
library.add_book(book2)

# Create a user
user = User("Alice")

# Borrow a book
library.borrow_book("1234567890", user._name)

# List available books
library.list_available_books()

# List borrowed books
library.list_borrowed_books()

# Return a book
library.return_book("1234567890")

# List available books again
library.list_available_books()

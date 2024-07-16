class Book:
    def __init__(self, title: str, author: str):
        self._title = title
        self._author = author


class BooksManager:
    def __init__(self):
        self._books = {}

    def add_book(self, book: Book):
        self._books[book._title] = book


class BooksFacade:
    def __init__(self, booksManager: BooksManager, usersManager: UsersManager):

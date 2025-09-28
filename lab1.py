class Book:
    def __init__(self, id=None, title=None, authors=None, publisher=None, 
                 year=None, page_count=None, price=None, binding_type=None):
        self._id = id
        self._title = title
        self._authors = authors
        self._publisher = publisher
        self._year = year
        self._page_count = page_count
        self._price = price
        self._binding_type = binding_type

    # Альтернативный конструктор
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            id=data_dict.get('id'),
            title=data_dict.get('title'),
            authors=data_dict.get('authors'),
            publisher=data_dict.get('publisher'),
            year=data_dict.get('year'),
            page_count=data_dict.get('page_count'),
            price=data_dict.get('price'),
            binding_type=data_dict.get('binding_type')
        )

    # Геттеры и сеттеры с правильными названиями (setTun, getTun)
    def getId(self):
        return self._id
    
    def setId(self, id):
        self._id = id
        
    def getTitle(self):
        return self._title
    
    def setTitle(self, title):
        self._title = title
        
    def getAuthors(self):
        return self._authors
    
    def setAuthors(self, authors):
        self._authors = authors
        
    def getPublisher(self):
        return self._publisher
    
    def setPublisher(self, publisher):
        self._publisher = publisher
        
    def getYear(self):
        return self._year
    
    def setYear(self, year):
        self._year = year
        
    def getPage_count(self):
        return self._page_count
    
    def setPage_count(self, page_count):
        self._page_count = page_count
        
    def getPrice(self):
        return self._price
    
    def setPrice(self, price):
        self._price = price
        
    def getBinding_type(self):
        return self._binding_type
    
    def setBinding_type(self, binding_type):
        self._binding_type = binding_type

    # Переопределение методов
    def __str__(self):
        return (f"Book(id={self._id}, title='{self._title}', "
                f"authors='{self._authors}', publisher='{self._publisher}', "
                f"year={self._year}, page_count={self._page_count}, "
                f"price={self._price}, binding_type='{self._binding_type}')")
    
    def __hash__(self):
        # Более надежная реализация хэша
        return hash((
            self._id, 
            self._title.lower() if self._title else None,
            tuple(self._authors) if isinstance(self._authors, list) else self._authors,
            self._publisher.lower() if self._publisher else None,
            self._year,
            self._page_count,
            self._price,
            self._binding_type.lower() if self._binding_type else None
        ))
    
    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return (self._id == other._id and 
                self._title == other._title and
                self._authors == other._authors and
                self._publisher == other._publisher and
                self._year == other._year and
                self._page_count == other._page_count and
                self._price == other._price and
                self._binding_type == other._binding_type)


class BookManager:
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def get_books_by_author(self, author):
        return [book for book in self.books if author in book.getAuthors()]
    
    def get_books_by_publisher(self, publisher):
        return [book for book in self.books if book.getPublisher() == publisher]
    
    def get_books_after_year(self, year):
        return [book for book in self.books if book.getYear() > year]
    
    # Дополнительный метод для демонстрации работы с хэшами
    def find_duplicates(self):
        seen = {}
        duplicates = []
        for book in self.books:
            book_hash = hash(book)
            if book_hash in seen:
                duplicates.append((seen[book_hash], book))
            else:
                seen[book_hash] = book
        return duplicates


# Создание массива объектов с использованием разных конструкторов
def create_books():
    manager = BookManager()
    
    # Добавление книг через основной конструктор
    manager.add_book(Book(1, "Python Basics", "John Doe", "TechPub", 2020, 300, 29.99, "Paperback"))
    manager.add_book(Book(2, "Advanced Python", "Jane Smith", "CodeBooks", 2021, 450, 49.99, "Hardcover"))
    
    # Добавление через альтернативный конструктор
    book_data = {
        'id': 3,
        'title': "Data Science with Python",
        'authors': "John Doe",
        'publisher': "DataPress",
        'year': 2019,
        'page_count': 500,
        'price': 39.99,
        'binding_type': "Paperback"
    }
    manager.add_book(Book.from_dict(book_data))
    
    manager.add_book(Book(4, "Web Development with Python", "Alice Johnson", "TechPub", 2022, 350, 44.99, "Hardcover"))
    manager.add_book(Book(5, "Machine Learning", "Jane Smith", "AIPress", 2020, 600, 59.99, "Hardcover"))
    
    return manager


# Основная программа
if __name__ == "__main__":
    manager = create_books()
    
    print("Все книги:")
    for book in manager.books:
        print(book)
    
    # a) Список книг заданного автора
    author = "John Doe"
    print(f"\nКниги автора {author}:")
    for book in manager.get_books_by_author(author):
        print(book)
    
    # b) Список книг заданного издательства
    publisher = "TechPub"
    print(f"\nКниги издательства {publisher}:")
    for book in manager.get_books_by_publisher(publisher):
        print(book)
    
    # c) Список книг, выпущенных после заданного года
    year = 2020
    print(f"\nКниги, выпущенные после {year} года:")
    for book in manager.get_books_after_year(year):
        print(book)
    
    # Демонстрация работы хэшей
    print(f"\nХэши книг:")
    for i, book in enumerate(manager.books, 1):
        print(f"Книга {i}: {hash(book)}")
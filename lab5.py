from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Library API", version="1.0.0")

# Модель данных для книги
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    is_available: bool = True

# Временная "база данных" - список книг
books_db = [
    Book(id=1, title="Преступление и наказание", author="Федор Достоевский", year=1866, is_available=True),
    Book(id=2, title="Война и мир", author="Лев Толстой", year=1869, is_available=False),
    Book(id=3, title="Мастер и Маргарита", author="Михаил Булгаков", year=1967, is_available=True),
]

# GET - Получить все книги
@app.get("/books", response_model=List[Book])
async def get_all_books():
    """Получить список всех книг"""
    return books_db

# GET - Получить книгу по ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Получить книгу по её ID"""
    book = next((book for book in books_db if book.id == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

# POST - Добавить новую книгу
@app.post("/books", response_model=Book)
async def create_book(book: Book):
    """Добавить новую книгу в библиотеку"""
    # Проверяем, существует ли книга с таким ID
    existing_book = next((b for b in books_db if b.id == book.id), None)
    if existing_book:
        raise HTTPException(status_code=400, detail="Книга с таким ID уже существует")
    
    books_db.append(book)
    return book

# PUT - Обновить информацию о книге
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    """Обновить информацию о книге"""
    if updated_book.id != book_id:
        raise HTTPException(status_code=400, detail="ID в пути и в теле запроса не совпадают")
    
    book_index = next((index for index, book in enumerate(books_db) if book.id == book_id), None)
    if book_index is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    books_db[book_index] = updated_book
    return updated_book

# DELETE - Удалить книгу
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    """Удалить книгу из библиотеки"""
    book_index = next((index for index, book in enumerate(books_db) if book.id == book_id), None)
    if book_index is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    deleted_book = books_db.pop(book_index)
    return {"message": f"Книга '{deleted_book.title}' удалена", "deleted_book": deleted_book}

# GET - Поиск книг по автору
@app.get("/books/search/{author}")
async def search_books_by_author(author: str):
    """Поиск книг по автору"""
    found_books = [book for book in books_db if author.lower() in book.author.lower()]
    if not found_books:
        raise HTTPException(status_code=404, detail="Книги данного автора не найдены")
    return found_books

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
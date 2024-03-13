from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI(description='Books CRUD by Breno', summary='My first CRUD done with FastAPI.')


class Book:
    id: int
    title:str
    author: str
    description: str
    rating: float
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=150)
    rating: float = Field(gt=-1,lt=11)
    published_year: int = Field(gt=1900, lt=2024, description="The book's published Year")

    class Config:
        json_schema_extra = {
            'example': {
                'title' : 'Book name',
                'author': 'Author name',
                'description': 'The book description',
                'rating': 7.0,
                'published_year': '2012'
            }
        }


Books = [
    Book(1, "Atomic Habits", 'James Clear', 'A very nice book! Mind changer when we talk about productivity.', 9.5, 2018),
    Book(2, "The Way of the Superior Man", 'David Deida', 'Mindset with work, women, duties and purpose', 8.7, 1997),
    Book(3, "The Little Book of Stoicism", 'Jonas Salzgeber', 'An awesome introduction to the Stoic Philosophy!', 9.2, 2019),
    Book(4, "The Art of Living", 'Epictetus', 'Nice mindset builder and life guider.', 9.0, 2023),
    Book(5, "Golden Rules", 'Napoleon Hill', 'The 12 rules for a good life by the genius from his era!', 9.0, 1920),
    Book(6, "The Daily Stoic", 'Ryan Holiday', '366 meditations on wisdom by the GOAT Ryan Holiday.', 9.5, 2016)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return Books


@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Book not found')
              

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: float = Query(gt=-1, lt=11)):
    books_to_return = []
    for book in Books:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return
    

@app.get("/books/{published_year}", status_code=status.HTTP_200_OK)
async def get_by_date(published_year: int = Path(gt=1900, lt=2024)):
    books_to_return = []
    for book in Books:
        if book.published_year == published_year:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))
    raise HTTPException(status_code=201, detail='Book created succefully!')


def find_book_id(book: Book):
    if len(Books) > 0:
        book.id = Books[-1].id + 1
    else:
        book.id = 1
    return book

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
            book_changed = True
            raise HTTPException(status_code=200, detail='Book updated succefully!')
    if not book_changed:
        raise HTTPException(status_code=404, detail='Book not found.')

@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_deleted = True
            raise HTTPException(status_code=200, detail='Book deleted succefully!')
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Book not found.')



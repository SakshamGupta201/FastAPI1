from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="Id is not Needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "null",
                "title": "Crime and Punishment",
                "author": "Fyodor Dostoevsky",
                "description": "A psychological novel following the moral dilemmas of Rodion Raskolnikov, a former student who commits a heinous crime.",
                "rating": 4,
            }
        }


BOOKS = [
    Book(
        1,
        "To Kill a Mockingbird",
        "Harper Lee",
        "A story set in the American South during the 1930s, revolving around the trial of a black man accused of raping a white woman.",
        5,
    ),
    Book(
        2,
        "1984",
        "George Orwell",
        "A dystopian novel set in a totalitarian regime, where the government monitors and controls every aspect of life.",
        4,
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "A tale of love, greed, and the American Dream, set in the Roaring Twenties.",
        4,
    ),
    Book(
        4,
        "Pride and Prejudice",
        "Jane Austen",
        "A romantic novel set in early 19th-century England, revolving around the lives of the Bennett sisters.",
        5,
    ),
    Book(
        5,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "A coming-of-age novel narrated by Holden Caulfield, a teenager navigating the challenges of adolescence.",
        4,
    ),
    Book(
        6,
        "Harry Potter and the Philosopher's Stone",
        "J.K. Rowling",
        "The first book in the Harry Potter series, following the journey of a young wizard, Harry Potter.",
        5,
    ),
    Book(
        7,
        "To the Lighthouse",
        "Virginia Woolf",
        "A novel that explores themes of family, loss, and the passage of time, set in the Hebrides.",
        4,
    ),
    Book(
        8,
        "Moby-Dick",
        "Herman Melville",
        "A tale of obsession and revenge, centered around the hunt for the elusive white whale, Moby Dick.",
        3,
    ),
    Book(
        9,
        "The Lord of the Rings",
        "J.R.R. Tolkien",
        "An epic fantasy trilogy following the quest to destroy the One Ring and defeat the dark lord Sauron.",
        5,
    ),
    Book(
        10,
        "The Hobbit",
        "J.R.R. Tolkien",
        "A fantasy adventure novel chronicling the journey of Bilbo Baggins, a hobbit who seeks treasure guarded by a dragon.",
        4,
    ),
]


# ? GET Requests


@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    book_found = [book for book in BOOKS if book.id == book_id]
    if book_found:
        return book_found
    else:
        return HTTPException(status_code=400, detail="Book not Found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(ge=0, le=5)):
    if rating:
        books_found = [book for book in BOOKS if book.rating == rating]
        if books_found:
            return books_found
        return HTTPException(status_code=400, detail="No Books with the rating")


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
def create_book(book_request: BookRequest):
    book_request = find_book_id(book_request)
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):

    for index, existing_book in enumerate(BOOKS):
        if existing_book.id == book.id:
            BOOKS[index] = Book(**book.model_dump())
            return {"message": "Book updated Successfully"}
    raise HTTPException(status_code=404, detail="Book not Found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            return {"message": "Book deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not Found")

import uvicorn
from fastapi import Body, FastAPI, HTTPException, Response

app = FastAPI()

BOOKS = [
    {"title": "Title 1", "author": "Author 1", "category": "Science"},
    {"title": "Title 2", "author": "Author 2", "category": "Fiction"},
    {"title": "Title 3", "author": "Author 3", "category": "History"},
    {"title": "Title 4", "author": "Author 4", "category": "Science Fiction"},
    {"title": "Title 5", "author": "Author 5", "category": "Mystery"},
    {"title": "Title 6", "author": "Author 6", "category": "Fantasy"},
    {"title": "Title 7", "author": "Author 7", "category": "Biography"},
    {"title": "Title 8", "author": "Author 8", "category": "Thriller"},
    {"title": "Title 9", "author": "Author 9", "category": "Romance"},
    {"title": "Title 10", "author": "Author 10", "category": "Adventure"},
    {"title": "Title 11", "author": "Author 11", "category": "Self-Help"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/")
async def read_books(category: str = None, author: str = None):
    if category:
        filtered_books = [book for book in BOOKS if book.get("category") == category]
        if not filtered_books:
            raise HTTPException(
                status_code=404, detail=f"No books found for the category '{category}'"
            )
        return filtered_books

    if author:
        filtered_books = [book for book in BOOKS if book.get("author") == author]
        if not filtered_books:
            raise HTTPException(
                status_code=404, detail=f"No books found for the author '{author}'"
            )
        return filtered_books

    raise HTTPException(
        status_code=400, detail="Please provide a category or an author"
    )


@app.get("/books/{author}/")
async def read_author_category_by_query(book_author: str, category: str):
    filtered_books = []

    filtered_books = [
        book
        for book in BOOKS
        if book.get("category").casefold() == category.casefold()
        and book.get("author").casefold() == book_author.casefold()
    ]

    if filtered_books:
        return filtered_books
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@app.get("/books/{book_title}")
async def read_book(book_title: int):
    found_book = next((book for book in BOOKS if book_title in book.values()), None)
    return found_book if found_book else "Book Not Found"


# ? POSTS Requests


# * EndPoint to create Book
@app.post("/books/create_book")
async def create_book(body=Body()):
    BOOKS.append(body)
    return Response(content="Content Added", status_code=200)


# ? PUT Requests


# * Endpoint to Update Book
@app.put("/books/update_book")
async def update_book(body=Body()):
    for i in range(len(BOOKS)):
        if str(body.get("title").casefold()) == str(BOOKS[i].get("title")).casefold():
            BOOKS[i] = body
            return Response(content="Updated Book", status_code=200)
    else:
        return HTTPException(status_code=404, detail="Not Found")


@app.delete("/books/delete/{title}")
async def delete_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == title.casefold():
            BOOKS.pop(i)
            return Response(content="Deleted Successfully", status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Not Found")


# ? GET Requests


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

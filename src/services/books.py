from fastapi import UploadFile
from sqlalchemy.orm import selectinload

from src.exceptions import (
    AuthorNotFoundException,
    BookNotFoundException,
    OnlyAdminOrAuthorException,
    AuthorCanOnlyAddOwnBooksException,
    CanEditOnlyOwnBooksException,
)
from src.models import UsersOrm, BooksOrm
from src.schemas.books import BookCreate, BookUpdate, BookFilterParams
from src.services.base import BaseService
from src.services.files import delete_file, save_cover, save_book_file


class BooksService(BaseService):
    async def get_books(self, filters: BookFilterParams):
        return await self.db.books.get_filtered(filters)

    async def get_book(self, book_id: int):
        return await self.db.books.get_one_or_none(id=book_id)

    async def create_book(self, payload: BookCreate, current_user: UsersOrm):
        if current_user.role.name not in ("ADMIN", "AUTHOR"):
            raise OnlyAdminOrAuthorException

        author = await self.db.authors.get_one_orm(id=payload.author_id)
        if author is None:
            raise AuthorNotFoundException
        if current_user.role.name == "AUTHOR" and author.user_id != current_user.id:
            raise AuthorCanOnlyAddOwnBooksException

        book = await self.db.books.add(payload)
        await self.db.commit()
        return book

    def _assert_can_manage_book(self, book: BooksOrm, current_user: UsersOrm) -> None:
        if current_user.role.name == "ADMIN":
            return
        if book.author.user_id != current_user.id:
            raise CanEditOnlyOwnBooksException

    async def update_book(self, book_id: int, payload: BookUpdate, current_user: UsersOrm):
        book = await self.db.books.get_one_orm(
            selectinload(BooksOrm.author),
            id=book_id
        )
        if book is None:
            raise BookNotFoundException
        self._assert_can_manage_book(book, current_user)
        await self.db.books.edit(data=payload, exclude_unset=True, id=book_id)
        await self.db.commit()

    async def delete_book(self, book_id: int, current_user: UsersOrm):
        book = await self.db.books.get_one_orm(
            selectinload(BooksOrm.author),
            id=book_id
        )
        if book is None:
            raise BookNotFoundException
        self._assert_can_manage_book(book, current_user)
        await self.db.books.delete(id=book_id)
        await self.db.commit()

    async def upload_cover(self, book_id: int, file: UploadFile, current_user: UsersOrm):
        book = await self.db.books.get_one_orm(
            selectinload(BooksOrm.author),
            id=book_id
        )
        if book is None:
            raise BookNotFoundException
        self._assert_can_manage_book(book, current_user)

        delete_file(book.cover_path)
        new_path = save_cover(file)
        await self.db.books.set_cover_path(book_id, new_path)
        await self.db.commit()
        return await self.get_book(book_id)

    async def upload_file(self, book_id: int, file: UploadFile, current_user: UsersOrm):
        book = await self.db.books.get_one_orm(
            selectinload(BooksOrm.author),
            id=book_id
        )
        if book is None:
            raise BookNotFoundException
        self._assert_can_manage_book(book, current_user)

        delete_file(book.file_path)
        new_path = save_book_file(file)
        await self.db.books.set_file_path(book_id, new_path)
        await self.db.commit()
        return await self.get_book(book_id)

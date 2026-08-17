from src.models import UsersOrm, BooksOrm, ReviewsOrm, FavoritesOrm, RolesOrm
from src.models.authors import AuthorsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.authors import Author
from src.schemas.books import Book
from src.schemas.favorites import Favorite
from src.schemas.reviews import Review
from src.schemas.roles import Role
from src.schemas.users import User

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class AuthorDataMapper(DataMapper):
    db_model = AuthorsOrm
    schema = Author

class BookDataMapper(DataMapper):
    db_model = BooksOrm
    schema = Book

class ReviewDataMapper(DataMapper):
    db_model = ReviewsOrm
    schema = Review

class FavoriteDataMapper(DataMapper):
    db_model = FavoritesOrm
    schema = Favorite

class RoleDataMapper(DataMapper):
    db_model = RolesOrm
    schema = Role
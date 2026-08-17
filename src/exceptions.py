from fastapi import HTTPException


class LibraryException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(LibraryException):
    detail = "Object not found"


class ObjectAlreadyExistsException(LibraryException):
    detail = "A similar object already exists"


class UserNotFoundException(LibraryException):
    detail = "User not found"


class AuthorNotFoundException(LibraryException):
    detail = "Author is not found"


class BookNotFoundException(LibraryException):
    detail = "Book does not exist"


class ReviewNotFoundException(LibraryException):
    detail = "Review not found"


class FavoriteNotFoundException(LibraryException):
    detail = "The book is not favorites"


class EmailAlreadyExistsException(LibraryException):
    detail = "The email is already registered"


class UsernameAlreadyExistsException(LibraryException):
    detail = "The username is taken"


class IncorrectCredentialsException(LibraryException):
    detail = "Incorrect email or password"


class UserInactiveException(LibraryException):
    detail = "Inactive user"


class UserBlockedException(LibraryException):
    detail = "Account is blocked"


class IncorrectTokenException(LibraryException):
    detail = "Invalid or expired token"


class InsufficientPermissionsException(LibraryException):
    detail = "Insufficient permissions to perform the operation"


class OnlyAdminOrAuthorException(LibraryException):
    detail = "Only admin and author are allowed"


class AuthorCanOnlyAddOwnBooksException(LibraryException):
    detail = "The author can only add books under their own name"


class CanEditOnlyOwnBooksException(LibraryException):
    detail = "You can edit only your books"


class ReviewAlreadyExistsException(LibraryException):
    detail = "You have already left a review for this book"


class CanEditOnlyOwnReviewException(LibraryException):
    detail = "You can only edit your own review"


class CanDeleteOnlyOwnReviewException(LibraryException):
    detail = "You don't have enough rights to delete the review"


class LibraryHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "User not found"


class AuthorNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Author is not found"


class BookNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Book does not exist"


class ReviewNotFoundHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "Review not found"


class FavoriteNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "The book is not favorites"


class EmailAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "The email is already registered"


class UsernameAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "The username is taken"


class IncorrectCredentialsHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Incorrect email or password"


class UserInactiveHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Inactive user"


class UserBlockedHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "Account is blocked"


class IncorrectTokenHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Invalid or expired token"


class NoAccessTokenHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "You are not logged in"


class InsufficientPermissionsHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "Insufficient permissions to perform the operation"


class OnlyAdminOrAuthorHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "Only admin and author are allowed"


class AuthorCanOnlyAddOwnBooksHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "The author can only add books under their own name"


class CanEditOnlyOwnBooksHTTPException(LibraryHTTPException):
    status_code = 403
    detail = "You can edit only your books"


class ReviewAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "You have already left a review for this book"


class CanEditOnlyOwnReviewHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "You can only edit your own review"


class CanDeleteOnlyOwnReviewHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "You don't have enough rights to delete the review"

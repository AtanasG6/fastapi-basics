from enum import IntEnum

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

users = {
    1: {"name": "Alice", "age": 30},
    2: {"name": "Bob", "age": 25},
    3: {"name": "Charlie", "age": 35},
}

class ErrorType(IntEnum):
    USER_NOT_FOUND = 1
    VALIDATION_ERROR = 2
    DUPLICATE_USER = 3,
    EROR = 4

class AppException(Exception):
    error_type: ErrorType
    def __init__(self, msg: str):
        self.msg = msg

class UserNotFoundException(AppException):
    error_type = ErrorType.USER_NOT_FOUND

class ValidationException(AppException):
    error_type = ErrorType.VALIDATION_ERROR

class DuplicateUserException(AppException):
    error_type = ErrorType.DUPLICATE_USER

MAP_ERRORS = {
    ErrorType.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorType.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
    ErrorType.DUPLICATE_USER: status.HTTP_409_CONFLICT,
    ErrorType.EROR: status.HTTP_400_BAD_REQUEST
}

@app.get("/")
def get_users() -> dict:
    return users

@app.get("/{id}")
def get_user(id: int) -> dict:
    user = users.get(id)

    # If the user with the given id is not found, raise an HTTPException with a 404 status code and a custom error message.
    if user is None:
        # raise HTTPException(
            # status_code=status.HTTP_404_NOT_FOUND,
            # detail=f"User with id {id} not found."
        # )
        raise UserNotFoundException(f"User with id {id} not found.")
    return user

# If app throws a UserNotFoundException, this handler will catch it and return a JSON response with a 404 status code and the error message.
@app.exception_handler(AppException)
def handle_app_exception(request: Request, exc: AppException):
    print("App exception occurred", exc)
    status_code = status.HTTP_400_BAD_REQUEST
    #if isinstance(exc, UserNotFoundException):
        #status_code = status.HTTP_404_NOT_FOUND
    #elif isinstance(exc, ValidationException):
        #status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    #elif isinstance(exc, DuplicateUserException):
        #status_code = status.HTTP_409_CONFLICT

    #if exc.error_type == ErrorType.USER_NOT_FOUND:
        #status_code = status.HTTP_404_NOT_FOUND
    #elif exc.error_type == ErrorType.VALIDATION_ERROR:
        #status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    #elif exc.error_type == ErrorType.DUPLICATE_USER:
        #status_code = status.HTTP_409_CONFLICT
    #else:
        #status_code = status.HTTP_400_BAD_REQUEST

    status_code = map_app_error_to_http_status.get(exc.error_type, status.HTTP_400_BAD_REQUEST)

    return JSONResponse(
        status_code=status_code,
        content={"error_message": exc.msg},
    )


    #return HTMLResponse(
       # status_code=status.HTTP_404_NOT_FOUND,
       # content=f"<html><body><h1>Error: {exc.msg}</h1></body></html>",
    #)

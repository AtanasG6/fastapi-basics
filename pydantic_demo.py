from pydantic import BaseModel, Field, field_validator
from enum import StrEnum

class BookGenre(StrEnum):
    SCIFI = "scifi"
    CRIME = "crime"
    ROMANCE = "romance"
    COMEDY = "comedy",
    NOVEL = "novel"
    OTHER = "other"

# Custom exception for field validation errors
class FieldValidationError(Exception):
    pass

class Book(BaseModel):
    author: str
    title: str
    description: str | None = None # Optional field, can be None
    genre: BookGenre
    published_year: int = Field(gt=1900, lt=2026, description="The year the book was published. Must be between 1900 and 2025.")

    # Custom validator for the 'author' field
    @field_validator('author')
    @classmethod #Static method decorator
    def validate_author_name(cls, author: str) -> str:
        for ch in author:
            if ch.isdigit():
                raise FieldValidationError("Author name cannot contain numbers.")
        return author.upper() # Validators can also modify the value of the field.

# __annotations__ is a special attribute in Python 
# that stores the type hints for the attributes of a class. 
# In this case, it will show the type hints for the attributes of the Book class.
print(Book.__annotations__)

the_great_gatsby = Book(
    author="F. Scott Fitzgerald",
    title="The Great Gatsby",
    #description="A novel set in the Jazz Age that tells the story of Jay Gatsby and his unrequited love for Daisy Buchanan.",
    genre=BookGenre.ROMANCE,
    published_year=1925
)

print(the_great_gatsby)

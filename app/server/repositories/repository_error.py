from typing import Optional, TypeVar

from pydantic import BaseModel
from typing_extensions import Generic

T = TypeVar("T")

class RepositoryError(BaseModel):
    message: str

class Result(Generic[T]):
    def __init__(self, value: Optional[T] = None, error: Optional[RepositoryError] = None):
        self.value = value
        self.error = error
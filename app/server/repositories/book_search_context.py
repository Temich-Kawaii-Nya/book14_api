from abc import ABC, abstractmethod

from typing import Optional

import requests
from pydantic import BaseModel

from app.server.models.book import Book


class SearchBookModel(BaseModel):
    isnb: Optional[str]
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]

class IBookSearchContext(ABC):
    @abstractmethod
    async def find_book(self, book: SearchBookModel) -> Book:
        pass
class IGoogleBooksContext(IBookSearchContext, ABC):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "isbn:9785046665239",
        "key": "AIzaSyAS9kGTFFZ0lYP9TzMIOxUOWhBUJR97Xx0"
    }
    async def find_book(self, isnb: str):
        try:
            params = {
                "q": f"isbn:{isnb}",
                "key": "AIzaSyAS9kGTFFZ0lYP9TzMIOxUOWhBUJR97Xx0"
            }
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise {"error": f"HTTP error occurred: {response.status_code}"}
        except requests.RequestException as e:
            raise {"error": f"Request error occurred: {str(e)}"}
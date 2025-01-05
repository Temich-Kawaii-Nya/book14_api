import logging
from abc import ABC, abstractmethod
from typing import Optional

import requests
from pydantic import BaseModel

from ..models.book import Book
from ..utils.json_book_encoder import GoogleBookJsonEncoder, IBookJsonEncoder

book_encoder: IBookJsonEncoder = GoogleBookJsonEncoder()

class SearchBookModel(BaseModel):
    isnb: Optional[str] = ""
    title: Optional[str] = ""
    author: Optional[str] = ""
    publisher: Optional[str] = ""
class IBookSearchContext(ABC):
    @abstractmethod
    async def find_book(self, book: SearchBookModel) -> Book:
        pass


def build_query(search_model: SearchBookModel) -> str:
    """
        Формируем строку поиска на основе значений модели.
    """
    query_parts = []
    if search_model.isnb:
        query_parts.append(f"isbn:{search_model.isnb}")
    if search_model.title:
        query_parts.append(f"intitle:{search_model.title}")
    if search_model.author:
        query_parts.append(f"inauthor:{search_model.author}")
    if search_model.publisher:
        query_parts.append(f"inpublisher:{search_model.publisher}")
    return " ".join(query_parts)


class IGoogleBooksContext(IBookSearchContext, ABC):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": "isbn:9785046665239",
        "key": "AIzaSyAS9kGTFFZ0lYP9TzMIOxUOWhBUJR97Xx0"
    }
    async def find_book(self, queryModel: SearchBookModel):
        try:
            query = build_query(queryModel)
            params = {
                "q": query,
                "key": "AIzaSyAS9kGTFFZ0lYP9TzMIOxUOWhBUJR97Xx0"
            }
            response = requests.get(self.url, params=params, timeout=10)
            logging.info(response.request.url + " " + response.request.path_url + " ")
            response.raise_for_status()
            book = book_encoder.convert_from_json_to_book(response.json())
            return book
        except requests.HTTPError as e:
            raise {"error": f"HTTP error occurred: {response.status_code}"}
        except requests.RequestException as e:
            raise {"error": f"Request error occurred: {str(e)}"}
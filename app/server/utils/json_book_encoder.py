import datetime
from abc import ABC, abstractmethod

from ..models.book import Book
from ..models.description import Description


class IBookJsonEncoder(ABC):
    @abstractmethod
    def convert_from_json_to_book(self, json: str) -> [Book]:
        pass

class GoogleBookJsonEncoder(IBookJsonEncoder, ABC):
    def convert_from_json_to_book(self, json: dict) -> list[Book]:
        books = []
        for item in json.get("items", []):
            volume_info = item.get("volumeInfo", {})
            industry_identifiers = volume_info.get("industryIdentifiers", [])
            isnb = None
            for identifier in industry_identifiers:
                if identifier.get("type") == "ISBN_13":
                    isnb = identifier.get("identifier")
                    break
            if not isnb and industry_identifiers:
                isnb = industry_identifiers[0].get("identifier")

            authors = volume_info.get("authors", ["Unknown Author"])
            description_text = volume_info.get("description", "No description available.")
            publisher = volume_info.get("publisher", "Unknown Publisher")
            cover_url = volume_info.get("imageLinks", {}).get("thumbnail", "No cover available.")

            desc = Description(
                title=volume_info.get("title", ""),
                description=description_text,
                author_name=", ".join(authors),
                publisher_name=publisher,
                publishing_date=volume_info.get("publishedDate", datetime.date),
                cover_url=cover_url,
                page_number=volume_info.get("pageCount", 0),
            )
            book = Book(
                isnb=isnb,
                description=desc,
            )
            books.append(book)
        return books


"""
Design Amazon comments filtering system.
"""
from abc import ABC, abstractmethod
from typing import List


class FilterInterface(ABC):
    @abstractmethod
    def filter_and_continue(self, unfiltered: str):
        pass


class Filter(FilterInterface):
    def __init__(self, next_filter: FilterInterface):
        self._next_filter = next_filter

    @property
    def next_filter(self) -> FilterInterface:
        return self._next_filter

    @next_filter.setter
    def next_filter(self, next_filter: FilterInterface):
        self._next_filter = next_filter

    @abstractmethod
    def filter_and_continue(self, request: str) -> str:
        if self._next_filter:
            return self._next_filter.filter_and_continue(request)

        return request


class TransparentFilter(Filter):
    def filter_and_continue(self, request: str) -> str:
        if self._next_filter:
            return self._next_filter.filter_and_continue(request)

        return request


class RemoveBadWordsFilter(Filter):
    def __init__(self, next_filter: FilterInterface, bad_words: List[str]):
        super().__init__(next_filter)
        self._bad_words = bad_words

    def filter_and_continue(self, request: str) -> str:
        for bw in self._bad_words:
            request = request.replace(bw, '')

        if self._next_filter:
            return self._next_filter.filter_and_continue(request)

        return request


class FilteringService:
    _instance = None
    _filters = None

    def __new__(cls):
        raise RuntimeError("Singleton class cannot be instantiated!")

    @classmethod
    def instance(cls, filters: List[Filter]):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._filters = [TransparentFilter(filters[0] if filters else None)] + filters

        return cls._instance

    def apply_filters(self, inp: str):
        return self._filters[0].filter_and_continue(inp)


if __name__ == '__main__':
    service = FilteringService.instance([RemoveBadWordsFilter(None, ['bad'])])

    print(service.apply_filters("A sentence with a bad word"))

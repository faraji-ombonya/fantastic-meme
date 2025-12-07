from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TransformedEntry:
    slug: str
    content: dict
    source: str


class Transformer(ABC):
    @abstractmethod
    def transform(self, entry: dict) -> TransformedEntry:
        pass


class TheStandardTransformer(Transformer):
    def transform(self, entry: dict):
        data = {
            "slug": entry.get("id"),
            "content": entry,
            "source": "standard",
        }
        return TransformedEntry(**data)


class TheStarTransformer(Transformer):
    def transform(self, entry: dict):
        data = {
            "slug": entry.get("link"),
            "content": entry,
            "source": "star",
        }
        return TransformedEntry(**data)

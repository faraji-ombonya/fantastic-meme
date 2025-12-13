from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TransformedEntry:
    slug: str
    """The slug of the post."""

    content: dict
    """Post content as a dictionary."""

    source: str
    """The source of the post, e.g. star, standard."""


class Transformer(ABC):
    @abstractmethod
    def transform(self, entry: dict) -> TransformedEntry:
        pass

    def bulk_transform(self, entries: list[dict]) -> list[TransformedEntry]:
        transformed_entries = []
        for entry in entries:
            transformed_entry = self.transform(entry)
            transformed_entries.append(transformed_entry)
        return transformed_entries


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

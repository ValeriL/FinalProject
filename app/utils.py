"""Converters for links."""
from typing import List, Tuple

from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):
    """Converter for list of tuples."""

    def to_python(self, value: str) -> List[Tuple[str, str]]:
        """Convert string to list."""
        return [tuple(x.split("_")) for x in value.split("+")]

    def to_url(self, values: List[Tuple[str, str]]) -> str:
        """Convert list to string."""
        return "+".join(f"{x}_{y}" for x, y in values)


class TupleConverter(BaseConverter):
    """Converter for tuple."""

    def to_python(self, value: str) -> Tuple[str, str]:
        """Convert string to tuple."""
        return tuple(value.split("_"))

    def to_url(self, values: Tuple[str, str]) -> str:
        """Convert tule to string."""
        x, y = values
        return f"{x}_{y}"

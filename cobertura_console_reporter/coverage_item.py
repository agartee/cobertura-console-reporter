"""Represents a test-covered .NET class."""

from dataclasses import dataclass
from typing import List

from attr import field


@dataclass
class CoverageItem:
    """Represents a test-covered .NET class."""

    name: str
    file_name: str
    coverable_lines: str
    covered_lines: str
    uncovered_line_numbers: List[int]
    branches: str
    covered_branches: str

    @property
    def class_name(self) -> str:
        """Class name"""
        if "." not in self.name:
            return self.name

        _, class_name = self.name.rsplit(".", 1)
        return class_name

    @property
    def class_namespace(self) -> str:
        """Class namespace"""
        if "." not in self.name:
            return ""

        namespace, _ = self.name.rsplit(".", 1)
        return namespace

"""Represents configuration settings for formatter functions."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FormatterConfig:
    """Represents configuration settings for formatter functions."""

    colorize: bool = True
    warning_threshold: Optional[float] = None

    @staticmethod
    def default() -> "FormatterConfig":  # pragma: no cover
        """Default formatter configuration

        Returns:
            FormatterConfig: an instance of a FormatterConfig
        """
        return FormatterConfig(colorize=True, warning_threshold=90)

    @staticmethod
    def no_color() -> "FormatterConfig":  # pragma: no cover
        """Default formatter configuration

        Returns:
            FormatterConfig: an instance of a FormatterConfig
        """
        return FormatterConfig(colorize=False)

# SPDX-License-Identifier: LGPL-2.1-only
import logging
import typing

from PyQt5 import QtWidgets

__all__ = ('CriteriaWidget',)


class CriteriaWidget(QtWidgets.QGroupBox):

    """Base class for criteria widgets."""

    def __init__(self, title: str, query, attrname: str,
                 parent: QtWidgets.QWidget | None = None) -> None:

        super().__init__(parent=parent)
        self.log: typing.Final = logging.getLogger(self.__module__)
        self.query: typing.Final = query
        self.attrname: typing.Final[str] = attrname

        self.setTitle(title)

    @property
    def has_errors(self) -> bool:
        """
        Get error state of this widget.

        If the error text is set, there is an error.
        """
        raise NotImplementedError

    #
    # Save/Load field
    #

    def save(self, settings: dict) -> None:
        """Save the widget settings to the settings dictionary."""
        raise NotImplementedError

    def load(self, settings: dict) -> None:
        """Load the widget settings from the settings dictionary."""
        raise NotImplementedError

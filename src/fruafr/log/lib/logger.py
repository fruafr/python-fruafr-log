# pylint: disable=line-too-long
# pylint: disable=protected-access
"""
Extends logging.Logger
Uses standards python logging.

Reference:
https://docs.python.org/3/library/logging.html
Contains:
- LoggerClass
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

import logging

# ---------------------------------------------------------------------------
#   Miscellaneous module data
# ---------------------------------------------------------------------------
#
# RAISEEXCEPTIONS is used to see if exceptions during handling should be
# propagated
#
RAISEEXCEPTIONS = True


class LoggerClass(logging.Logger):
    """LoggerClass extends logging.Logger"""

    def __init__(self, name, level=logging.NOTSET) -> None:
        """LoggerClass constructor
        Args:
            level (int, optional): The level integer [default: logging.NOTSET]
        """
        super().__init__(name, level)

    @property
    def default_formatter(self) -> logging.Formatter:
        """Returns the logger default formatter
        Returns:
            The logger formatter
        """
        return self._default_formatter

    @default_formatter.setter
    def default_formatter(self, formatter: logging.Formatter) -> None:
        """Set the default formatter to a given logging formatter
        Args:
            formatter (logging.Formatter): the logging formatter
        """
        if not isinstance(formatter, logging.Formatter):
            if RAISEEXCEPTIONS:
                raise TypeError("formatter must be a logging.Formatter")
            else:
                return
        # set the default formatter
        self._default_formatter = formatter

    def remove_handler(self, name: str) -> None:
        """Remove an Handler identified by its name
        Args:
            name (str): name of the Handler
        """
        if not isinstance(name, str):
            if RAISEEXCEPTIONS:
                raise TypeError("name must be a string")
            else:
                return
        logging._acquireLock()
        try:
            for hdlr in self.handlers:
                if hdlr._name == name:
                    self.handlers.remove(hdlr)
        finally:
            logging._releaseLock()

    def get_handler(self, name: str) -> logging.Handler:
        """Return an Handler based on its name
        Args:
            name (str): name of the Handler
        """
        out_hdlr = None
        if not isinstance(name, str):
            if RAISEEXCEPTIONS:
                raise TypeError("name must be a string")
            else:
                return
        logging._acquireLock()
        try:
            for hdlr in self.handlers:
                if hdlr._name == name:
                    out_hdlr = hdlr
        finally:
            logging._releaseLock()
        return out_hdlr

    def set_handler_level(self, name: str,
                          newlevel: int = logging.NOTSET) -> None:
        """Set the Handler level.
        The handler is identified by its name
        Args:
            name (str): name of the Handler
            newlevel (int): one of the logging levels.
            Defaults to logging.NOTSET
        """
        if not isinstance(name, str):
            if RAISEEXCEPTIONS:
                raise TypeError("name must be a string")
        if not isinstance(newlevel, int):
            if RAISEEXCEPTIONS:
                raise TypeError("newlevel must be an integer")
        hdlr = self.get_handler(name)
        # lock are handled at the handler level
        hdlr.setLevel(newlevel)

    def set_handler_name(self, oldname: str, newname: str) -> None:
        """Change the Handler name.
        The handler is identified by its old name
        Args:
            oldname (str): current name of the Handler
            newname (str): new name of the Handler to change the current \
                name to
        """
        if not isinstance(oldname, str):
            if RAISEEXCEPTIONS:
                raise TypeError("oldname must be a string")
        if not isinstance(newname, str):
            if RAISEEXCEPTIONS:
                raise TypeError("newname must be an string")
        hdlr = self.get_handler(oldname)
        # lock are handled at the handler level
        hdlr.set_name(newname)

    def set_handler_formatter(self, name: str,
                              newformatter: logging.Formatter) -> None:
        """Change the Handler Formatter.
        The handler is identified by its name
        Args:
            name (str): name of the Handler
            newformatter (logging.Formatter): the new handler formatter
        """
        if not isinstance(name, str):
            if RAISEEXCEPTIONS:
                raise TypeError("name must be a string")
        if not isinstance(newformatter, logging.Formatter):
            if RAISEEXCEPTIONS:
                raise TypeError("newformatter must be a logging.Formatter")
        hdlr = self.get_handler(name)
        # lock are handled at the handler level
        hdlr.setFormatter(newformatter)

    def __str__(self) -> str:
        """String representation of the object
        Returns:
            The string representation of the object
        """
        return f"{self.__class__}({self.name})"

    def __repr__(self) -> str:
        """Representation of the object
        Returns:
            The representation of the object
        """
        return f"{self.__class__}({self.__dict__}"

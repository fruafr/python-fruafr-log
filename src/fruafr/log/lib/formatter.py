"""
Uses standards python logging logger objects to template the formatter \
    string and create the formatter

Reference:
https://docs.python.org/3/library/logging.html#logger-objects

Contains:
- FormatterClass

"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>
import logging

from fruafr.log.lib import common

# ---------------------------------------------------------------------------
#   Miscellaneous module data
# ---------------------------------------------------------------------------
#
# RAISEEXCEPTIONS is used to see if exceptions during handling should be
# propagated
#
RAISEEXCEPTIONS = True


class FormatterClass(logging.Formatter):
    """FormatterClass
    """

    def __init__(self,
                 fmt=None,
                 datefmt=None,
                 style='%',
                 validate=True) -> None:
        """FormatterClass constructor
        Args:
            fmt (str, optional):  The format string
            datefmt (str, optional): The date format string
            style (str, optional): The style string [default: '%']
            validate (bool, optional): Whether to validate the formatting
             [default: True]
        """
        if fmt is not None:
            if not isinstance(fmt, str):
                if RAISEEXCEPTIONS:
                    raise TypeError("fmt must be a string")
                else:
                    return
        super().__init__(fmt, datefmt, style, validate)

    @property
    def supported(self) -> list:
        """Returns the supported format attribuates
        Returns:
            The supported format attribuates as a list
        """
        return common.LOGGING_OPTIONS.keys()

    @property
    def fmt(self) -> str:
        """Returns a format string
        Returns:
            The format string
        """
        return self._fmt

    @fmt.setter
    def fmt(self, fmtstr: str) -> None:
        """Sets the format string
        Args:
            fmtstr (str): The format string
        """
        if not isinstance(fmtstr, str):
            if RAISEEXCEPTIONS:
                raise TypeError("fmtstr must be a string")
            else:
                return
        self._fmt = fmtstr

    def _change_style(self, style: str = '%') -> None:
        """Apply a new formatting style
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        """
        if style not in logging._STYLES: #pylint: disable=protected-access
            if RAISEEXCEPTIONS:
                styles = ','.join(logging._STYLES.keys()) #pylint: disable=protected-access
                raise ValueError(f"Style must be one of: {styles}")
        if style == '{':
            self._fmt = self._fmt.replace('%(', '{').replace(')s', '}')\
                .replace(')d', '}').replace(')', '}')
        elif style == '$':
            self._fmt = self._fmt.replace('%(', '${').replace(')s', '}')\
                .replace(')d', '}').replace(')', '}')
        else:
            return

    def create_format_str(self,
                          kwargs: list,
                          sep: str = ' ',
                          style: str = '%') -> None:
        """Creates the format string from kwargs. Resets it if pre-existing
        Args:
            kwargs (list): list of kwargs
            sep (str, optional) : separator. [defaults: space]
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        """
        if not isinstance(kwargs, list):
            if RAISEEXCEPTIONS:
                raise TypeError("kwargs must be a list")
            else:
                return
        if style not in logging._STYLES: #pylint: disable=protected-access
            if RAISEEXCEPTIONS:
                styles = ','.join(logging._STYLES.keys()) #pylint: disable=protected-access
                raise ValueError(f"Style must be one of: {styles}")
            else:
                return
        if not isinstance(sep, str):
            if RAISEEXCEPTIONS:
                raise TypeError("sep must be a string")
            else:
                return
        self._fmt = ''
        n = 0
        for attr in kwargs:
            k = common.LOGGING_OPTIONS.keys()  # pylint: disable=E1101
            if attr not in k:
                print(f"{attr} is not supported")
                return
            if n > 0:
                self._fmt += f"{sep}{common.LOGGING_OPTIONS[attr]['format']}"
            else:
                self._fmt += str(common.LOGGING_OPTIONS[attr]['format'])  # pylint: disable=E1101
                n = 1
        # change the style if necessary
        self._change_style(style)
        # reformat
        self._style = logging._STYLES[style][0](self._fmt) #pylint: disable=protected-access
        self._fmt = self._style._fmt #pylint: disable=protected-access

    def default(self, style: str = '%') -> str:
        """Set the format string to default format as a String
        Creates the formatter accordingly
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        Returns:
            The default format string
        """
        # format
        self._fmt = common.DEFAULT_FORMAT
        # change the style if necessary
        self._change_style(style)
        return self.fmt

    def typical(self, style: str = '%') -> str:
        """Set the format string to typical format as a string
        Creates the formatter accordingly
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        Returns:
            The typical format string
        """
        self._fmt = common.TYPICAL_FORMAT
        # change the style if necessary
        self._change_style(style)
        return self.fmt

    def simple(self, style: str = '%') -> str:
        """Set the format string to simple format as a string
        Creates the formatter accordingly
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        Returns:
            The simple format string
        """
        self._fmt = common.SIMPLE_FORMAT
        # change the style if necessary
        self._change_style(style)
        return self.fmt

    def basic(self, style: str = '%') -> str:
        """Set the format string to basic format as a string
        Creates the formatter accordingly
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        Returns:
            The basic format string
        """
        self._fmt = common.BASIC_FORMAT
        # change the style if necessary
        self._change_style(style)
        return self.fmt

    def raw(self, style: str = '%') -> str:
        """Set the format string to raw format as a string
        Creates the formatter accordingly
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        Returns:
            The raw format string
        """
        self._fmt = common.RAW_FORMAT
        # change the style if necessary
        self._change_style(style)
        return self.fmt

    def custom(self, fmtstr: str, style: str = '%') -> str:
        """Set the format string to a custom string
        Creates the formatter accordingly
        Args:
            style (str, optional): The style string.
            Can be %, { or ( [default: '%']
        Returns:
            The custom format string
        """
        if not isinstance(fmtstr, str):
            if RAISEEXCEPTIONS:
                raise TypeError("fmtstr must be a string")
            else:
                return
        # change the style if necessary
        self._fmt = fmtstr
        self._change_style(style)
        return self.fmt

    def __str__(self) -> str:
        """String representation of the object
        Returns:
            The string representation of the object
        """
        return f"{self.__class__}({self._fmt})"

    def __repr__(self) -> str:
        """Representation of the object
        Returns:
            The representation of the object
        """
        return f"{self.__class__}({self.__dict__})"

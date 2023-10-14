"""
Templating utilities for custom logging message
"""
# Copyright 2023 by David Heurtevent.
# SPDX_LICENSE: MIT
# License: MIT License
# Author: David HEURTEVENT <david@heurtevent.org>

from string import Template

class Templating:
    """Class to perform basic templating"""

    @classmethod
    def create_template(cls, variables: list, separator: str = ',') -> str:
        """Prepare a template from the variables provided
        Args:
            variables (list): List of variables
            separator (str): Separator [default: ',']
        Returns:
            The template string (in string.Template format)
        """
        vars_new = []
        #add the dollar sign to the parameter
        for variable in variables:
            vars_new.append(f"${variable}")
        #prepare the template string
        return separator.join(vars_new)

    @classmethod
    def validate_template(cls, template: str, variables: list()) -> str :
        """
        Validate that each variable in the variables list is found in the template
        Args:
            template (str): template string
            variables (list): list of variables
        Returns:
            The first variable not found in the template (otherwise returns None)
        """
        for variable in variables :
            index = template.find(f"${variable}")
            if index == -1 :
                return variable

    @classmethod
    def apply_template(cls, template: str, valuesdict: dict) -> str :
        """Render the template
        Args:
            template: str: template string
            valuesdict: dict: values of the template variables
        Returns:
            The templated string
        """
        t = Template(template)
        return t.substitute(valuesdict)

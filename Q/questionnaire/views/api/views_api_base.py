####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django_filters import FilterSet, Filter


TRUE_VALUES = ["True", "true", "1", ]
FALSE_VALUES = ["False", "false", "0", ]


class BetterBooleanFilter(Filter):

    def filter(self, qs, value):
        """
        Overrides the built-in boolean filter to accept more than just "True" and "False"
        (that seemed pretty Pythonic for this JSON-based system)
        :param qs:
        :param value:
        :return:
        """
        if value is not None:
            if value in TRUE_VALUES:
                value = True
            elif value in FALSE_VALUES:
                value = False
            else:
                msg = "'{0}' is an invalid search term for the boolean field '{1}'. Valid terms include: {2}.".format(
                    value,
                    self.name,
                    ", ".join('"{0}"'.format(v) for v in TRUE_VALUES + FALSE_VALUES)
                )
                raise SyntaxError(msg)
            return qs.filter(**{self.name: value})
        else:
            return qs


class QFilterSet(FilterSet):
    """
    Simple way to make sure that _all_ filtered fields are available
    to views which use a FilterSet based on this class
    """

    @classmethod
    def get_field_names(cls):
        """
        Simple way to make sure that _all_ filtered fields
        are available to the views below
        """
        return tuple(cls.Meta.fields)

####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.conf import settings

# simple context processors that allow me to reference settings variables in templates
# be sure to add these to "settings.py"


def q_debug(context):
    """
    simple context processor that allows me to use a "debug" template tag
    without requiring me to explicitly provide "INTERNAL_IPS" in settings.py
    (as per http://stackoverflow.com/a/13609888/1060339)
    :param context:
    :return:
    """
    return {
        "debug": settings.DEBUG
    }


def q_obfuscate(context):
    return {
        "obfuscate": settings.OBFUSCATE
    }


def q_profile(context):
    return {
        "profile": settings.PROFILE
    }


def q_cdn(context):
    return {
        "cdn": settings.CDN
    }

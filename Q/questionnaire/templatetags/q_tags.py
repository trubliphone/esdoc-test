####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

"""
.. module:: q_tags

defines custom template tags
"""

from django import template
from django.conf import settings
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import json

from Q.questionnaire import get_version
from Q.questionnaire.models.models_sites import QSite
from Q.questionnaire.models.models_users import is_member_of as user_is_member_of, is_user_of as user_is_user_of, is_admin_of as user_is_admin_of, is_pending_of as user_is_pending_of
from Q.questionnaire.q_constants import *

register = template.Library()

#####################
# get static things #
#####################


@register.simple_tag
def q_version():
    return get_version()


@register.simple_tag
def q_url():
    return settings.Q_CODE_URL


@register.simple_tag
def q_email():
    return settings.Q_EMAIL


@register.simple_tag
def profanities():
    return mark_safe(PROFANITIES_LIST)


@register.simple_tag
def reserved_words():
    return mark_safe(RESERVED_WORDS)


#######################
# authentication tags #
#######################


@register.filter
def is_member_of(user, project):
    return user_is_member_of(user, project)


@register.filter
def is_user_of(user, project):
    return user_is_user_of(user, project)


@register.filter
def is_admin_of(user, project):
    return user_is_admin_of(user, project)


@register.filter
def is_pending_of(user, project):
    return user_is_pending_of(user, project)


#################
# dynamic sites #
#################

@register.filter
def site_type(site):
    try:
        q_site = site.q_site
        return q_site.type
    except QSite.DoesNotExist:
        return None

################
# utility tags #
################


@register.filter
def index(sequence, i):
    """
    returns the ith element in the sequence, otherwise returns an empty string
    :param sequence:
    :param i:
    :return:
    """
    try:
        return sequence[i]
    except IndexError:
        return u""


@register.filter
def jsonify(object):
    """
    returns a JSON representation of [a set of] object[s]
    :param object:
    :return:
    """
    # note: ng provides a "json" filter that can do this too
    # note: but Django doesn't [https://code.djangoproject.com/ticket/17419]
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)


@register.filter
def a_or_an(value):
    """
    filter to return "a" or "an" depending on whether string starts with a vowel sound
    """
    # TODO: handle confusing things like "an hour" or "a unicycle"
    vowel_sounds = ["a", "e", "i", "o", "u"]
    if value[0].lower() in vowel_sounds:
        return "an"
    else:
        return "a"


@register.filter
def format(value, arg):
    """
    Alters default filter "stringformat" to not add the % at the front,
    so the variable can be placed anywhere in the string.
    """
    try:
        if value is not None:
            # return (str(arg)) % value
            return (str(value)) % arg
        else:
            return ""
    except (ValueError, TypeError):
        return ""


#############################
# form / field manipulation #
#############################


@register.filter
def get_field_by_name(form, field_name):
    """
    gets a field from a form based on its name
    :param form:
    :param field_name:
    :return:
    """
    if field_name in form.fields:
        return form[field_name]
    return None


@register.filter
def get_fields_by_names(form, field_names):
    """
    gets a list of fields from a form based on their names
    :param form:
    :param field_names:
    :return:
    """
    fields = []
    for field_name in field_names.split(','):
        field = get_field_by_name(form, field_name)
        if field:
            fields.append(field)
    return fields


@register.filter
def get_form_by_field(formset, field_info):
    """
    gets a form from a formset based on a field_name/field_value pair
    :param formset:
    :param field_info:
    :return:
    """
    field_name, field_value = field_info.split('|')
    return formset.get_form_by_field(field_name, field_value)


@register.filter
def get_forms_by_field(formset, field_info):
    """
    gets a list of forms from a formset based on a field_name/field_value pair
    :param formset:
    :param field_info:
    :return:
    """
    field_name, field_value = field_info.split('|')
    return formset.get_forms_by_field(field_name, field_value)

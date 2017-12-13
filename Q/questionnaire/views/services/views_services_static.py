from django.http import HttpResponseBadRequest, JsonResponse
import re

from Q.questionnaire.models.models_projects import QProject
from Q.questionnaire.models.models_users import QUserProfile
from Q.questionnaire.q_fields import FIELD_TYPES
from Q.questionnaire.q_utils import convert_to_snake_case


validator_regex = re.compile("(^.*)(\_validator$)")


def serialize_static_field(field, **kwargs):
    assert field is not None

    include = kwargs.pop("include", {})
    exclude = kwargs.pop("exclude", [])

    serialized_static_field = {
        # "path": None,
        "name": field.name,
        "title": field.verbose_name.title(),
        "documentation": field.help_text,
        "inline_help": False,
        "is_editable": field.editable,
        "is_required": not field.blank,
        "is_displayed": True,
        "is_nillable": True,
        "validators": []
    }

    for v in field.validators:
        validator_name = convert_to_snake_case(type(v).__name__)
        serialized_static_field["validators"].append({
            "name": validator_regex.match(validator_name).groups()[0],
            "fn_name": validator_name,
            "msg": "<span class='glyphicon glyphicon-remove'/> {0}".format(v.message),
            "asynchronous": False,
        })

    if field.choices or field.is_relation:
        serialized_static_field["enumeration_choices"] = [
            {
                "order": i,
                "value": choice[0],
                "title": choice[1],
                "documentation": "",
                # "asynchronous": False,

            }
            for i, choice in enumerate(field.get_choices(include_blank=False))
        ]
        serialized_static_field["enumeration_open"] = False
        serialized_static_field["enumeration_multiple"] = field.many_to_many

    serialized_static_field.update(include)
    for e in exclude:
        serialized_static_field.pop(e, None)

    return serialized_static_field


def q_serialize_static_project(request, serialization_type=None):
    pass


def q_serialize_static_user_profile(request):
    """
    "fakes" a serialized QUserProfile proxy or customization (the content is the same; I just ignore the irrelevant bits)
    these are "static" objects, in that they are hard-coded and not actually dynamic
    this view just exists so that some of the Q's non-dynamic pages can use the same mechanisms as the dynamic pages
    :param request:
    :param model_type:
    :param model_id:
    :param serialization_type:
    :return:
    """

    static_serialization = {
        "properties": [
            serialize_static_field(
                QUserProfile.get_field("user.first_name"),
                include={
                    "path": ".user.first_name",
                    "field_type": FIELD_TYPES["string"],
                    "order": 0,
                    "placeholder": "what's your first name?",
                },
                exclude=[]
            ),
            serialize_static_field(
                QUserProfile.get_field("user.last_name"),
                include={
                    "path": ".user.last_name",
                    "field_type": FIELD_TYPES["string"],
                    "order": 1,
                    "placeholder": "what's your last name?",
                },
                exclude=[]
            ),
            serialize_static_field(
                QUserProfile.get_field("user.email"),
                include={
                    "path": ".user.email",
                    "field_type": FIELD_TYPES["email"],
                    "order": 2,
                    "is_editable": False,
                },
                exclude=[]
            ),
            serialize_static_field(
                QUserProfile.get_field("description"),
                include={
                    "path": ".description",
                    "field_type": FIELD_TYPES["text"],
                    "order": 3,
                    "placeholder": "tell us about yourself!",
                },
                exclude=[]
            ),
            serialize_static_field(
                QUserProfile.get_field("institute"),
                include={
                    "path": ".institute",
                    "field_type": FIELD_TYPES["enumeration"],
                    "order": 4,

                },
                exclude=[]
            ),
        ]
    }

    return JsonResponse(static_serialization)

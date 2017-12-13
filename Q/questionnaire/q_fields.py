from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError as DjangoValidationError
# from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models.signals import post_delete
from django.forms import CharField
import os
import re

from Q.questionnaire.q_utils import Version
from Q.questionnaire.q_constants import *

FIELD_TYPES = {
    "string": {
        "tag": "input",
        "title": "character string",
        "type": "text",
        "attrs": {}
    },
    "text": {
        "tag": "textarea",
        "title": "text",
        "type": None,
        "attrs": {
            "rows": "4"
        }
    },
    "bool": {
        "tag": "input",
        "title": "boolean value",
        "type": "checkbox",
        "attrs": {}
    },
    "int": {
        "tag": "input",
        "title": "integer",
        "type": "number",
        "attrs": {}
    },
    "float": {
        "tag": "input",
        "title": "floating-point number",
        "type": "number",
        "attrs": {}
    },
    "url": {
        "tag": "input",
        "title": "URL",
        "type": "url",
        "attrs": {}
    },
    "email": {
        "tag": "input",
        "title": "email address",
        "type": "text",
        "attrs": {}
    },
    "date": {
        "tag": "input",
        "title": "date",
        "type": "text",
        "attrs": {
            "uib-datepicker-popup": None
        }
    },
    "datetime": {
        "tag": "input",
        "title": "date and time",
        "type": "text",
        "attrs": {}
    },
    "time": {
        "tag": "input",
        "title": "time",
        "type": "text",
        "attrs": {}
    },
    "enumeration": {
        "tag": "select",
        "title": "enumeration",
        "type": "text",
        "attrs": {
            "style": "display: none"
        }
    },
    "relation": {
        "tag": "input",
        "title": "relation to other object",
        "type": "text",
        "attrs": {}
    },
    "reference": {
        "tag": "input",
        "title": "reference to other document",
        "type": "text",
        "attrs": {}
    }
}

DEFAULT_FIELD_TYPE_KEY = "string"


###############
# file fields #
###############


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            file_path = os.path.join(settings.MEDIA_ROOT, name)
            os.remove(file_path)
        return name


class QFileField(models.FileField):
    """
    just like a standard Django FileField,
    except it uses the above OverwriteStorage class,
    and it deletes the file when the corresponding class instance is deleted
    (so long as no other class members are using it)
    """

    default_help_text = "Note that files with the same names will be overwritten"

    def __init__(self, *args, **kwargs):
        """
        ensure that OverwriteStorage is used,
        and provide help_text (if none was specified)
        :param args:
        :param kwargs:
        :return:
        """

        help_text = kwargs.pop("help_text", self.default_help_text)
        kwargs.update({
            "storage": OverwriteStorage(),
            "help_text": help_text
        })
        super(QFileField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        attach the "post_delete" signal of the model class
        to the "delete_file" fn of the field class
        :param cls:
        :param name:
        :return: None
        """
        super(QFileField, self).contribute_to_class(cls, name, **kwargs)
        post_delete.connect(self.delete_file, sender=cls)

    def delete_file(self, sender, **kwargs):
        """
        delete the file iff no other class instance point to it
        :param sender:
        :return: None
        """
        instance = kwargs.pop("instance")
        instance_field_name = self.name
        instance_field = getattr(instance, instance_field_name)
        filter_parameters = {
            instance_field_name: instance_field.name,
        }
        other_instances_with_same_file = sender.objects.filter(**filter_parameters)
        if not len(other_instances_with_same_file):
            # if there are no other instances w/ the same file...
            # delete the file...
            instance_field.delete(save=False)  # save=False prevents model from re-saving itself


##################
# version fields #
##################

class QVersionFormField(CharField):

    def clean(self, value):
        # check string format (only numbers and the '.' character

        if not re.match(r'^([0-9]\.?)+$', value):
            msg = "Versions must be of the format 'major.minor.patch'"
            raise DjangoValidationError(msg)

        return value


class QVersionField(models.IntegerField):

    # TODO: models w/ this field have to call refresh_from_db if set manually
    # TODO: (ie: if set in tests)

    def formfield(self, **kwargs):
        default_kwargs = {
            "form_class": QVersionFormField,
        }
        default_kwargs.update(kwargs)
        return super(QVersionField, self).formfield(**default_kwargs)

    def to_python(self, value):
        """
        db to code; int to Version
        """
        if isinstance(value, Version):
            return value

        if isinstance(value, str):
            return Version(value)

        if value is None:
            return None

        return Version(Version.int_to_string(value))

    def get_prep_value(self, value):
        """
        code to db; Version to int
        """
        if isinstance(value, str):
            return Version.string_to_int(value)

        if value is None:
            return None

        return int(value)

    def from_db_value(self, value, expression, connection, context):
        """
        does the same thing as "to_python",
        it's just called in different situations b/c of a quirk w/ Django 1.8
        (see https://docs.djangoproject.com/en/1.8/howto/custom-model-fields/)
        """
        return self.to_python(value)

    def contribute_to_class(self, cls, name, **kwargs):
        """
        adds "get/<field_name>_major/minor/patch" fns to the class
        :param cls:
        :param name:
        :param kwargs:
        :return:
        """
        super(QVersionField, self).contribute_to_class(cls, name, **kwargs)

        def _get_major(instance, field_name=name):
            """
            notice how I pass the name of the field from the parent "contribute_to_class" fn;
            this lets me access it from the instance
            :param instance:
            :param field_name:
            :return:
            """
            version_value = getattr(instance, field_name)
            return version_value.major()

        def _get_minor(instance, field_name=name):
            """
            notice how I pass the name of the field from the parent "contribute_to_class" fn;
            this lets me access it from the instance
            :param instance:
            :param field_name:
            :return:
            """
            version_value = getattr(instance, field_name)
            return version_value.minor()

        def _get_patch(instance, field_name=name):
            """
            notice how I pass the name of the field from the parent "contribute_to_class" fn;
            this lets me access it from the instance
            :param instance:
            :param field_name:
            :return:
            """
            version_value = getattr(instance, field_name)
            return version_value.patch()

        get_major_fn_name = "get_{0}_major".format(name)
        get_minor_fn_name = "get_{0}_minor".format(name)
        get_patch_fn_name = "get_{0}_patch".format(name)
        setattr(cls, get_major_fn_name, _get_major)#types.MethodType(_get_major, None, cls))
        setattr(cls, get_minor_fn_name, _get_minor)# types.MethodType(_get_minor, None, cls))
        setattr(cls, get_patch_fn_name, _get_patch)#types.MethodType(_get_patch, None, cls))

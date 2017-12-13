from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

from django.db.models.fields import FieldDoesNotExist
from Q.questionnaire import APP_LABEL


class QPostgresModel(models.Model):
    class Meta:
        app_label = APP_LABEL
        abstract = True

    @classmethod
    def get_field(cls, field_name):
        """
        convenience fn for getting a Django Field
        (used for serializing static customizations)
        note that this can take as input a JSON-style name to better work w/ Angular
        :param field_name: a fully-qualified field name (ie: "model.child.field")
        :return:
        """
        try:
            model_class = cls
            for fn in field_name.split("."):
                field = model_class._meta.get_field(fn)
                model_class = field.related_model
            return field
        except (AttributeError, FieldDoesNotExist):
            return None


class QMongoModel(Document):
    class Meta:
        app_label = APP_LABEL
        abstract = True

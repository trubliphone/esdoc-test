from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

from Q.questionnaire.q_constants import BIG_STRING
from Q.questionnaire import APP_LABEL


class QTestPostgresModel(models.Model):

    class Meta:
        app_label = APP_LABEL
        abstract = False
        verbose_name = "Questionnaire Test Postgres Model"
        verbose_name_plural = "Questionnaire Test Postgres Models"

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    name = models.CharField(max_length=BIG_STRING, blank=False)
    documentation = models.TextField(blank=True, null=True)


class QTestMongodbChildModel(EmbeddedDocument):

    name = fields.StringField(required=True)
    documentation = fields.StringField(required=False, null=True)


class QTestMongodbModel(Document):

    name = fields.StringField(required=True)
    documentation = fields.StringField(required=False, null=True)
    children = fields.ListField(fields.EmbeddedDocumentField(QTestMongodbChildModel))


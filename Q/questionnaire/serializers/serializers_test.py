####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework_mongoengine.serializers import DocumentSerializer
from uuid import UUID as generate_uuid

from Q.questionnaire.models.models_test import QTestPostgresModel, QTestMongodbModel
from Q.questionnaire.q_constants import *


class QTestPostgresModelSerializer(ModelSerializer):

    class Meta:
        model = QTestPostgresModel
        fields = (
            'id',
            'name',
            'documentation',
            'created',
            'modified',
        )


class QTestMongoModelSerializer(DocumentSerializer):

    class Meta:
        model = QTestMongodbModel
        fields = (
            'id',
            'name',
            'documentation',
            'children',
        )

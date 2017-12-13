####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

# from django.core.exceptions import ValidationError as DjangoValidationError
# from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from Q.questionnaire.models.models_projects import QProject


class QProjectSerializer(ModelSerializer):

    class Meta:
        model = QProject
        fields = (
            'id',
            'name',
            'title',
            'description',
            'order',
            'email',
            'url',
            # TODO: LOGO STUFF
            'authenticated',
            'is_legacy',
             'is_active',
            'is_displayed',
            'ontologies',

        )
        extra_kwargs = {
        }

    ontologies = SerializerMethodField()

    def get_ontologies(self, obj):
        ontologies = obj.ontologies.all()
        return [
            {
                "name": ontology.name,
                "version": ontology.version,
            }
            for ontology in ontologies
        ]



####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.core.exceptions import ValidationError as DjangoValidationError
# from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import Field, SerializerMethodField
from Q.questionnaire.models.models_projects import GROUP_PERMISSIONS
from Q.questionnaire.models.models_users import QUserProfile

# TODO: DO I HAVE TO MAKE ANY CHANGES TO SUPPORT 'allauth.socialaccount' ?


# institute is a fk, but the client treats it as a Q Enumeration
# this class makes sure that those two representations play nicely together
# (specifically, this means the client deals w/ lists of values while the server deals w/ single integer pks)

class InstituteField(Field):

    def __init__(self, **kwargs):
        self.queryset = kwargs.pop('queryset', QUserProfile.institute.get_queryset())
        super(InstituteField, self).__init__(**kwargs)

    def to_representation(self, obj):
        # given a Pythonic representation, return a serialized representation
        data = []
        if obj is not None:
            data.append(obj.pk)
        return data

    def to_internal_value(self, data):
        # given a serialized representation, return a Pythonic representation
        if len(data):
            obj = self.queryset.get(pk=data[0])
            return obj
        return None


class QUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        # this is needed to allow this writable nested serializer to cope w/ the unique constraint on username
        # (this is a known issue: https://github.com/encode/django-rest-framework/issues/2996)
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()]
            }
        }


class QUserProfileSerializer(ModelSerializer):

    class Meta:
        model = QUserProfile
        fields = (
            'id',
            'projects',
            'change_password',
            'description',
            'institute',
            'is_verified',
            'user',
        )

    projects = SerializerMethodField()
    institute = InstituteField(allow_null=True)
    user = QUserSerializer(many=False)

    def get_projects(self, obj):
        projects = obj.projects.all()
        return [
            {
                "name": project.name,
                "title": project.title,
                "permissions": [gp for gp in GROUP_PERMISSIONS if obj.user in project.get_group(gp).user_set.all()],
            }
            for project in projects
        ]

    def to_representation(self, instance):
        # if "institute" is None, then the serializer field above does not get used
        # I am overriding that behaviour here
        # (the inspiration came from: https://gist.github.com/mpyrev/e59919e1e9bbbe4eeec17cb0fa6ba07a)
        representation = super(QUserProfileSerializer, self).to_representation(instance)
        if representation["institute"] is None:
            representation["institute"] = []
        return representation

    def create(self, validated_data):
        user_serializer = self.fields["user"]
        user_data = validated_data.pop(user_serializer.source, [])

        if user_data:
            user = user_serializer.create(user_data)
            validated_data["user"] = user
            # QUserProfile is a special case, b/c it's already created automatically via signals whenever a User is created...
            user_profile = super(QUserProfileSerializer, self).update(user.profile, validated_data)
        else:
            user_profile = super(QUserProfileSerializer, self).create(validated_data)
        return user_profile

    def update(self, instance, validated_data):
        user_serializer = self.fields["user"]
        user_data = validated_data.pop(user_serializer.source, [])

        if user_data:
            user = user_serializer.update(instance.user, user_data)
            validated_data["user"] = user

        user_profile = super(QUserProfileSerializer, self).update(instance, validated_data)
        return user_profile

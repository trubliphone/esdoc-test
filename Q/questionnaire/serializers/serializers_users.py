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
from rest_framework.fields import SerializerMethodField
from Q.questionnaire.models.models_projects import GROUP_PERMISSIONS
from Q.questionnaire.models.models_users import QUserProfile

# TODO: DO I HAVE TO MAKE ANY CHANGES TO SUPPORT 'allauth.socialaccount' ?


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

    def create(self, validated_data):
        user_serializer = self.fields["user"]
        user_data = validated_data.pop(user_serializer.source, [])

        if user_data:
            user = user_serializer.create(user_data)
            validated_data["user"] = user
            # QUserProfile is a special case, b/c it's created automatically via signals whenever a User is created...
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

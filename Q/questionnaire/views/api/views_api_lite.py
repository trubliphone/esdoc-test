####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

# from django.contrib.auth.models import User

from django_filters import FilterSet, CharFilter
from rest_framework import permissions, viewsets


from Q.questionnaire.models.models_users import QUserProfile
from Q.questionnaire.serializers.serializers_lite import QUserProfileLiteSerializer
from Q.questionnaire.views.api.views_api_base import BetterBooleanFilter


class QModelLitePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # anybody can submit GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # nobody can submit PUT, POST, or DELETE requests
        # (this is the "lite" serialization, after all)
        return False


class QUserProfileLiteFilter(FilterSet):

    class Meta:
        model = QUserProfile
        fields = [
            'id',
            'username',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

    is_active = BetterBooleanFilter(name="user__is_active")
    is_staff = BetterBooleanFilter(name="user__is_staff")
    is_superuser = BetterBooleanFilter(name="user__is_superuser")
    username = CharFilter(name='user__username')


    @classmethod
    def get_field_names(cls):
        """
        Simple way to make sure that _all_ filtered fields
        are available to the views below
        """
        return tuple(cls.Meta.fields)


class QUserProfileLiteViewSet(viewsets.ModelViewSet):
    serializer_class = QUserProfileLiteSerializer
    permission_classes = [QModelLitePermission]
    queryset = QUserProfile.objects.all()
    filter_class = QUserProfileLiteFilter

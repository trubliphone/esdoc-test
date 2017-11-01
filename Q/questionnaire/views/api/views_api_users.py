####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from rest_framework import permissions, viewsets

from Q.questionnaire.models.models_users import QUserProfile
from Q.questionnaire.serializers.serializers_users import QUserProfileSerializer
from Q.questionnaire.views.api.views_api_base import QFilterSet, BetterBooleanFilter


class QUserProfilePermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # anybody can submit GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # only the superuser or the user can submit PUT, POST, or DELETE requests
        current_user = request.user
        if current_user.is_superuser or current_user == obj.user:
            return True
        else:
            return False


class QUserProfileFilterSet(QFilterSet):

    class Meta:
        model = QUserProfile
        fields = [
            'projects',
            'change_password',
            'institute',
            'user__username',
            'user__first_name',
            'user__last_name',
            'user__email',
            'user__is_active',
            'user__is_staff',
            'user__is_superuser',
        ]

    change_password = BetterBooleanFilter(name="change_password")
    user__is_active = BetterBooleanFilter(name="user__is_active")
    user__is_staff = BetterBooleanFilter(name="user__is_staff")
    user__is_superuser = BetterBooleanFilter(name="user__is_superuser")


class QUserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = QUserProfileSerializer
    permission_classes = [QUserProfilePermission]
    queryset = QUserProfile.objects.all()
    filter_class = QUserProfileFilterSet


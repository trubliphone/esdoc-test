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

from Q.questionnaire.models.models_projects import QProject
from Q.questionnaire.models.models_users import is_admin_of, is_member_of, is_user_of, is_pending_of
from Q.questionnaire.serializers.serializers_projects import QProjectSerializer
from Q.questionnaire.views.api.views_api_base import QFilterSet, BetterBooleanFilter


class QProjectPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # anybody can submit GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # only the superuser or the project admin can submit PUT, POST, or DELETE requests
        current_user = request.user
        if current_user.is_superuser or is_admin_of(current_user, obj):
            return True
        else:
            return False


class QProjectFilterSet(QFilterSet):

    class Meta:
        model = QProject
        fields = [
            'is_legacy',
            'is_active',
            'is_displayed',
        ]

    is_legacy = BetterBooleanFilter(name="is_legacy")
    is_active = BetterBooleanFilter(name="is_active")
    is_displayed = BetterBooleanFilter(name="is_displayed")


class QProjectViewSet(viewsets.ModelViewSet):
    serializer_class = QProjectSerializer
    permission_classes = [QProjectPermission]
    queryset = QProject.objects.all()
    filter_class = QProjectFilterSet

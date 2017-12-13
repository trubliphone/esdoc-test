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
from Q.questionnaire.serializers.serializers_lite import QProjectLiteSerializer


class QLitePermission(permissions.BasePermission):
    """
    Lite Serializers are read-only
    """

    def has_object_permission(self, request, view, obj):
        # anybody can submit GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # nobody can submit PUT, POST, or DELETE requests
        return False


class QProjectLiteViewSet(viewsets.ModelViewSet):
    serializer_class = QProjectLiteSerializer
    permission_classes = [QLitePermission]
    queryset = QProject.objects.filter(is_active=True, is_displayed=True)


####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.http import Http404
from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
# OKAY, SO "viewsets" AREN'T AS CONFIGURABLE AS SEPARATE CUSTOM VIEWS,
# BUT IT IS HOW DRFM INTEGRATES W/ DRF...
# AND, ANYWAY, SINCE PROXIES/CUSTOMIZATIONS/REALIZATIONS NO LONGER USE POSTGRES, I DON'T HAVE MUCH CUSTOM STUFF TO DO
# HOORAY
from rest_framework import viewsets
from rest_framework_mongoengine import viewsets as mongo_viewsets

from Q.questionnaire.models.models_test import QTestPostgresModel, QTestMongodbModel
from Q.questionnaire.serializers.serializers_test import QTestPostgresModelSerializer, QTestMongoModelSerializer


class QTestPostgresModelPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # anybody can submit GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # nobody can submit PUT, POST, or DELETE requests
        return False


# class QTestPostgresModelDetail(APIView):
#     """
#     Retrieve, update or delete a model instance.
#     """
#
#     permission_classes = [QTestPostgresModelPermission]
#
#     def get_object(self, pk):
#
#         try:
#             return QTestPostgresModel.objects.get(pk=pk)
#         except QTestPostgresModel.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         model = self.get_object(pk)
#         serializer = QTestPostgresModelSerializer(model, context={"request": request})
#         return Response(serializer.data)
#
#
# class QTestPostgresModelList(generics.ListAPIView):
#     queryset = QTestPostgresModel.objects.all()
#     serializer_class = QTestPostgresModelSerializer
#     filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
#     # filter_class = QModelCustomizationFilter
#     # filter_fields = QModelCustomizationFilter.get_field_names()
#     ordering_fields = ("name", )
#     ordering = "name"
#

class QTestPostgresModelViewSet(viewsets.ModelViewSet):
    serializer_class = QTestPostgresModelSerializer
    permission_classes = [QTestPostgresModelPermission]
    queryset = QTestPostgresModel.objects.all()


class QTestMongodbModelViewSet(mongo_viewsets.ModelViewSet):

    serializer_class = QTestMongoModelSerializer
    lookup_field = 'id'
    # queryset = QTestMongodbModel.objects.all()

    def get_queryset(self):
        return QTestMongodbModel.objects.all()
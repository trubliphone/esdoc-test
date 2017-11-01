# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
#
# from collections import OrderedDict
# from django.core.urlresolvers import NoReverseMatch
#
# from rest_framework import routers, views, response
# from rest_framework.reverse import reverse

from rest_framework import routers

from Q.questionnaire.views.api.views_api_users import QUserProfileViewSet
from Q.questionnaire.views.api.views_api_tests import QTestPostgresModelViewSet
from Q.questionnaire.views.api.views_api_tests import QTestMongodbModelViewSet

# define a router for the DRF API which works with both postgres & mongodb
# (this is separate from the router for the DB, defined in "Q/questionnaire/__init__.py")

q_api_router = routers.DefaultRouter()

q_api_router.register(r'quserprofile', QUserProfileViewSet, r'quserprofile')

q_api_router.register(r'qtestmongodbmodel', QTestMongodbModelViewSet, r'qtestmongodbmodel')
q_api_router.register(r'qtestpostgresmodel', QTestPostgresModelViewSet, r'qtestpostgresmodel')



# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'test_posgres': reverse('test_postgres-list', request=request, format=format),
#         'test_mongodb': reverse('test_mongodb-list', request=request, format=format),
#     })

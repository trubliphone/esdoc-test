####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.conf import settings
from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns


from Q.questionnaire.views import *
from Q.questionnaire.views.api import *
from Q.questionnaire.views.services import *

api_urls = [
    url(r'', include(q_api_router.urls, namespace='api'))
]


#
#
# api_urls = [
#
#     # just some testing (obviously)...
#     url(r'^test_postgres/$', QTestPostgresModelList.as_view(), name="test_postgres-list"),
#     url(r'^test_postgres/(?P<pk>[0-9]+)/$', QTestPostgresModelDetail.as_view(), name="test_postgres-detail"),
#     url(r'^test_mongodb/$', QTestMongodbModelViewSet, name="test_mongodb-list"),
#
# ]
#
# if settings.DEBUG:
#     # only expose pre-defined api urls in debug mode...
#     api_urls.insert(0, url(r'^$', api_root))
#
# TODO: THIS DOESN'T WORK W/ MONGODB APIS
# automatically add support for different serialization formats (JSON is default)...
# api_urls = format_suffix_patterns(api_urls)


services_urls = [

    # getting pending messages...
    url(r'^messages/$', get_django_messages),

    # routing http calls through a proxy...
    url(r'^proxy/$', q_proxy, name="proxy"),

    # validating forms...
    url(r'^validate/$', q_validate, name="validate"),

    # logging data from the client...
    url(r'^log/$', q_log, name="log"),

    # setting up users...
    url(r'^accounts/send_email_confirmation/$', q_send_email_confirmation),

    # 'faking' static models...
    url(r'^static/quserprofile/$', q_serialize_static_user_profile),
    url(r'^static/qproject/$', q_serialize_static_project),

]


urlpatterns = [

    # RESTful API...
    url(r'^api/', include(api_urls)),

    # webservices outside of RESTful API...
    url(r'^services/', include(services_urls)),

    # testing (obviously)...
    url(r'^test/$', q_test, name="test"),

    # help...
    url(r'^help/$', RedirectView.as_view(url=settings.Q_HELP_URL, permanent=True), name="help"),

    # # customizations...
    # url(r'^(?P<project_name>[^/]+)/customize/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/$', q_customize_new, name="customize_new"),
    # url(r'^(?P<project_name>[^/]+)/customize/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/(?P<customization_name>[^/]+)/$', q_customize_existing, name="customize_existing"),
    #
    # # realizations...
    # url(r'^(?P<project_name>[^/]+)/edit/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/$', q_edit_new, name="edit_new"),
    # url(r'^(?P<project_name>[^/]+)/edit/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/(?P<realization_pk>[^/]+)/$', q_edit_existing, name="edit_existing"),
    # url(r'^(?P<project_name>[^/]+)/view/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/$', q_view_new, name="view_new"),
    # url(r'^(?P<project_name>[^/]+)/view/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/(?P<realization_pk>[^/]+)/$', q_view_existing, name="view_existing"),
    # url(r'^(?P<project_name>[^/]+)/get/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/$', q_get_existing, name="get_existing"),
    #
    # # publications (ATOM feed)...
    # url(r'^feed/$', QFeed(), name="feed"),
    # url(r'^feed/(?P<project_name>[^/]+)/$', QFeed(), name="feed_project"),
    # url(r'^feed/(?P<project_name>[^/]+)/(?P<ontology_key>[^/]+)/$', QFeed(), name="feed_project_ontology"),
    # url(r'^feed/(?P<project_name>[^/]+)/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/$', QFeed(), name="feed_project_ontology_proxy"),
    # url(r'^feed/(?P<project_name>[^/]+)/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/(?P<publication_name>[^/]+)/$', q_publication, name="publication_latest"),
    # url(r'^feed/(?P<project_name>[^/]+)/(?P<ontology_key>[^/]+)/(?P<document_type>[^/]+)/(?P<publication_name>[^/]+)/(?P<publication_version>[^/]+)/$', q_publication, name="publication_version"),
    #
    # # projects...
    # url(r'^(?P<project_name>[^/]+)/$', q_project, name="project"),
    # url(r'^(?P<project_name>[^/]+)/customize/$', q_project_customize, name="project_customize"),
    # url(r'^(?P<project_name>[^/]+)/manage/$', q_project_manage, name="project_manage"),

    # index...
    url(r'^$', q_index, name="index"),

]

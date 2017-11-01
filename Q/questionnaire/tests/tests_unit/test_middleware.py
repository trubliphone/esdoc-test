####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

"""
.. module:: test_middleware

Tests for custom middleware.  This includes dynamic_sites
"""

from django.core.urlresolvers import resolve, reverse

from django.test.client import RequestFactory
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site

from Q.questionnaire.middleware.dynamic_sites import DynamicSitesMiddleware
from Q.questionnaire.tests.test_base import TestQBase


class Test(TestQBase):

    def setUp(self):
        # no need for any questionnaire-specific stuff
        pass

    def tearDown(self):
        # no need for any questionnaire-specific stuff
        pass

    def test_dynamic_sites(self):

        test_factory = RequestFactory()
        test_request = test_factory.get(reverse("test"))
        test_view = resolve(reverse("test"))[0]

        dynamic_sites_middleware = DynamicSitesMiddleware(test_view)

        dynamic_sites_middleware(test_request)

        current_site = get_current_site(test_request)
        old_site = Site.objects.get(pk=settings.SITE_ID)

        self.assertEqual(current_site, old_site)
        self.assertEqual(settings.SITE_ID, old_site.id)

        new_site = Site(name="test_site", domain="testserver")
        new_site.save()

        dynamic_sites_middleware(test_request)

        current_site = get_current_site(test_request)

        self.assertEqual(current_site, new_site)
        self.assertEqual(settings.SITE_ID, new_site.id)

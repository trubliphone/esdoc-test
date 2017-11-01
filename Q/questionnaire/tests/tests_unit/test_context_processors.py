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
.. module:: test_context_processors

Tests for custom context_processors.

"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, override_settings

from Q import settings as app_settings
from Q.questionnaire.context_processors import *
from Q.questionnaire.tests.test_base import TestQBase


# by default Django sets DEBUG to False during tests,
# this decorator ensures it uses the value specified in the configuration file
@override_settings(DEBUG=app_settings.DEBUG)
class Test(TestQBase):

    def setUp(self):
        # no need for any questionnaire-specific stuff
        pass

    def tearDown(self):
        # no need for any questionnaire-specific stuff
        pass

    def test_debug(self):

        client = Client()
        test_context = client.get(reverse("test")).context

        self.assertEqual(settings.DEBUG, q_debug(test_context).get("debug"))

    def test_obfuscate(self):

        client = Client()
        test_context = client.get(reverse("test")).context

        self.assertEqual(settings.OBFUSCATE, q_obfuscate(test_context).get("obfuscate"))

    def test_profile(self):

        client = Client()
        test_context = client.get(reverse("test")).context

        self.assertEqual(settings.PROFILE, q_profile(test_context).get("profile"))

    def test_cdn(self):

        client = Client()
        test_context = client.get(reverse("test")).context

        self.assertEqual(settings.CDN, q_cdn(test_context).get("cdn"))

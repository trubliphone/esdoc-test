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
.. module:: models_sites

Q-specific sites

"""

from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings

from Q.questionnaire import APP_LABEL
from Q.questionnaire.q_utils import EnumeratedType, EnumeratedTypeList
from Q.questionnaire.q_constants import *


class QSiteType(EnumeratedType):
    pass

QSiteTypes = EnumeratedTypeList([
    QSiteType("LOCAL", "Local"),
    QSiteType("TEST", "Test"),
    QSiteType("DEV", "Development"),
    QSiteType("PROD", "Production"),
])


class QSite(models.Model):

    class Meta:
        app_label = APP_LABEL
        abstract = False
        verbose_name = 'Questionnaire Site'
        verbose_name_plural = 'Questionnaire Sites'

    # 1to1 relationship w/ standard Django Site...
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="q_site")

    # extra info associated w/ a Questionnaire Site...
    type = models.CharField(
        max_length=LIL_STRING,
        blank=True,
        choices=[(type.get_type(), type.get_name()) for type in QSiteTypes]
    )

    def __str__(self):
        return "{0}".format(self.site)

    @classmethod
    def get_current_site(self):
        # assuming that requests have been made prior to calling this fn,
        # the "dynamic_sites" middleware will have run which will have set "settings.SITE_ID" correctly
        return Site.objects.get(pk=settings.SITE_ID)
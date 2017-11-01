"""
.. module:: q_dynamic_sites

Sets current site dynamically on a per-request basis.
This is needed b/c the site information is used for various messages that get emailed to administrators
(such as project join requests); In order to process the request, recipients must know which site to act upon.
"""

from django.conf import settings
from django.contrib.sites.models import Site


class DynamicSitesMiddleware(object):
    """
    Intercepts request as per standard Django middleware
    Tries to find a site in the db based on the request's domain
    :param request:
    :return:
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.set_site(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def set_site(self, request):
        domain = request.get_host()
        try:
            current_site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            # rather than raising an error, just use site w/ a pk=1 (as per settings.DEFAULT_SITE_ID)
            # msg = "Unable to locate domain '%s' in Sites.  Please update the database." % domain
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)

        settings.SITE_ID = current_site.id
        request.current_site = current_site


from allauth.account.adapter import DefaultAccountAdapter
from allauth.compat import is_authenticated
from django.core.urlresolvers import reverse


class QAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.
        Note that URLs passed explicitly (e.g. by passing along a `next`
        GET parameter) take precedence over the value returned here.
        """
        import ipdb; ipdb.set_trace()
        assert is_authenticated(request.user)
        path = reverse("account_profile", kwargs={
            "username": request.user.username
        })
        return path
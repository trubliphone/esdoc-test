from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve

from allauth.account import views as account_views
from allauth.socialaccount import providers
from importlib import import_module
from Q.questionnaire.views.views_users import *

admin.autodiscover()

account_urls = [
    # this mostly uses the default allauth views...
    # but overrides a few for Q-specific functionality...
    # and adds some for dealing w/ Q-specific User Profiles

    # authentication...
    url(r"^signup/$", QSignupView.as_view(), name="account_signup"),
    url(r"^login/$", QLoginView.as_view(), name="account_login"),
    url(r"^logout/$", QLogoutView.as_view(), name="account_logout"),

    # 3rd party authentication...
    url(r"^social/", include('allauth.socialaccount.urls')),

    # disabled accounts...
    url(r"^inactive/$", account_views.account_inactive, name="account_inactive"),

    # e-mail...
    url(r"^email/$", account_views.email, name="account_email"),
    url(r"^confirm-email/$", account_views.email_verification_sent, name="account_email_verification_sent"),
    url(r"^confirm-email/(?P<key>[-:\w]+)/$", account_views.confirm_email, name="account_confirm_email"),

    # password set...
    url(r"^password/change/$", account_views.password_change, name="account_change_password"),
    url(r"^password/set/$", account_views.password_set, name="account_set_password"),

    # password reset...
    url(r"^password/reset/$", account_views.password_reset, name="account_reset_password"),
    url(r"^password/reset/done/$", account_views.password_reset_done, name="account_reset_password_done"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", account_views.password_reset_from_key, name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$", account_views.password_reset_from_key_done, name="account_reset_password_from_key_done"),

    # # profiles...
    url(r"^profile/(?P<username>.+)/$", q_profile, name="account_profile"),
    url(r"^profile/$", q_profile, name="account_profile"),
]

for provider in providers.registry.get_list():
    try:
        provider_module= import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(provider_module, 'urlpatterns', None)
    if prov_urlpatterns:
        account_urls += prov_urlpatterns

urlpatterns = [

    # ORDER IS IMPORTANT !!!

    # TODO: THIS IS A SECURITY RISK !
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

    # some low-level 3rd party templates have hard-coded the location of "favicon"; this pattern reroutes it correctly
    url(r'^favicon.ico$', serve, {
        'document_root': "{0}questionnaire/images/".format(settings.STATIC_ROOT),
        'path': 'favicon.ico',
    }),

    # admin...
    url(r'^admin/', admin.site.urls),

    # 3rd-party authentication...
    url(r'^accounts/', include(account_urls)),
    # url(r'^accounts/', include('allauth.urls')),

    # mindmaps app...
    url(r'^mindmaps/', include('mindmaps.urls')),

    # questionnaire app...
    url(r'', include('questionnaire.q_urls')),

]

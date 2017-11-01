from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from Q.questionnaire.views.services.views_services_base import validate_request

# just a simple wrapper for the django_allauth confirmation system
# usually, it is invoked via signals from user creation, etc.
# but I want to be able to explicitly re-send it
# hence this fn...


def q_send_email_confirmation(request):
    valid_request, msg = validate_request(request)
    if not valid_request:
        return HttpResponseForbidden(msg)

    username = request.POST.get("username")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        msg = "Unable to locate user '{0}'.".format(username)
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseBadRequest(msg)

    current_user = request.user
    if not current_user.is_superuser and current_user.username != username:
        msg = "You do not have authority to validate this user's email."
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseBadRequest(msg)

    try:
        send_email_confirmation(request, user)
    except Exception as e:
        msg = "Error sending confirmation email."
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseBadRequest(msg)

    return JsonResponse({})

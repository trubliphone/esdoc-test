####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from Q.questionnaire.views.services.views_services_base import validate_request
import Q.questionnaire.q_utils as q_utils


# this is mostly used for asynchronous validation w/ Angular
# synchronous validation can all be done on the client

def q_validate(request):

    valid_request, msg = validate_request(request)
    if not valid_request:
        return HttpResponseForbidden(msg)

    old_value = request.POST.get('old_value')
    new_value = request.POST.get('new_value')
    validator_name = request.POST.get('validator')
    if not validator_name:
        msg = "missing validator name"
        return HttpResponseBadRequest(msg)
    try:
        validator = getattr(q_utils, validator_name)
    except AttributeError:
        msg = "invalid validator name"
        return HttpResponseBadRequest(msg)

    try:
        is_valid = validator(new_value)
        if is_valid is not False:
            return JsonResponse(True, safe=False)
    except ValidationError:
        pass
    return JsonResponse(False, safe=False)

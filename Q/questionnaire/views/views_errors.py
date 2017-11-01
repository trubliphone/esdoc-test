####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

from django.shortcuts import render

from Q.questionnaire import q_logger


def q_error(request, error_msg="", status_code=400):

    #  print error_msg...
    q_logger.error(error_msg)

    # gather all the extra information required by the template...
    context = {
        "error_msg": error_msg,
        "status_code": status_code,
    }

    return render(request, "questionnaire/q_error.html", context=context, status=status_code)


# def q_400(request):
#     context = {
#         "error_msg": "bad request",
#     }
#     return render(request, "questionnaire/q_error.html", context=context, status=400)
#
#
# def q_403(request):
#     context = {
#         "error_msg": "permission_denied",
#     }
#     return render(request, "questionnaire/q_error.html", context=context, status=403)


def q_404(request):
    context = {}
    return render(request, "questionnaire/q_404.html", context=context, status=404)


def q_500(request):
    context = {}
    return render(request, "questionnaire/q_500.html", context=context, status=404)



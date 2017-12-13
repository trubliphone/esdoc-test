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
from Q.questionnaire.views.views_base import add_parameters_to_context


def q_index(request):

    # context = add_parameters_to_context(request)

    read_only = False

    context = {
        "read_only": read_only,
    }

    return render(request, 'questionnaire/q_index.html', context)


def q_test(request):

    # context = add_parameters_to_context(request)

    context = {}
    return render(request, 'questionnaire/q_test.html', context)

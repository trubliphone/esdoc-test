####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2016 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

"""
stand-alone script to obfuscate sensitive parameters used in the Questionnaire configuration file
"""

import os, sys, django

project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Q")
sys.path.append(project_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Q.settings")
django.setup()

from Q.questionnaire.q_utils import encode_parameter


def usage():
    """
    print usage instructions
    :return: usage string
    """
    print(u"usage: %s \"<string to encode>\"" % sys.argv[0])


if len(sys.argv) != 2:
    usage()
    sys.exit(2)

string = sys.argv[1]
encoded_string = encode_parameter(string)
print(encoded_string)

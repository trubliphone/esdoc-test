####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################


from django.contrib import admin

from Q.questionnaire.models.models_institutes import QInstitute
from Q.questionnaire.models.models_test import QTestPostgresModel

admin.site.register(QInstitute)
admin.site.register(QTestPostgresModel)
# admin.site.register(QTestMongodbModel)

# note the relative imports; this is to prevent loading __init__.py twice
from .admin_projects import *
from .admin_sites import *
from .admin_user import *


from django.apps import AppConfig
from django.conf import settings


import json

from Q.questionnaire import APP_LABEL


class QConfig(AppConfig):
    name = APP_LABEL
    verbose_name = "Questionnaire Application"

    def ready(self):
        """
        put code that ought to run only once here...
        :return: None
        """

        from Q.questionnaire.q_constants import PROFANITIES_LIST

        # don't want naughty words in the questionnaire...
        with open(settings.STATIC_ROOT + APP_LABEL + "/profanities.json", 'r') as file:
            profanities = json.load(file)
            [PROFANITIES_LIST.append(p) for p in profanities if p not in PROFANITIES_LIST]
        file.closed

        # connect signal receivers...
        import Q.questionnaire.signals

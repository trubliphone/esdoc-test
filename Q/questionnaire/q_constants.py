####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

# pre-defined string lengths...
TINY_STRING = 64
LIL_STRING = 128
SMALL_STRING = 256
BIG_STRING = 512
HUGE_STRING = 1024

CARDINALITY_INFINITE = 'N'
CARDINALITY_MIN_CHOICES = [(str(i), str(i)) for i in range(0, 11)]
CARDINALITY_MAX_CHOICES = [(CARDINALITY_INFINITE, CARDINALITY_INFINITE)] + [(str(i), str(i)) for i in range(0, 11)]

# minimum password length...
MIN_PASSWORD_LENGTH = 6

# just use the default cache; don't get fancy...
CACHE_ALIAS = "default"

# at what point should suggested text be triggered...
TYPEAHEAD_LIMIT = 6

# a cipher key for encoding / decoding sensitive parameters
# (this is not real security, it just prevents users from having to store plain-text passwords in config files)
# (which would be unwise for tutorials, screen-sharing, etc.)

CIPHER_KEY = "q_JVE8kOU2Ei3C6Z"

# valid reasons to leave a property value blank (taken from seeGrid)...

NIL_PREFIX = "nil"
NIL_REASONS = [
    ("Unknown", "The correct value is not known, and not computable by, the sender of this data.  However, a correct value probably exists."),
    ("Missing", "The correct value is not readily available to the sender of this data. Furthermore, a correct value may not exist."),
    ("Inapplicable", "There is no value."),
    ("Template", "The value will be available later."),
    ("Withheld", "The value is not divulged."),
]

# naughty words...
# (these are stored in an external file and loaded at startup in "apps.py")
PROFANITIES_LIST = []

# cannot have projects w/ these names...
# (else the URLs won't make sense)
RESERVED_WORDS = [
    "admin", "static", "media",
    # "user", "profile", "login", "logout", "register",
    "accounts", "google", "gitub",
    "questionnaire", "mindmaps", "metadata", "legacy",
    "customize", "edit", "view", "help",
    "api", "services",
    "test", "bak",
]


from collections import OrderedDict

SUPPORTED_DOCUMENTS = OrderedDict([
    # this is a slightly convoluted way to define a dictionary,
    # but I have to initialize it w/ a list in order to preserve order
    # (as per http://stackoverflow.com/a/15733571/1060339)
    ("citation", {
        "name": "citation",
        "title": "Citation",
        "type": "cim.2.shared.Citation",
        "category": None,
        "is_active": False,
    }),
    ("conformance", {
        "name": "conformance",
        "title": "Conformance",
        "type": "cim.2.activity.Conformance",
        "category": None,
        "is_active": False,
    }),
    ("ensemble", {
        "name": "ensemble",
        "title": "Ensemble",
        "type": "cim.2.activity.Ensemble",
        "category": None,
        "is_active": False,
    }),
    ("party", {
        "name": "party",
        "title": "Responsible Party",
        "type": "cim.2.shared.Party",
        "category": None,
        "is_active": False,
    }),
    ("machine", {
        "name": "machine",
        "title": "Machine",
        "type": "cim.2.platform.Machine",
        "category": None,
        "is_active": False,
    }),
    ("model", {
       "name": "model",
        "title": "Top-Level Model",
        "category": "Models",
        "is_active": False,
    }),
    ("ocean", {
        "name": "ocean",
        "title": "Ocean",
        "category": "Models",
        "is_active": False,
    }),
    ("seaice", {
        "name": "seaice",
        "title": "Sea Ice",
        "category": "Models",
        "is_active": False,
    }),
    ("performance", {
        "name": "performance",
        "title": "Performance",
        "type": "cim.2.platform.Performance",
        "category": None,
        "is_active": False,
    }),
    ("project", {
        "name": "project",
        "title": "Project",
        "type": "cim.2.designing.Project",
        "category": None,
        "is_active": True,
    }),
])

##################################
# Publication-specific constants #
##################################

PUBLICATION_SOURCE = "questionnaire"

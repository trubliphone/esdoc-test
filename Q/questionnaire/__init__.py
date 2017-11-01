import logging

###########################
# what is the app called? #
###########################

APP_LABEL = "questionnaire"
default_app_config = 'questionnaire.apps.QConfig'


###################################
# which dbs are models stored in? #
###################################

MONGO_DB_MODELS = [
    "QTestMongodbModel",
]


class QRouter(object):
    """
    A router to control all database operations for CIM Documents
    (these are stored in MongoDB)
    """

    def db_for_read(self, model, **hints):
        if model.__name__.lower() in [mdb.lower() for mdb in MONGO_DB_MODELS]:
            # use the special (mongo) db...
            return "documents"
        else:
            # use the default (postgres) db...
            return None

    def db_for_write(self, model, **hints):
        if model.__name__.lower() in [mdb.lower() for mdb in MONGO_DB_MODELS]:
            # use the special (mongo) db...
            return "documents"
        else:
            # use the default (postgres) db...
            return None

    def allow_relation(self, obj1, obj2, **hints):
        import ipdb;
        ipdb.set_trace()
        return None
        if obj1._meta.app_label == 'auth' and obj2._meta.app_label == 'auth':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name.lower() in [mdb.lower() for mdb in MONGO_DB_MODELS]:
            import ipdb; ipdb.set_trace
        return None
        if app_label == 'auth':
            return db == 'documents'
        return None

#########################
# where do messages go? #
#########################

q_logger = logging.getLogger(APP_LABEL)

####################################
# what version is the app/project? #
####################################

__version_info__ = {
    'major': 0.18,
    'minor': 0,
    'patch': 0,
}


def get_version():
    version = ".".join(str(value) for value in __version_info__.values())
    return version


__version__ = get_version()


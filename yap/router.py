import logging

logger = logging.getLogger(__name__)

class APIRouter(object):
    """
    Router for access to API DB
    """
    def db_for_read(self, model, **hints):
        """
        API models to yte_1_cl_test_db_1
        """
        if ((model._meta.app_label == 'location') or
                (model._meta.app_label == 'manual_override') or
                (model._meta.app_label == 'notification') or
                (model._meta.app_label == 'report') or
                (model._meta.app_label == 'search') or
                (model._meta.app_label == 'stream') or
                (model._meta.app_label == 'users') or
                (model._meta.app_label == 'yap')):
            return 'yte_1_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        API models to api_db
        """
        if model._meta.app_label == 'yap':
            return 'yte_1_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relation into databases, no between
        """
        if ((obj1._meta.app_label == 'location') or
                (obj1._meta.app_label == 'manual_override') or
                (obj1._meta.app_label == 'notification') or
                (obj1._meta.app_label == 'report') or
                (obj1._meta.app_label == 'search') or
                (obj1._meta.app_label == 'stream') or
                (obj1._meta.app_label == 'users') or
                (obj1._meta.app_label == 'yap')) and ((obj2._meta.app_label == 'location') or
                                                           (obj2._meta.app_label == 'manual_override') or
                                                           (obj2._meta.app_label == 'notification') or
                                                           (obj2._meta.app_label == 'report') or
                                                           (obj2._meta.app_label == 'search') or
                                                           (obj2._meta.app_label == 'stream') or
                                                           (obj2._meta.app_label == 'users') or
                                                           (obj2._meta.app_label == 'yap')):
            return True
        elif 'mains' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_syncdb(self, db, model):
        """
        Syncdb used only for Default DB
        """
        if db == 'yte_1_db':
            return False
        elif ((model._meta.app_label == 'location') or
                  (model._meta.app_label == 'manual_override') or
                  (model._meta.app_label == 'notification') or
                  (model._meta.app_label == 'report') or
                  (model._meta.app_label == 'search') or
                  (model._meta.app_label == 'stream') or
                  (model._meta.app_label == 'users') or
                  (model._meta.app_label == 'yap')):
            return False
        return None

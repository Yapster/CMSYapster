
class APIRouter(object):
    """
    Router for access to API DB
    """
    def db_for_read(self, model, **hints):
        """
        API models to api_db
        """
        if model._meta.app_label == 'api':
            return 'api_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        API models to api_db
        """
        if model._meta.app_label == 'api':
            return 'api_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relation into databases, no between
        """
        if obj1._meta.app_label == 'api' and obj2._meta.app_label == 'api':
            return True
        elif 'api' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_syncdb(self, db, model):
        """
        Syncdb used only for Default DB
        """
        if db == 'api' or model._meta.app_label == "api":
            return False
        else:
            return True

# dj
from django.conf import settings


class DJSMSConf(object):
    """DJSMS Conf"""

    @property
    def django_q_installed(self):
        return "django_q" in settings.INSTALLED_APPS


djsms_conf = DJSMSConf()

# dj
from django.utils.functional import classproperty

# internal
from .backends.base import BaseBackend
from .errors import SMSBackendDoesNotExistError


class SMSManager(object):
    """SMSManager"""

    @classproperty
    def backends(cls) -> list:
        from .backends import BACKENDS

        return BACKENDS

    @classproperty
    def backends_as_choices(cls):
        return ((backend.identifier, backend.label) for backend in cls.backends)

    @classmethod
    def get_backend_class(cls, identifier: str):
        for backend in cls.backends:
            if identifier == backend.identifier:
                return backend
        raise SMSBackendDoesNotExistError

    def get_backend(self, identifier: str, config: dict | None = None) -> BaseBackend:
        backend_class = self.get_backend_class(identifier)
        return backend_class(config)

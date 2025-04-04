# standard
from typing import Any, List

# internal
from ..models import Message


class BaseBackend(object):
    """Base Backend"""

    identifier = "base"
    label = "Base"

    def __init__(self, config: dict | None = None) -> None:
        if config is None:
            config = {}
        self._config = self.validate_config(config)

    @staticmethod
    def validate_config(config: dict) -> dict:
        return config

    def _get_config(self, name: str, default: Any = None) -> Any:
        return self._config.get(name, default)

    def send(self, text: str, to: str, **kwargs: Any) -> Message:
        raise NotImplementedError

    def send_bulk(self, text: str, to: List[str], **kwargs: Any) -> Message:
        raise NotImplementedError

    def send_schedule(
        self,
        text,
        to: str,
        year: int,
        month: int,
        day: int,
        hours: int,
        minutes: int,
        **kwargs: Any,
    ) -> Message:
        raise NotImplementedError

    def send_pattern(
        self, name: str, to: str, args: List[str], **kwargs: Any
    ) -> Message:
        raise NotImplementedError

    def send_multiple(
        self, texts: List[str], recipients: List[str], **kwargs: Any
    ) -> Message:
        raise NotImplementedError

    def get_credit(self) -> int:
        raise NotImplementedError

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"Backend(identifier={self.identifier}, label={self.label})"

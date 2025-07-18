# standard
from typing import Any, List

# internal
from .. import request
from ..models import Message
from .base import BaseBackend
from ..errors import SMSImproperlyConfiguredError


BASE_URL = "https://edge.ippanel.com/v1"


class IPPanel(BaseBackend):
    """IP Panel"""

    identifier = "ippanel"
    label = "IPPanel"

    @staticmethod
    def validate_config(config: dict) -> dict:

        return config

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

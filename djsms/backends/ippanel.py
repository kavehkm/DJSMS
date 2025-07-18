# standard
import re
from typing import Any, List, Dict

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
        token = config.get("token")
        from_number = config.get("from")
        # validate token
        if not token or not isinstance(token, str):
            raise SMSImproperlyConfiguredError("Invalid token.")
        # validate from_number
        if not from_number or not isinstance(from_number, str) or not re.match(r"^\+98\d+$", from_number):
            raise SMSImproperlyConfiguredError("Invalid from number.")

        # return validated config
        return config

    @property
    def token(self) -> str:
        return self._get_config("token")

    @property
    def from_number(self):
        return self._get_config("from")

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

    def _send_message(self, text: str, recipient: str, url: str, **kwargs) -> Message:
        return request.send_message(text, recipient, url, headers=self.headers, **kwargs)

    @staticmethod
    def get_url(path):
        return "{base_url}/{path}".format(base_url=BASE_URL, path=path)

    def send(self, text: str, to: str, **kwargs: Any) -> Message:
        url = self.get_url("/api/send")
        data = {
            "sending_type": "webservice",
            "from_number": self.from_number,
            "message": text,
            "params": {
                "recipients": [to]
            }
        }
        return self._send_message(text, to, url, json=data)

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
        url = self.get_url("/api/payment/credit/mine")
        res = request.get(url, headers=self.headers).json()
        remain_credit = res["data"]["credit"]
        return int(remain_credit)

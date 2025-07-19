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
        patterns = config.get("patterns")
        # validate token
        if not token or not isinstance(token, str):
            raise SMSImproperlyConfiguredError("Invalid token.")
        # validate from_number
        if not from_number or not isinstance(from_number, str) or not re.match(r"^\+98\d+$", from_number):
            raise SMSImproperlyConfiguredError("Invalid from number.")
        # validate patterns
        if patterns is not None:
            if not isinstance(patterns, list):
                raise SMSImproperlyConfiguredError("Invalid patterns.")
            for pattern in patterns:
                if not isinstance(pattern, dict) or not all(
                    key in pattern for key in ("code", "name", "body")
                ):
                    raise SMSImproperlyConfiguredError("Invalid patterns")
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
        url = self.get_url("/api/send")
        data = {
            "sending_type": "webservice",
            "from_number": self.from_number,
            "message": text,
            "params": {
                "recipients": to
            }
        }
        return self._send_message(text, ",".join(to), url, json=data)

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
        # get url
        url = self.get_url("/api/send")
        # try to find seconds from kwargs
        seconds = kwargs.get("seconds", 0)
        # clean month
        if len(str(month)) == 1:
            month = f"0{month}"
        # clean day
        if len(str(day)) == 1:
            day = f"0{day}"
        # clean hours
        if len(str(hours)) == 1:
            hours = f"0{hours}"
        # clean minutes
        if len(str(minutes)) == 1:
            minutes = f"0{minutes}"
        # clean seconds
        if len(str(seconds)) == 1:
            seconds = f"0{seconds}"
        # prepare request body
        data = {
            "sending_type": "webservice",
            "from_number": self.from_number,
            "message": text,
            "params": {
                "recipients": [to]
            },
            "send_time": f"{year}-{month}-{day} {hours}:{minutes}:{seconds}"
        }
        # send message
        return self._send_message(text, to, url, json=data)

    def send_pattern(
        self, name: str, to: str, args: List[str], **kwargs: Any
    ) -> Message:

        raise NotImplementedError

    def send_multiple(
        self, texts: List[str], recipients: List[str], **kwargs: Any
    ) -> Message:
        # get url
        url = self.get_url("/api/send")
        # check length of texts and recipients
        if len(texts) != len(recipients):
            raise SMSImproperlyConfiguredError("length of texts and recipients must be same.")
        # create params base on ippanel acceptable format
        params = [
            {
                "recipients": [recipients[item_index]],
                "message": texts[item_index]
            }
            for item_index in range(len(texts))
        ]
        # prepare request body
        data = {
            "sending_type": "peer_to_peer",
            "from_number": self.from_number,
            "params": params
        }
        return self._send_message(",".join(texts), ",".join(recipients), url, json=data)

    def get_credit(self) -> int:
        url = self.get_url("/api/payment/credit/mine")
        res = request.get(url, headers=self.headers).json()
        remain_credit = res["data"]["credit"]
        return int(remain_credit)

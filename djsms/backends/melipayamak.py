# standard
from typing import Any, List

# requests
import requests

# internal
from .base import BaseBackend


BASE_URL = "https://console.melipayamak.com/api"


class MeliPayamak(BaseBackend):
    """Meli Payamak"""

    @property
    def token(self) -> str:
        return self._get_config("token")

    def get_url(self, path: str) -> str:
        return f"{BASE_URL}/{path}/{self.token}"

    def get_from(self, kwargs: Any) -> str:
        return kwargs.get("from", self._get_config("from"))

    def get_udh(self, kwargs: Any) -> str:
        return kwargs.get("udh", self._get_config("udh", ""))

    def send(self, text: str, to: str, **kwargs: Any) -> dict:
        url = self.get_url("send/simple")
        data = {"text": text, "to": to, "from": self.get_from(kwargs)}
        res = requests.post(url, json=data)
        return res.json()

    def send_bulk(self, text: str, to: List[str], **kwargs: Any) -> dict:
        url = self.get_url("send/advanced")
        data = {
            "text": text,
            "to": to,
            "from": self.get_from(kwargs),
            "udh": self.get_udh(kwargs),
        }
        res = requests.post(url, json=data)
        return res.json()

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
    ) -> dict:
        url = self.get_url("send/schedule")
        data = {
            "message": text,
            "from": self.get_from(kwargs),
            "to": to,
            "data": f"{month}/{day}/{year} {hours}:{minutes}",
        }
        # check for period
        if "period" in kwargs:
            data["period"] = kwargs["period"]
        res = requests.post(url, json=data)
        return res.json()

    def send_pattern(
        self, pattern_id: int, to: str, args: List[str], **kwargs: Any
    ) -> dict:
        url = self.get_url("send/shared")
        data = {"bodyId": pattern_id, "to": to, "args": args}
        res = requests.post(url, json=data)
        return res.json()

    def send_multiple(
        self, texts: List[str], recipients: List[str], **kwargs: Any
    ) -> dict:
        url = self.get_url("send/multiple")
        data = {
            "to": recipients,
            "text": texts,
            "from": self.get_from(kwargs),
            "udh": self.get_udh(kwargs),
        }
        res = requests.post(url, json=data)
        return res.json()

    def get_credit(self) -> int:
        url = self.get_url("receive/credit")
        res = requests.get(url)
        return res.json()

    def get_status(self, ids: List[int]) -> dict:
        url = self.get_url("receive/status")
        data = {"recIds": ids}
        res = requests.post(url, json=data)
        return res.json()

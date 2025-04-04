# requests
import requests

# internal
from .models import Message
from .conf import djsms_conf
from .consts import HTTP_200_OK, HTTP_201_CREATED
from .errors import SMSError, SMSImproperlyConfiguredError

# djq
try:
    from django_q.tasks import async_task
except ImportError:
    async_task = None


def req(method: str, url: str, **kwargs) -> requests.Response:
    try:
        res = getattr(requests, method)(url, **kwargs)
    except Exception as e:
        raise SMSError(str(e))
    if res.status_code not in [HTTP_200_OK, HTTP_201_CREATED]:
        raise SMSError()
    return res


def get(url: str, **kwargs) -> requests.Response:
    return req("get", url, **kwargs)


def _post(url: str, **kwargs) -> requests.Response:
    return req("post", url, **kwargs)


def sync_post(url: str, **kwargs) -> Message:
    _post(url, **kwargs)
    # create and return success message
    return Message.objects.create(status=Message.SUCCESS)


def _async_post_hook(task) -> None:
    message = Message.objects.filter(task_id=task.id).first()
    message.status = Message.SUCCESS if task.success else Message.FAILED
    message.save(update_fields=["status"])


def async_post(url: str, **kwargs) -> Message:
    # check django_q installation
    if async_task is None:
        raise SMSImproperlyConfiguredError("django_q did not install.")
    # send async post
    task_id = async_task(_post, url, **kwargs, hook=_async_post_hook)  # noqa
    # create and return pending message with given task_id
    return Message.objects.create(task_id=task_id, status=Message.PENDING)


def post(url: str, **kwargs) -> Message:
    # check for use django_q
    if djsms_conf.use_django_q:
        return async_post(url, **kwargs)
    else:
        return sync_post(url, **kwargs)

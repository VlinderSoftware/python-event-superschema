from jose import jwe
import json
from typing import Callable, Dict

from .get_event_dispatcher import get_event_dispatcher

def get_jwe_event_dispatcher(
    err: Callable[[Dict[str, str]], None],
    handlers: Dict[str, Callable[[dict], None]],
    key: str,
    ) -> Callable[[dict], None]:
    inner_dispatcher = get_event_dispatcher(err, handlers)
    def _dispatch(encrypt_event: str):
        try:
            decrypted_event = json.loads(jwe.decrypt(encrypt_event, key))
            inner_dispatcher(decrypted_event)
        except TypeError:
            err({"error":"InternalError", "message": "TypeError while parsing the event -- unencrypted event?"})
    return _dispatch

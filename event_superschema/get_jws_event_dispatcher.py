from jose import jws
import json
from typing import Callable, Dict

from .get_event_dispatcher import get_event_dispatcher

def get_jws_event_dispatcher(
    err: Callable[[Dict[str, str]], None],
    handlers: Dict[str, Callable[[dict], None]],
    key: str,
    algorithm: str
    ) -> Callable[[str], None]:
    inner_dispatcher = get_event_dispatcher(err, handlers)
    def _dispatch(signed_event: str):
        try:
            decoded_event = json.loads(jws.verify(signed_event, key, algorithm))
            inner_dispatcher(decoded_event)
        except AttributeError:
            err({"error":"InternalError", "message": "AttributeError while parsing the event -- unsigned event?"})
    return _dispatch

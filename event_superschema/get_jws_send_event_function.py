from jose import jws
import json
from typing import Callable, Dict, Optional

from .get_send_event_function import get_send_event_function

def get_jws_send_event_function(
    send:Callable[[str], None],
    pid:str,
    key:str,
    algorithm:str,
    data_preprocessors:Optional[Dict[str, Callable[[dict], None]]]=None
    ) -> Callable[[
    str,Optional[any],Optional[str],Optional[str],Optional[str]],None]:
    def sign_then_send(formatted_event):
        signed_event = jws.sign(formatted_event, key, algorithm=algorithm, headers={"typ": "event"})
        send(signed_event)
    return get_send_event_function(sign_then_send, pid, data_preprocessors)

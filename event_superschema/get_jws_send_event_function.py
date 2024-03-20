from jose import jws
import json
from typing import Callable, Dict

from .get_send_event_function import get_send_event_function

def get_jwe_send_event_function(
    send:Callable[[str], None],
    pid:str,
    data_preprocessors:Optional[Dict[str, Callable[[dict], None]]]=None,
    key:str
    algorithm:str
    ) -> Callable[[
    str,Optional[any],Optional[str],Optional[str],Optional[str]],None]:
    def sign_then_send(formatted_event):
        signed_event = jws.sign(json.dumps(formatted_event), key, algorithm)
        send(signed_event)
    return get_send_event_function(sign_then_send, pid, data_preprocessors)

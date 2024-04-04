from jose import jwe
import json
from typing import Callable, Dict, Optional

from .get_send_event_function import get_send_event_function

def get_jwe_send_event_function(
    send:Callable[[str], None],
    pid:str,
    data_preprocessors:Optional[Dict[str, Callable[[dict], None]]]=None,
    key:str=None,
    algorithm:str='dir',
    encryption:str='A256GCM'
    ) -> Callable[[
    str,Optional[any],Optional[str],Optional[str],Optional[str]],None]:
    def encrypt_then_send(formatted_event):
        encrypted_event = jwe.encrypt(json.dumps(formatted_event), key, algorithm, encryption)
        send(encrypted_event)
    return get_send_event_function(encrypt_then_send, pid, data_preprocessors)

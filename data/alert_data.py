from dataclasses import dataclass
from typing import Literal, Optional

@dataclass
class Alert:

    name: str
    temperature_from: str
    temperature_to: str
    send_sms: bool
    send_email: bool
    locations: Optional[list[Literal["Office"]]]
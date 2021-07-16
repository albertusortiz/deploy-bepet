from typing import Optional

from pydantic import BaseModel

class ZoneRequestModel(BaseModel):
    lat: float
    lon: float
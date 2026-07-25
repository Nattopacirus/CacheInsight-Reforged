from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class PresetBase(BaseModel):
    name: str
    cache_size: int
    block_size: int
    mapping_type: str
    n_way: Optional[int] = None
    replacement_policy: str = "LRU"

    @field_validator('cache_size', 'block_size')
    @classmethod
    def check_power_of_2(cls, v: int) -> int:
        if v <= 0 or (v & (v - 1)) != 0:
            raise ValueError('must be a power of 2')
        return v

class PresetCreate(PresetBase):
    pass

class PresetResponse(PresetBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

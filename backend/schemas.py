from typing import Optional
from pydantic import BaseModel, ConfigDict

# default state
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

# for creating new items
class CreateItem(ItemBase):
    pass

# for reading and receiving the data
class Item(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
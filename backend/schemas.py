from pydantic import BaseModel

# default state
class ItemBase(BaseModel):
    name: str
    description: str = None

# for creating new items
class CreateItem(ItemBase):
    pass

# for reading and receiving the data
class Item(ItemBase):
    id: int

    def Config():
        orm_mode = True
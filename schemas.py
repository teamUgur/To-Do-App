from pydantic import BaseModel

#default state
class ItemBase(Base):
    name: str
    description: str = None

#for creating items
class CreateItem(ItemBase):
    pass

#for reading / recieving item from db
class Item(ItemBase):
    id: int

    class Confiq:
        orm_mode = True
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemBody(BaseModel):
  amount: float
  content: str
  date: str
  type: str

class Item(ItemBody):
  id: str
  item_id: int
  user_id: int
  category_id: int
  class Config:
      orm_mode = True

class ItemCreate(ItemBody):
  user_id: int
  category_id: int

class SuccessMsg(BaseModel):
  message: str

class UserBody(BaseModel):
  email: str
  password: str

class UserInfo(BaseModel):
  id: Optional[str] = None
  email: str

class UserDelete(BaseModel):
  user_id: str

class UserCategoriesBase(BaseModel):
  user_id: str
  category_id: str

class UserCategoriesCreate(UserCategoriesBase):
  pass

class UserCategories(UserCategoriesBase):
  class Config:
    orm_mode = True

class CategoryBody(BaseModel):
  name: str
  user_id: str

class CategoryCreate(CategoryBody):
  pass

class Category(CategoryBody):
  id: str
  class Config:
    orm_mode = True

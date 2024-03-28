from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decouple import config

CSRF_KEY = config('CSRF_KEY')

class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY

class ItemBody(BaseModel):
  amount: float
  content: str
  date: str
  type: str

class Item(ItemBody):
  id: str
  user_id: Optional[str] = None
  category_id: Optional[str] = None
  class Config:
      orm_mode = True

class ItemCreate(ItemBody):
  user_id: Optional[str] = None
  category_id: Optional[str] = None

class SuccessMsg(BaseModel):
  message: str

class UserBody(BaseModel):
  email: str
  password: str

class UserInfo(BaseModel):
  id: Optional[str] = None
  email: str

class UserApiInfo(BaseModel):
  id: str
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

class Csrf(BaseModel):
  csrf_token: str

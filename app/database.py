from decouple import config
from typing import Union
import motor.motor_asyncio
from bson import ObjectId
from auth_utils import AuthJwtCsrf
from fastapi import HTTPException

CONNECTION_STRING = "mongodb://admin:password@mongo:27017/?authSource=admin"

client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
database = client['api']
collection_item = database.item
collection_user = database.user
collection_category = database.category
auth = AuthJwtCsrf()

def item_serializer(item) -> dict:
  return {
    'id': str(item['_id']),
    'amount': item['amount'],
    'date': item['date'],
    'content': item['content'],
    "type": item['type'],
    "user_id": item['user_id'] if 'user_id' in item else '',
    "category_id": item['category_id'] if 'category_id' in item else '',
  }

def user_serializer(user) -> dict:
  return {
    'id': str(user['_id']),
    'email': user['email'],
  }

def category_serializer(category) -> dict:
  return {
    'id': str(category['_id']),
    'name': category['name'],
    'user_id': category['user_id'],
  }

async def db_create_category(data: dict) -> Union[dict, bool]:
  category = await collection_category.insert_one(data)
  new_category = await collection_category.find_one({"_id": category.inserted_id})
  if new_category:
    return category_serializer(new_category)
  return False

async def db_get_categories(user_id: str) -> list:
  categories = []
  for category in await collection_category.find({"user_id": user_id}).to_list(length=100):
    categories.append(category_serializer(category))
  return categories

async def db_get_single_category(id: str, user_id: str) -> Union[dict, bool]:
  category = await collection_category.find_one({"_id": ObjectId(id), "user_id": id})
  if category:
    return category_serializer(category)
  return False

async def db_update_category(id: str, data: dict) -> Union[dict, bool]:
  category = await collection_category.find_one({"_id": ObjectId(id)})
  if category:
    updated_category = await collection_category.update_one(
      {"_id": ObjectId(id)}, {"$set": data}
    )
    if (updated_category.modified_count > 0):
      new_category = await collection_category.find_one({"_id": ObjectId(id)})
      return category_serializer(new_category)
  return False

async def db_delete_category(id: str) -> bool:
  category = await collection_category.find_one({"_id": ObjectId(id)})
  if category:
    deleted_category = await collection_category.delete_one({"_id": ObjectId(id)})
    if (deleted_category.deleted_count > 0):
      return True
  return False

async def db_create_item(data: dict) -> Union[dict, bool]:
  item = await collection_item.insert_one(data)
  new_item = await collection_item.find_one({"_id": item.inserted_id})
  if new_item:
    return item_serializer(new_item)
  return False

async def db_get_items(id: str) -> list:
  items = []
  for item in await collection_item.find({"user_id": id}).to_list(length=100):
    items.append(item_serializer(item))
  return items

async def db_get_single_item(id: str, user_id: str) -> Union[dict, bool]:
  item = await collection_item.find_one({"_id": ObjectId(id), "user_id": id})
  if item:
    return item_serializer(item)
  return False

async def db_update_item(id: str, data: dict) -> Union[dict, bool]:
  item = await collection_item.find_one({"_id": ObjectId(id)})
  if item:
    updated_item = await collection_item.update_one(
      {"_id": ObjectId(id)}, {"$set": data}
    )
    if (updated_item.modified_count > 0):
      new_item = await collection_item.find_one({"_id": ObjectId(id)})
      return item_serializer(new_item)
  return False

async def db_delete_item(id: str) -> bool:
  item = await collection_item.find_one({"_id": ObjectId(id)})
  if item:
    deleted_item = await collection_item.delete_one({"_id": ObjectId(id)})
    if (deleted_item.deleted_count > 0):
      return True
  return False

async def db_signup(data: dict) -> dict:
  email = data.get('email')
  password = data.get('password')
  overlap_user = await collection_user.find_one({'email': email})
  if overlap_user:
    raise HTTPException(status_code=400, detail='そのメールアドレスはすでに登録されています')
  if not password or len(password) < 6:
    raise HTTPException(status_code=400, detail='パスワードが短すぎます')
  user = await collection_user.insert_one({'email': email, 'password': auth.generate_hashed_pw(password)})
  new_user = await collection_user.find_one({'_id': user.inserted_id})
  return user_serializer(new_user)

async def db_get_single_user(email: str) -> dict:
  user = await collection_user.find_one({"email": email})
  if not user:
    raise HTTPException(
      status_code=401, detail='Invalid user'
    )
  return user

async def do_login(data: dict) -> str:
  email = data.get('email')
  password = data.get('password')
  user = await collection_user.find_one({'email': email})
  if not user or not auth.verify_pw(password, user['password']):
    raise HTTPException(
      status_code=401, detail='Invalid email or password'
    )
  token = auth.encode_jwt(user['email'])
  return token

async def delete_user(data: dict) -> dict:
  email = Depends(auth_jwt_csrf.decode_jwt)
  user = data.get('user')
  user_db = await collection_user.find_one({"email": email})
  if user_db and str(user_db["_id"]) == user.user_id:
    await collection_user.delete_one({"_id": user_db["_id"]})
    return {"message": "User deleted successfully"}
  else:
    raise HTTPException(status_code=403, detail="You don't have permission to delete this user")

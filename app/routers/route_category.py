from fastapi import APIRouter
from fastapi import Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Category, CategoryBody, SuccessMsg
from database import db_create_category, db_get_categories, db_get_single_category, db_update_category, db_delete_category, db_get_single_user
from starlette.status import HTTP_201_CREATED
from typing import List
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

@router.post('/api/category', response_model=Category)
async def create_category(request: Request, response: Response, data: CategoryBody):
  category = jsonable_encoder(data)
  res = await db_create_category(category)
  response.status_code = HTTP_201_CREATED
  if res:
    return res
  raise HTTPException(
    status_code=404, detail='categoryの作成に失敗しました'
  )

@router.get('/api/category', response_model=List[Category])
async def get_category(request: Request):
  _, subject = auth.verify_update_jwt(request)
  user = await db_get_single_user(subject)
  res = await db_get_categories(str(user['_id']))
  return res

@router.get("/api/category/{id}", response_model=Category)
async def get_single_category(id: str):
  res = await db_get_single_category(id)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"このカテゴリーは存在しません。"
  )

@router.put("/api/category/{id}", response_model=Category)
async def update_category(id: str, data: CategoryBody):
  category = jsonable_encoder(data)
  res = await db_update_category(id, category)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"このカテゴリーは存在しません。"
  )

@router.delete('/api/category/{id}', response_model=SuccessMsg)
async def deleted_item(id: str):
  res = await db_delete_category(id)
  if res:
    return {'message': 'カテゴリーの削除に成功しました'}
  raise HTTPException(status_code=404, detail='カテゴリーの削除に失敗しました')

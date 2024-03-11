from fastapi import APIRouter
from fastapi import Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Category, CategoryBody, SuccessMsg
from database import db_create_category, db_get_categories, db_get_single_category, db_update_category, db_delete_category
from starlette.status import HTTP_201_CREATED
from typing import List

router = APIRouter()

@router.post('/api/category', response_model=Category)
async def create_item(request: Request, response: Response, data: CategoryBody):
  item = jsonable_encoder(data)
  res = await db_create_category(item)
  response.status_code = HTTP_201_CREATED
  if res:
    return res
  raise HTTPException(
    status_code=404, detail='itemの作成に失敗しました'
  )

@router.get('/api/category', response_model=List[Category])
async def get_items():
  res = await db_get_categories()
  return res

@router.get("/api/category/{id}", response_model=Category)
async def get_single_item(id: str):
  res = await db_get_single_category(id)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"このカテゴリーは存在しません。"
  )

@router.put("/api/category/{id}", response_model=Category)
async def update_item(id: str, data: CategoryBody):
  item = jsonable_encoder(data)
  res = await db_update_category(id, item)
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

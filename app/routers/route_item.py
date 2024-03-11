from fastapi import APIRouter
from fastapi import Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Item, ItemBody, SuccessMsg
from database import db_create_item, db_get_items, db_get_single_item, db_update_item, db_delete_item
from starlette.status import HTTP_201_CREATED
from typing import List

router = APIRouter()

@router.post('/api/item', response_model=Item)
async def create_item(request: Request, response: Response, data: ItemBody):
  item = jsonable_encoder(data)
  res = await db_create_item(item)
  response.status_code = HTTP_201_CREATED
  if res:
    return res
  raise HTTPException(
    status_code=404, detail='itemの作成に失敗しました'
  )

@router.get('/api/item', response_model=List[Item])
async def get_items():
  res = await db_get_items()
  return res

@router.get("/api/item/{id}", response_model=Item)
async def get_single_item(id: str):
  res = await db_get_single_item(id)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"このアイテムは存在しません。"
  )

@router.put("/api/item/{id}", response_model=Item)
async def update_item(id: str, data: ItemBody):
  item = jsonable_encoder(data)
  res = await db_update_item(id, item)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"このアイテムは存在しません。"
  )

@router.delete('/api/item/{id}', response_model=SuccessMsg)
async def deleted_item(id: str):
  res = await db_delete_item(id)
  if res:
    return {'message': 'Successfully deleted'}
  raise HTTPException(status_code=404, detail='アイテムの削除に失敗しました')

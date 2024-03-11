from fastapi import APIRouter
from fastapi import Response, Request
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, UserInfo, SuccessMsg
from database import (
  db_signup,
  do_login
)
router = APIRouter()

@router.post('/api/register', response_model=UserInfo)
async def signup(user: UserBody):
  user = jsonable_encoder(user)
  new_user = await db_signup(user)
  return new_user

@router.post('/api/login', response_model=SuccessMsg)
async def login(response: Response, user: UserBody):
  user = jsonable_encoder(user)
  token = await do_login(user)
  response.set_cookie(
    key="access_token", value=f"Bearer {token}", httponly=True, samesite='none', secure=True
  )
  return {'message': 'ログインに成功しました。'}

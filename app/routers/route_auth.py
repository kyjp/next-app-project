from fastapi import APIRouter
from fastapi import Response, Request, Depends
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, UserInfo, UserApiInfo, SuccessMsg, Csrf
from database import (
  db_signup,
  do_login,
  db_get_single_user,
  db_get_categories
)
from auth_utils import AuthJwtCsrf
from fastapi_csrf_protect import CsrfProtect

router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/register", response_model=UserInfo)
async def signup(request: Request, user: UserBody, csrf_protect: CsrfProtect = Depends()):
  csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
  csrf_protect.validate_csrf(csrf_token)
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

@router.get('/api/user', response_model=UserApiInfo)
async def get_user_refresh_jwt(request: Request, response: Response):
  new_token, subject = auth.verify_update_jwt(request)
  response.set_cookie(
    key="access_token",
    value=f"Bearer {new_token}",
    httponly=True,
    samesite="none",
    secure=True
  )
  user = await db_get_single_user(subject)
  return {"id": str(user["_id"]), "email": subject}

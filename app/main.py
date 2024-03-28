from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import route_item, route_auth, route_category
from schemas import SuccessMsg, CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

app = FastAPI()
app.include_router(route_item.router)
app.include_router(route_auth.router)
app.include_router(route_category.router)
origins = ['http://localhost:3000', 'https://fastapi-1436a.web.app']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(
      status_code=exc.status_code,
      content={'detail':  exc.message}
  )

@app.get('/', response_model=SuccessMsg)
def root():
  return {'message': '成功'}

@app.get('/api/csrf-token')
def generate_csrf_token():
  csrf_token = CsrfProtect().generate_csrf()
  return JSONResponse(content={'csrf_token': csrf_token})

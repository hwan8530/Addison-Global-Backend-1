from fastapi import APIRouter
from python_fastapi.app.schemas.user import Credentials, UserToken
from python_fastapi.app.services.syncservice import SimpleSyncTokenService
from python_fastapi.app.services.asyncservice import SimpleAsyncTokenService

router = APIRouter(prefix="/api/v1")
async_token_service = SimpleAsyncTokenService(None, None)
sync_token_service = SimpleSyncTokenService()


@router.post("/token", response_model=UserToken, status_code=200)
def sync_request_token(credential: Credentials) -> UserToken:
  return sync_token_service.request_token(credential)

@router.post("/atoken", response_model=UserToken, status_code=200)
async def async_request_token(credential: Credentials) -> UserToken|None:
  return await async_token_service.request_token(credential)
import asyncio
from fastapi import HTTPException
from python_fastapi.app.schemas.user import Credentials, User, UserToken
import random
import datetime

# 서비스 공통 상수
DELAY_MIN_MS=0
DELAY_MAX_MS=5000

class AsyncAuthentication :
  """비동기 인증 서비스
  
  Credentials를 검증하여 User 인스턴스를 반환합니다.
  0~5000ms의 랜덤 지연을 포함합니다.
  """
  
  async def authenticate(self, credential: Credentials) -> User :
    self._validate_credentials(credential)
    await self._apply_delay()
    return User(userid=credential.username)

  # password 검증 (username uppercase와 비교)
  def _validate_credentials(self, credential: Credentials) -> None:
    if credential.username.upper() != credential.password :
      raise HTTPException(status_code=401, detail="Incorrect username or password")

  # 0 ~ 5000 밀리초 랜덤 지연
  async def _apply_delay(self) -> None:
    random_ms = random.randint(DELAY_MIN_MS, DELAY_MAX_MS)
    await asyncio.sleep(random_ms / 1000)

class AsyncToken:
  """비동기 토큰 발급 서비스
  
  User에 대한 UserToken을 발급합니다.
  'A'로 시작하는 userid는 필터링합니다.
  0~5000ms의 랜덤 지연을 포함합니다.
  """
  
  async def issue_token(self, user:User) -> UserToken:
    self._validate_user(user)
    await self._apply_delay()
    return self._generate_token(user)

  # Userid 검증 ('A'로 시작하면 실패)
  def _validate_user(self, user: User) -> None:
    if user.userid.startswith("A"):
      raise HTTPException(status_code=403, detail="Incorrect username")

  # 0 ~ 5000 밀리초 랜덤 지연
  async def _apply_delay(self) -> None:
    random_ms = random.randint(DELAY_MIN_MS, DELAY_MAX_MS)
    await asyncio.sleep(random_ms / 1000)

  # 토큰 생성
  def _generate_token(self, user: User) -> UserToken:
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d'T'%H:%M:%S.%f")[:-3]
    return UserToken(token=user.userid+"_"+formatted_datetime)

class SimpleAsyncTokenService:
  """통합 비동기 토큰 요청 서비스 (README 요구사항 3번)
  
  인증과 토큰 발급을 순차적으로 처리합니다:
  1. authenticate() → User 획득
  2. issue_token() → UserToken 발급
  3. UserToken 반환
  
  여러 요청을 동시에 처리할 수 있습니다.
  """
  
  def __init__(
      self,
      auth_service:AsyncAuthentication|None,
      token_service:AsyncToken|None
  ):
    self._auth_service = auth_service or AsyncAuthentication()
    self._token_service = token_service or AsyncToken()

  async def request_token(self, credential: Credentials) -> UserToken|None:
    user = await self._auth_service.authenticate(credential)
    return await self._token_service.issue_token(user)

from fastapi import HTTPException
from python_fastapi.app.schemas.user import Credentials, User, UserToken
import random
import time
import datetime

# 서비스 공통 상수
DELAY_MIN_MS=0
DELAY_MAX_MS=5000

class SyncAuthentication:
  """동기 인증 서비스
  
  Credentials를 검증하여 User 인스턴스를 반환합니다.
  0~5000ms의 랜덤 지연을 포함합니다.
  """
  
  def authenticate(self, credential: Credentials) -> User :
    self._validate_credentials(credential)
    self._apply_delay()
    return User(userid=credential.username)

  # password 검증 (username uppercase와 비교)
  def _validate_credentials(self, credential: Credentials) -> None:
    if credential.username.upper() != credential.password :
      raise HTTPException(status_code=401, detail="Incorrect username or password")

  # 0 ~ 5000 밀리초 랜덤 지연
  def _apply_delay(self) -> None:
    random_ms = random.randint(DELAY_MIN_MS, DELAY_MAX_MS)
    time.sleep(random_ms / 1000)

class SyncToken:
  """동기 토큰 발급 서비스
  
  User에 대한 UserToken을 발급합니다.
  'A'로 시작하는 userid는 필터링합니다.
  0~5000ms의 랜덤 지연을 포함합니다.
  """
  
  def issue_token(self, user: User) -> UserToken :
    self._validate_user(user)
    self._apply_delay()
    return self._generate_token(user)

  # Userid 검증 ('A'로 시작하면 실패)
  def _validate_user(self, user: User) -> None:
    if user.userid.startswith("A"):
      raise HTTPException(status_code=403, detail="Incorrect username")

  # 0 ~ 5000 밀리초 랜덤 지연
  def _apply_delay(self) -> None:
    random_ms = random.randint(DELAY_MIN_MS, DELAY_MAX_MS)
    time.sleep(random_ms / 1000)

  # 토큰 생성
  def _generate_token(self, user : User) -> UserToken:
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d'T'%H:%M:%S.%f")[:-3]
    user_token = UserToken(token=user.userid+"_"+formatted_datetime)
    return user_token

class SimpleSyncTokenService:
  """통합 동기 토큰 요청 서비스 (README 요구사항 3번)
  
  인증과 토큰 발급을 순차적으로 처리합니다:
  1. authenticate() → User 획득
  2. issue_token() → UserToken 발급
  3. UserToken 반환
  """
  
  def __init__(self):
    self._auth_service = SyncAuthentication()
    self._token_service = SyncToken()

  def request_token(self, credential: Credentials) -> UserToken:
    user = self._auth_service.authenticate(credential)
    return self._token_service.issue_token(user)

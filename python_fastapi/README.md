# FAST API README

SimpleAsyncTokenService는 모두 비동기 서비스로 이뤄져있으며 TestCode는 copilot을 통해 작성했음.

## 동시성 처리 (Concurrency)

### 비동기 구현
- `AsyncAuthenticationService`와 `AsyncTokenService`는 완전히 비동기입니다
- `asyncio.sleep()`을 사용하여 블로킹 없이 대기합니다
- 여러 요청이 동시에 처리될 수 있습니다

### 테스트 예제
```python
import asyncio
from app.services.asyncservice import SimpleAsyncTokenService
from app.schemas.user import Credentials

async def concurrent_requests():
    service = SimpleAsyncTokenService()
    
    # 5개의 요청을 동시에 처리
    tasks = [
        service.request_token(Credentials(username=f"user{i}", password=f"USER{i}"))
        for i in range(5)
    ]
    
    tokens = await asyncio.gather(*tasks)
    return tokens  # 약 5~10초 (순차가 아니라 병렬 처리)
```

## 내결함성(Fault Tolerance)

별도 미구현

- DB 등 외부와 연결되는 포인트가 없어 retry 및 timeout 불필요하다고 판단
- 단순히 검증만 거치는 서비스가 아닌 실제 데이터를 저장해두고 확인하는 서비스라면 DB Connection 실패나 timeout에 대한 별도 처리 필요
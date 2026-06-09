from fastapi.testclient import TestClient
from .main import app
from .schemas.user import Credentials, User, UserToken
from .services import asyncservice, syncservice
import pytest
import re
import asyncio

from .services.syncservice import SyncAuthentication, SyncToken, SimpleSyncTokenService
from .services.asyncservice import AsyncAuthentication, AsyncToken, SimpleAsyncTokenService

client = TestClient(app)
sync_auth = SyncAuthentication()
sync_token = SyncToken()
sync_token_service = SimpleSyncTokenService()
async_auth = AsyncAuthentication()
async_token = AsyncToken()
async_token_service = SimpleAsyncTokenService(None, None)
# ============ Sync Service Tests ============

class TestSyncService:
    """Sync service 테스트"""
    
    def test_authenticate_valid_credentials(self):
        """유효한 credentials으로 user 반환"""
        cred = Credentials(username="house", password="HOUSE")
        user = sync_auth.authenticate(cred)
        assert user.userid == "house"
    
    def test_authenticate_invalid_password(self):
        """잘못된 비밀번호로 401 에러 반환"""
        cred = Credentials(username="house", password="House")
        with pytest.raises(Exception):
            sync_auth.authenticate(cred)
    
    def test_authenticate_empty_username(self):
        """빈 username으로 유효하지 않은 credentials"""
        cred = Credentials(username="", password="")
        user = sync_auth.authenticate(cred)
        assert user.userid == ""
    
    def test_authenticate_case_sensitive(self):
        """비밀번호가 대소문자 구분"""
        cred = Credentials(username="test", password="test")
        with pytest.raises(Exception):
            sync_auth.authenticate(cred)
    
    def test_issue_token_valid_user(self):
        """유효한 user로 token 발급"""
        user = User(userid="house")
        token = sync_token.issue_token(user)
        
        # 토큰 포맷 검증: userid_YYYY-MM-DD'T'HH:MM:SS.mmm
        assert "house_" in token.token
        assert re.match(r"house_\d{4}-\d{2}-\d{2}'T'\d{2}:\d{2}:\d{2}\.\d{3}", token.token)
    
    def test_issue_token_user_starts_with_a(self):
        """'A'로 시작하는 userid는 토큰 발급 실패"""
        user = User(userid="Alice")
        with pytest.raises(Exception):
            sync_token.issue_token(user)
    
    def test_issue_token_user_starts_with_lowercase_a(self):
        """'a'로 시작하는 userid는 성공"""
        user = User(userid="apple")
        token = sync_token.issue_token(user)
        assert "apple_" in token.token
    
    def test_request_token_success(self):
        """성공 케이스: credentials로 token 발급"""
        cred = Credentials(username="house", password="HOUSE")
        token = sync_token_service.request_token(cred)
        
        assert isinstance(token, UserToken)
        assert "house_" in token.token
        assert re.match(r"house_\d{4}-\d{2}-\d{2}'T'\d{2}:\d{2}:\d{2}\.\d{3}", token.token)
    
    def test_request_token_invalid_credentials(self):
        """실패 케이스: 유효하지 않은 credentials"""
        cred = Credentials(username="house", password="house")
        with pytest.raises(Exception):
            sync_token_service.request_token(cred)
    
    def test_request_token_user_starts_with_a(self):
        """실패 케이스: 'A'로 시작하는 username"""
        cred = Credentials(username="Alice", password="ALICE")
        with pytest.raises(Exception):
            sync_token_service.request_token(cred)


# ============ Async Service Tests ============

class TestAsyncService:
    """Async service 테스트"""
    
    @pytest.mark.asyncio
    async def test_authenticate_valid_credentials(self):
        """유효한 credentials으로 user 반환"""
        cred = Credentials(username="house", password="HOUSE")
        user = await async_auth.authenticate(cred)
        assert user.userid == "house"
    
    @pytest.mark.asyncio
    async def test_authenticate_invalid_password(self):
        """잘못된 비밀번호로 에러 반환"""
        cred = Credentials(username="house", password="House")
        with pytest.raises(Exception):
            await async_auth.authenticate(cred)
    
    @pytest.mark.asyncio
    async def test_authenticate_case_sensitive(self):
        """비밀번호가 대소문자 구분"""
        cred = Credentials(username="test", password="test")
        with pytest.raises(Exception):
            await async_auth.authenticate(cred)
    
    @pytest.mark.asyncio
    async def test_issue_token_valid_user(self):
        """유효한 user로 token 발급"""
        user = User(userid="house")
        token = await async_token.issue_token(user)
        
        assert "house_" in token.token
        assert re.match(r"house_\d{4}-\d{2}-\d{2}'T'\d{2}:\d{2}:\d{2}\.\d{3}", token.token)
    
    @pytest.mark.asyncio
    async def test_issue_token_user_starts_with_a(self):
        """'A'로 시작하는 userid는 토큰 발급 실패"""
        user = User(userid="Alice")
        with pytest.raises(Exception):
            await async_token.issue_token(user)
    
    @pytest.mark.asyncio
    async def test_issue_token_user_starts_with_lowercase_a(self):
        """'a'로 시작하는 userid는 성공"""
        user = User(userid="apple")
        token = await async_token.issue_token(user)
        assert "apple_" in token.token
    
    @pytest.mark.asyncio
    async def test_request_token_success(self):
        """성공 케이스: credentials로 token 발급"""
        cred = Credentials(username="house", password="HOUSE")
        token = await async_token_service.request_token(cred)
        
        assert isinstance(token, UserToken)
        assert "house_" in token.token
        assert re.match(r"house_\d{4}-\d{2}-\d{2}'T'\d{2}:\d{2}:\d{2}\.\d{3}", token.token)
    
    @pytest.mark.asyncio
    async def test_request_token_invalid_credentials(self):
        """실패 케이스: 유효하지 않은 credentials"""
        cred = Credentials(username="house", password="house")
        with pytest.raises(Exception):
            await async_token_service.request_token(cred)
    
    @pytest.mark.asyncio
    async def test_request_token_user_starts_with_a(self):
        """실패 케이스: 'A'로 시작하는 username"""
        cred = Credentials(username="Alice", password="ALICE")
        with pytest.raises(Exception):
            await async_token_service.request_token(cred)
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """동시성 테스트: 여러 요청이 병렬로 처리"""
        tasks = []
        for i in range(5):
            cred = Credentials(username=f"user{i}", password=f"USER{i}")
            tasks.append(async_token_service.request_token(cred))
        
        tokens = await asyncio.gather(*tasks)
        assert len(tokens) == 5
        for i, token in enumerate(tokens):
            assert f"user{i}_" in token.token


# ============ API Endpoint Tests ============

class TestSyncTokenAPI:
    """동기 토큰 API 엔드포인트 테스트"""
    
    def test_post_token_success(self):
        """POST /api/v1/token 성공"""
        response = client.post("/api/v1/token", json={
            "username": "house",
            "password": "HOUSE"
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "house_" in data["token"]
    
    def test_post_token_invalid_credentials(self):
        """POST /api/v1/token 유효하지 않은 credentials"""
        response = client.post("/api/v1/token", json={
            "username": "house",
            "password": "house"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_post_token_user_starts_with_a(self):
        """POST /api/v1/token 'A'로 시작하는 username"""
        response = client.post("/api/v1/token", json={
            "username": "Alice",
            "password": "ALICE"
        })
        assert response.status_code == 403
        assert "Incorrect username" in response.json()["detail"]
    
    def test_post_token_various_usernames(self):
        """POST /api/v1/token 다양한 username 테스트"""
        test_cases = [
            ("john", "JOHN", True),
            ("test123", "TEST123", True),
            ("bob", "BOB", True),
            ("alice", "ALICE", True),  # 소문자 a로 시작하므로 성공
        ]
        
        for username, password, should_succeed in test_cases:
            response = client.post("/api/v1/token", json={
                "username": username,
                "password": password
            })
            if should_succeed:
                assert response.status_code == 200
                assert username in response.json()["token"]
            else:
                assert response.status_code in [401, 403]
    
    def test_post_token_response_format(self):
        """POST /api/v1/token 응답 포맷 검증"""
        response = client.post("/api/v1/token", json={
            "username": "testuser",
            "password": "TESTUSER"
        })
        assert response.status_code == 200
        data = response.json()
        
        # 토큰 포맷 검증
        assert re.match(r"testuser_\d{4}-\d{2}-\d{2}'T'\d{2}:\d{2}:\d{2}\.\d{3}", data["token"])


class TestAsyncTokenAPI:
    """비동기 토큰 API 엔드포인트 테스트"""
    
    def test_post_atoken_success(self):
        """POST /api/v1/atoken 성공"""
        response = client.post("/api/v1/atoken", json={
            "username": "house",
            "password": "HOUSE"
        })
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "house_" in data["token"]
    
    def test_post_atoken_invalid_credentials(self):
        """POST /api/v1/atoken 유효하지 않은 credentials"""
        response = client.post("/api/v1/atoken", json={
            "username": "house",
            "password": "house"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_post_atoken_user_starts_with_a(self):
        """POST /api/v1/atoken 'A'로 시작하는 username"""
        response = client.post("/api/v1/atoken", json={
            "username": "Alice",
            "password": "ALICE"
        })
        assert response.status_code == 403
        assert "Incorrect username" in response.json()["detail"]
    
    def test_post_atoken_various_usernames(self):
        """POST /api/v1/atoken 다양한 username 테스트"""
        test_cases = [
            ("john", "JOHN", True),
            ("test123", "TEST123", True),
            ("bob", "BOB", True),
            ("alice", "ALICE", True),
        ]
        
        for username, password, should_succeed in test_cases:
            response = client.post("/api/v1/atoken", json={
                "username": username,
                "password": password
            })
            if should_succeed:
                assert response.status_code == 200
                assert username in response.json()["token"]
            else:
                assert response.status_code in [401, 403]
    
    def test_post_atoken_response_format(self):
        """POST /api/v1/atoken 응답 포맷 검증"""
        response = client.post("/api/v1/atoken", json={
            "username": "testuser",
            "password": "TESTUSER"
        })
        assert response.status_code == 200
        data = response.json()
        
        assert re.match(r"testuser_\d{4}-\d{2}-\d{2}'T'\d{2}:\d{2}:\d{2}\.\d{3}", data["token"])
    
    def test_post_atoken_multiple_requests(self):
        """POST /api/v1/atoken 여러 요청이 독립적으로 처리됨"""
        responses = []
        for i in range(3):
            response = client.post("/api/v1/atoken", json={
                "username": f"user{i}",
                "password": f"USER{i}"
            })
            responses.append(response)
        
        assert all(r.status_code == 200 for r in responses)
        tokens = [r.json()["token"] for r in responses]
        assert all("user" in token for token in tokens)


# ============ Edge Cases and Error Handling ============

class TestEdgeCases:
    """엣지 케이스 및 에러 처리 테스트"""
    
    def test_empty_username(self):
        """빈 username"""
        response = client.post("/api/v1/token", json={
            "username": "",
            "password": ""
        })
        assert response.status_code == 200
    
    def test_special_characters_in_username(self):
        """특수 문자를 포함한 username"""
        response = client.post("/api/v1/token", json={
            "username": "user-123",
            "password": "USER-123"
        })
        assert response.status_code == 200
        assert "user-123_" in response.json()["token"]
    
    def test_numbers_only_username(self):
        """숫자만으로 이루어진 username"""
        response = client.post("/api/v1/token", json={
            "username": "123456",
            "password": "123456"  # 숫자는 대문자 변환이 없음
        })
        assert response.status_code == 200
    
    def test_long_username(self):
        """긴 username"""
        long_username = "a" * 100
        response = client.post("/api/v1/token", json={
            "username": long_username,
            "password": long_username.upper()
        })
        assert response.status_code == 200
    
    def test_missing_password_field(self):
        """비밀번호 필드 누락"""
        response = client.post("/api/v1/token", json={
            "username": "house"
        })
        assert response.status_code == 422
    
    def test_missing_username_field(self):
        """사용자명 필드 누락"""
        response = client.post("/api/v1/token", json={
            "password": "HOUSE"
        })
        assert response.status_code == 422
    
    def test_extra_fields_ignored(self):
        """추가 필드는 무시됨"""
        response = client.post("/api/v1/token", json={
            "username": "house",
            "password": "HOUSE",
            "extra_field": "ignored"
        })
        assert response.status_code == 200

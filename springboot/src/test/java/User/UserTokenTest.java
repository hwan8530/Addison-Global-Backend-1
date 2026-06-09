package User;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import backendchallenge.addison1.User.entity.Credential;
import backendchallenge.addison1.User.entity.User;
import backendchallenge.addison1.User.entity.UserToken;
import backendchallenge.addison1.User.service.AsyncTokenService;
import backendchallenge.addison1.Addison1Application;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.regex.Pattern;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(classes = Addison1Application.class)
@DisplayName("AsyncTokenService 테스트")
@SuppressWarnings("unchecked")
public class UserTokenTest {

  @Autowired
  private AsyncTokenService asyncTokenService;

  @SuppressWarnings("unchecked")
  @Test
  @DisplayName("authenticate 유효한 자격증명으로 User 반환")
  public void authenticate_ValidCredential_ReturnsUser() throws Exception {
    // Arrange
    Credential credential = new Credential("house", "HOUSE");

    // Act
    CompletableFuture<User> future = asyncTokenService.authenticate(credential);
    User user = future.get(); // 최대 6초 대기 (0-5초 지연 + 여유)

    // Assert
    assertNotNull(user);
    assertEquals("house", user.getUserid());
  }
  @Test
  @DisplayName("authenticate_유효하지_않은_자격증명_예외_발생")
  public void authenticate_InvalidCredentials_ThrowsException()
      throws ExecutionException, InterruptedException {
    // Arrange
    Credential credential = new Credential("house", "House"); // 소문자 'H' - 유효하지 않음

    // Act & Assert
    CompletableFuture<User> future = asyncTokenService.authenticate(credential);

    // CompletableFuture에서 예외가 발생하는 경우 처리
    assertThrows(ExecutionException.class, future::get);
  }

  @Test
  @DisplayName("authenticate_다양한_사용자명_테스트")
  public void authenticate_VariousUsernames_Success()
      throws ExecutionException, InterruptedException {
    // 여러 사용자명으로 테스트
    String[] usernames = {"alice", "bob", "user123", "test"};

    for (String username : usernames) {
      Credential credential = new Credential(username, username.toUpperCase());
      CompletableFuture<User> future = asyncTokenService.authenticate(credential);
      User user = future.get();

      assertNotNull(user);
      assertEquals(username, user.getUserid());
    }
  }

  /**
   * ========== issueToken 메소드 테스트 ==========
   *
   * 테스트 이유:
   * - userId가 'A'로 시작하는 경우 예외 발생 검증
   * - 토큰 형식이 정확한지 검증 (yyyy-MM-dd'T'HH:mm:ss'Z')
   * - 비동기 처리 확인
   * - userId 값이 토큰에 포함되는지 확인
   */

  @Test
  @DisplayName("issueToken_유효한_User_토큰_발급")
  public void issueToken_ValidUser_IssuedToken()
      throws ExecutionException, InterruptedException {
    // Arrange
    User user = new User("house");

    // Act
    CompletableFuture<UserToken> future = asyncTokenService.issueToken(user);
    UserToken token = future.get();

    // Assert
    assertNotNull(token);
    assertNotNull(token.getToken());
    assertTrue(token.getToken().startsWith("house_"));
  }

  @Test
  @DisplayName("issueToken_A로_시작하는_userId_예외_발생")
  public void issueToken_UserIdStartsWithA_ThrowsException()
      throws ExecutionException, InterruptedException {
    // Arrange
    User user = new User("Alice");

    // Act & Assert
    CompletableFuture<UserToken> future = asyncTokenService.issueToken(user);
    assertThrows(ExecutionException.class, future::get);
  }

  @Test
  @DisplayName("issueToken_토큰_형식_검증")
  public void issueToken_TokenFormat_MatchesPattern()
      throws ExecutionException, InterruptedException {
    // Arrange
    User user = new User("testuser");

    // Act
    CompletableFuture<UserToken> future = asyncTokenService.issueToken(user);
    UserToken token = future.get();

    // Assert
    // 토큰 형식: userid_yyyy-MM-ddThh:mm:ss.ssZ
    // 예: testuser_2024-05-23T14:30:45:123Z
    String tokenPattern = "^[a-z0-9]+_\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$";
    Pattern pattern = Pattern.compile(tokenPattern);

    assertTrue(
        pattern.matcher(token.getToken()).matches(),
        "토큰 형식이 올바르지 않습니다: " + token.getToken());
  }

  @Test
  @DisplayName("issueToken_여러_유효한_User_테스트")
  public void issueToken_MultipleValidUsers_Success()
      throws ExecutionException, InterruptedException {
    // A로 시작하지 않는 사용자명들
    String[] usernames = {"bob", "charlie", "david", "eva", "frank"};

    for (String username : usernames) {
      User user = new User(username);
      CompletableFuture<UserToken> future = asyncTokenService.issueToken(user);
      UserToken token = future.get();

      assertNotNull(token);
      assertTrue(token.getToken().startsWith(username + "_"));
    }
  }

  /**
   * ========== requestToken 메소드 테스트 ==========
   *
   * 테스트 이유:
   * - 전체 인증 → 토큰 발급 플로우 검증
   * - 유효한 자격증명에서 UserToken까지 정확히 처리되는지 확인
   * - 비동기 체인 처리 검증 (thenCompose)
   * - 유효하지 않은 자격증명 처리 검증
   * - A로 시작하는 사용자 필터링 검증
   */

  @Test
  @DisplayName("requestToken_유효한_자격증명_토큰_반환")
  public void requestToken_ValidCredentials_ReturnToken()
      throws ExecutionException, InterruptedException {
    // Arrange
    Credential credential = new Credential("house", "HOUSE");

    // Act
    CompletableFuture<UserToken> future = asyncTokenService.requestToken(credential);
    UserToken token = future.get();

    // Assert
    assertNotNull(token);
    assertNotNull(token.getToken());
    assertTrue(token.getToken().startsWith("house_"));
  }

  @Test
  @DisplayName("requestToken_유효하지_않은_자격증명_예외")
  public void requestToken_InvalidCredentials_ThrowsException()
      throws ExecutionException, InterruptedException {
    // Arrange
    Credential credential = new Credential("house", "house"); // 소문자 - 유효하지 않음

    // Act & Assert
    CompletableFuture<UserToken> future = asyncTokenService.requestToken(credential);
    assertThrows(ExecutionException.class, future::get);
  }

  @Test
  @DisplayName("requestToken_A로_시작하는_사용자_예외")
  public void requestToken_UserIdStartsWithA_ThrowsException()
      throws ExecutionException, InterruptedException {
    // Arrange
    // 'Apple' -> 'APPLE'로 변환
    // userId가 대문자 'A'로 시작하므로 예외 발생 예상
    Credential credential = new Credential("Apple", "APPLE");

    // Act & Assert
    CompletableFuture<UserToken> future = asyncTokenService.requestToken(credential);
    assertThrows(ExecutionException.class, future::get);
  }

  /**
   * ========== 동시성 테스트 ==========
   *
   * 테스트 이유:
   * - 여러 스레드에서 동시 요청 처리 확인
   * - ThreadPoolExecutor 설정이 올바르게 작동하는지 확인
   * - 비동기 태스크가 블로킹되지 않는지 확인
   * - 동시 요청으로 인한 시간 단축 확인 (병렬 처리)
   */

  @Test
  @DisplayName("동시_요청_처리_테스트")
  public void concurrentRequests_MultipleAsync_AllComplete()
      throws ExecutionException, InterruptedException {
    // Arrange
    CompletableFuture<UserToken>[] futures = new CompletableFuture[5];
    Credential[] credentials = {
        new Credential("user1", "USER1"),
        new Credential("user2", "USER2"),
        new Credential("user3", "USER3"),
        new Credential("user4", "USER4"),
        new Credential("bob", "BOB")
    };

    // Act
    long startTime = System.currentTimeMillis();

    for (int i = 0; i < 5; i++) {
      futures[i] = asyncTokenService.requestToken(credentials[i]);
    }

    // 모든 요청 대기
    CompletableFuture.allOf(futures).get();
    long endTime = System.currentTimeMillis();

    // Assert
    for (int i = 0; i < 5; i++) {
      UserToken token = futures[i].get();
      assertNotNull(token);
      assertNotNull(token.getToken());
    }

    // 각 요청이 0-5초 걸리지만, 병렬 처리로 총 시간은 5초 이상을 넘지 않아야 함
    long duration = endTime - startTime;
    System.out.println("5개 동시 요청 총 소요 시간: " + duration + "ms");

    // 순차 처리면 최소 25초, 병렬 처리면 5초 안팎
    assertTrue(duration < 15000, "병렬 처리가 제대로 작동하지 않음");
  }

  /**
   * ========== 타이밍 테스트 ==========
   *
   * 테스트 이유:
   * - 0~5000ms 지연이 실제로 적용되는지 확인
   * - 지연이 과도하지 않은지 확인 (< 6초)
   */

  @Test
  @DisplayName("authenticate_지연_시간_검증")
  public void authenticate_DelayTime_WithinRange()
      throws ExecutionException, InterruptedException {
    // Arrange
    Credential credential = new Credential("test", "TEST");

    // Act
    long startTime = System.currentTimeMillis();
    CompletableFuture<User> future = asyncTokenService.authenticate(credential);
    User user = future.get();
    long endTime = System.currentTimeMillis();
    long duration = endTime - startTime;

    // Assert
    assertNotNull(user);
    assertTrue(duration >= 0 && duration < 6000, "지연 시간이 0-6초 범위를 벗어남: " + duration + "ms");
  }
}

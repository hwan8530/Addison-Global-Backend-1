# Addison Global 백엔드 기술 과제

## 소개

Addison Global 백엔드 기술 테스트에 오신 것을 환영합니다.

이 과제의 주요 목표는 문제 해결 방식과 깔끔하고, 잘 테스트되며 재사용 가능한 코드를 작성하는 능력을 평가하는 것입니다. 엄격한 규칙이나 까다로운 질문은 없습니다.

> **참고:** 일부 예제가 Scala로 작성되어 있지만, 과제는 Java로 개발해도 됩니다.

## 용어집
* Credentials - 고객을 인증하는 데 사용되는 _username_과 _password_의 튜플입니다.
* User - 시스템 내에서 주어진 고객을 식별합니다. 간단히 하기 위해, 이는 주어진 고객의 _userId_만 포함하고, 이 값은 해당 고객의 _username_과 일치합니다.
* UserToken - 시스템에서 추가 작업을 수행하기 위해 사용자에게 발급되는 토큰입니다. 형식은 _userId_와 현재 시간의 연결입니다. 예: `user123_2017-01-01T10:00:00.000`

예시 구현:
```scala
case class Credentials(username: String, password: String)
case class User(userId: String)
case class UserToken(token: String)
```

## 과제
목표는 백엔드 서비스/모듈의 정의를 개선하고 그 구현을 제공하는 것입니다. 이를 완료하면 해당 서비스/모듈 기능을 소비하는 REST API를 제공하는 마이크로서비스를 작성합니다.
> **참고:** 단일 모듈로 간단하게 구현하고 패키지로 구조화하는 것을 선호합니다.

### 1. 서비스 Trait / Interface
다음 두 개의 동기 및 비동기 TokenService 정의가 주어집니다.
```scala
trait SyncTokenService {
  protected def authenticate(credentials: Credentials): User
  protected def issueToken(user: User): UserToken

  def requestToken(credentials: Credentials): UserToken = ???
}
```
```scala
import scala.concurrent.Future

trait AsyncTokenService {
  protected def authenticate(credentials: Credentials): Future[User]
  protected def issueToken(user: User): Future[UserToken]

  def requestToken(credentials: Credentials): Future[UserToken] = ???
}
```
**과제:** `requestToken`을 `authenticate`와 `issueToken`을 이용해 각각 구현하세요. 이렇게 하면 서비스를 구현하는 사람은 `authenticate`와 `issueToken`만 구현하면 됩니다.

> **참고:** Scala의 `scala.concurrent.Future`는 Java의 `java.util.concurrent.Future`와 동일하지 않습니다. Scala의 Future는 합성이 가능하므로, Java로 개발하는 경우 적절히 시그니처를 변경해도 됩니다. 추천: `java.util.concurrent.CompletionStage` 또는 `java.util.concurrent.CompletableFuture`를 사용하세요.


### 2. 서비스 구현

다음 API에 대한 구현을 제공하세요. 이 API는 이전 섹션에서 설계한 것과 **다릅니다**:
```scala
 trait SimpleAsyncTokenService {
   def requestToken(credentials: Credentials): Future[UserToken]
 }
```
> **참고:** Scala의 `scala.concurrent.Future`는 Java의 `java.util.concurrent.Future`와 동일하지 않습니다. Scala의 Future는 합성이 가능하므로, Java로 개발하는 경우 적절히 시그니처를 변경해도 됩니다. 추천: `java.util.concurrent.CompletionStage` 또는 `java.util.concurrent.CompletableFuture`를 사용하세요.

**과제 요구사항 / 가이드라인:**

Actor 모델 구현체(예: [Akka](https://akka.io/))를 사용하는 것을 선호하지만 필수는 아닙니다. 다른 프레임워크(예: [Spring](https://spring.io/)) 등을 사용해도 됩니다.

1. 다음 기능을 수행하는 Actor/Service/Module을 구현하세요:
    * *Credentials*를 검증하고 *User* 인스턴스를 반환합니다.
    * *User* 인스턴스는 항상 0 ~ 5000 밀리초 사이의 랜덤 지연 후 반환됩니다.
    * 비밀번호가 username을 대문자로 바꾼 것과 일치하면 검증 성공, 그렇지 않으면 실패입니다. 예:
        * username: house , password: HOUSE => 유효한 자격증명.
        * username: house , password: House => 유효하지 않은 자격증명.
    * 반환되는 *User*의 *userId*는 제공된 *username*이 됩니다.
    * 이 로직은 별도의 Actor/Service/Module에 캡슐화되어야 합니다.

2. 다음 기능을 수행하는 또 다른 Actor/Service/Module을 구현하세요:
    * 주어진 *User*에 대해 *UserToken*을 반환합니다.
    * *UserToken* 인스턴스는 항상 0 ~ 5000 밀리초 사이의 랜덤 지연 후 반환됩니다.
    * 제공된 *User*의 *userId*가 'A'로 시작하면 호출은 실패합니다.
    * *UserToken*의 *token* 속성은 *userId*와 UTC 현재 날짜 시간(`yyyy-MM-dd'T'HH:mm:ssZ`)을 연결한 값입니다:
        * 예: `username: house => house_2017-01-01T10:00:00Z`
    * 이 로직은 별도의 Actor/Service/Module에 캡슐화되어야 합니다.

3. **SimpleAsyncTokenService** 인터페이스/트레이트의 `requestToken` 함수를 다음 방식으로 구현하세요:
    * 그 로직은 Actor/Service/Module에 캡슐화되어야 합니다.
    * 인증과 토큰 발급을 위해 위에서 정의한 actor/service/module들을 사용해야 합니다:
        * 먼저 *Credentials* 검증을 통해 *User*를 얻습니다.
        * 그 다음 *UserToken*을 얻기 위해 토큰 발급 actor/service/module을 호출합니다.
        * 마지막으로 원래 호출자에게 *UserToken*을 반환합니다.

**평가 노트:**

우리는 특히 액터 시스템(또는 서비스 오케스트레이션)의 설계와 테스트 방법에 관심이 있습니다. 다음 항목들에 주의를 기울여 평가합니다:
* **단순성**: 과도하게 설계하지 마세요. 단순할수록 좋습니다.
* **스레딩 모델** 및 **논블로킹 API**: 사용 가능한 자원을 최대한 활용하는 방식.
* **동시성**: 동시 요청을 어떻게 처리하여 성능을 최적화하는지.
* **테스트**: 커버리지를 높이기 위한 테스트 설계 방식.
* **내결함성**: 실패를 어떻게 처리, 격리, 반응하는지.

> **유의사항:**
> * 이 구현은 여러 동시 요청을 처리하도록 설계되어야 합니다!!!
    >
    >      계산에 5초가 걸릴 수 있더라도 그 동안 다른 계산들이 진행되지 못하게 해서는 안 됩니다.
> * 실패를 어떻게 모델링/처리할지 고려하세요.

### 3. REST API

**과제**: 이전 블록에서 구현한 **SimpleAsyncTokenService**의 기능을 제공하는 간단한 REST API를 설계하세요.

구현에는 [Akka HTTP](https://doc.akka.io/docs/akka-http/current/scala/http/)를 사용하는 것을 선호하지만 필수는 아닙니다. 다른 프레임워크([http4s](http://http4s.org/), [Play Framework](https://www.playframework.com/), [Spring Boot](https://projects.spring.io/spring-boot/)) 등을 사용해도 됩니다.

**평가 노트:**

우리는 API의 구조와 완전성, 그리고 그것이 어떻게 테스트되었는지에 관심이 있습니다.

## 제출물
* **소스 코드**: 다음 중 편한 방식으로 프로젝트를 번들하세요:
    * 전체 프로젝트를 포함한 `zip` 파일. (바이너리/로그 등 불필요한 파일은 제외)
    * 작업을 포함한 접근 가능한 개인 저장소(예: GitHub, Bitbucket 등)의 링크.
* **문서 / 실행 지침**:
    * 해결 과정에서의 가정과 결정(기술 및 라이브러리 선택 포함)을 설명하는 `Readme.md`(간단한 설명이면 충분).
    * Linux 환경에서 솔루션과 테스트를 실행하기 위한 필요한 지침들.
> **참고:** 이는 논문이 아니므로 과도한 설명은 불필요합니다. 자기 설명적인 코드가 더 중요합니다.

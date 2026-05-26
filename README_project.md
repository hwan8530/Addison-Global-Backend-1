## Backend Challenge - Addison 1

### Introduction
backend-challenges의 AddisonGlobal - 1번 챌린지입니다.

### Project Description
주어진 요구사항에 따라 간단한 RESTful API를 구축하는 프로젝트입니다.

요구사항은 README.md 파일에 명시되어 있으며 API 엔드포인트, 데이터 모델 및 기타 세부사항이 포함되어 있습니다.

### Technologies Used
- Java 17
- Spring Boot 4.0.6

### Technical Retrospective
- DTO : 별도의 DTO를 생성하여 API 요청과 응답을 처리하도록 구현해야 하지만 간단한 프로젝트이므로 Entity를 직접 사용하여 구현했습니다.
- Repository : Repository 인터페이스를 생성하여 데이터 액세스를 추상화해야하지만 간단한 프로젝트로 별도의 DB 사용이 없으므로 Respository 인터페이스는 사용하지 않았습니다.
- Test : 단위 테스트 및 통합 테스트 작성에 어려움을 겪어 AI의 도움을 받아 테스트 코드를 작성했습니다.
- Exception Handling : 예외 처리를 위한 별도의 클래스나 매커니즘을 구현해야하지만 간단한 프로젝트이므로 Controller에서 직접 예외처리를 구현했습니다.
- Validation : 입력 데이터의 유효성 검사를 위한 별도의 검증 로직을 구현했어야 했습니다.
- Async Processing : 비동기 처리를 위해 별도의 thread pool을 구성했으나 thread pool의 임계점에 설정값에 대한 이유가 명확하지 않았습니다.
- Logging : 별도의 로깅 없이 구현했습니다.
- API Documentation : Swagger와 같은 도구를 사용하며 API 문서를 자동으로 생성해야 합니다.

### Conclusion
이 프로젝트는 간단한 Restful API를 구축하는데 필요한 기술과 개념을 연습하는 좋은 기회였습니다.

자주 다뤄보지 않던 비동기 처리에 대해 공부할 수 있었고 API Documentation과 Test 작성의 중요성을 다시한번 깨닫는 기회였습니다.
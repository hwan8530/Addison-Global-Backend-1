package backendchallenge.addison1.User.controller;

import backendchallenge.addison1.User.entity.Credential;
import backendchallenge.addison1.User.entity.UserToken;
import java.util.Map;
import java.util.concurrent.ExecutionException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import backendchallenge.addison1.User.service.AsyncTokenService;

@RestController
@RequiredArgsConstructor
public class UserController {
  private final AsyncTokenService asyncTokenService;

  @PostMapping("/token")
  public ResponseEntity<?> generateToken(@RequestBody Credential credential)
      throws ExecutionException, InterruptedException {
    try {
      UserToken token = asyncTokenService.requestToken(credential).get();
      return ResponseEntity.ok(token);
    } catch (IllegalArgumentException e) {
      return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
    }
  }
}

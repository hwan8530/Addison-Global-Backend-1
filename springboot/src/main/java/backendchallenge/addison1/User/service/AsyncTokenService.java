package backendchallenge.addison1.User.service;

import backendchallenge.addison1.User.entity.Credential;
import backendchallenge.addison1.User.entity.User;
import backendchallenge.addison1.User.entity.UserToken;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Random;
import java.util.concurrent.CompletableFuture;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class AsyncTokenService {
  @Async("tokenServiceTaskExecutor")
  public CompletableFuture<User> authenticate(Credential credential)
  {
    if (!credential.getUsername().toUpperCase().equals(credential.getPassword()))
      throw new IllegalArgumentException("Invalid Credentials");

    CompletableFuture<User> future = new CompletableFuture<>();
    Random random = new Random();
    try {
      Thread.sleep(random.nextInt(5001));
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    future.complete(new User(credential.getUsername()));
    return future;
  }

  @Async("tokenServiceTaskExecutor")
  public CompletableFuture<UserToken> issueToken(User user) {
    if (user.getUserid().startsWith("A"))
      throw new IllegalArgumentException("Invalid User ID");

    LocalDateTime now = LocalDateTime.now();
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'hh:mm:ss.SSS'Z'");

    String token = user.getUserid() + "_" + now.format(formatter);
    CompletableFuture<UserToken> future = new CompletableFuture<>();
    Random random = new Random();
    try {
      Thread.sleep(random.nextInt(5001));
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    future.complete(new UserToken(token));
    return future;
  }

  @Async("tokenServiceTaskExecutor")
  public CompletableFuture<UserToken> requestToken(Credential credential) {
    CompletableFuture<User> user = authenticate(credential);
    return user.thenCompose(this::issueToken);
  }
}

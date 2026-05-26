package backendchallenge.addison1.User.service;

import java.time.LocalDateTime;
import backendchallenge.addison1.User.entity.Credential;
import backendchallenge.addison1.User.entity.User;
import backendchallenge.addison1.User.entity.UserToken;
import java.time.format.DateTimeFormatter;
import org.springframework.stereotype.Service;
import java.util.Random;

@Service
public class SyncTokenService {
  public User authenticate(Credential credential)
  {
    if (!credential.getUsername().toUpperCase().equals(credential.getPassword()))
      throw new IllegalArgumentException("Invalid Credentials");
    Random random = new Random();
    try {
      Thread.sleep(random.nextInt(5001));
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    return new User(credential.getUsername());
  }

  public UserToken issueToken(User user) {
    if (user.getUserid().startsWith("A"))
      throw new IllegalArgumentException("Invalid User ID");

    LocalDateTime now = LocalDateTime.now();
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'hh:mm:ss.SSS'Z'");

    String token = user.getUserid() + "_" + now.format(formatter);
    Random random = new Random();
    try {
      Thread.sleep(random.nextInt(5001));
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    return new UserToken(token);
  }

  public UserToken requestToken(Credential credential) {
    User user = authenticate(credential);
    return issueToken(user);
  }
}

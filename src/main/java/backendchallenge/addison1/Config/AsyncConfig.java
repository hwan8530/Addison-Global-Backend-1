package backendchallenge.addison1.Config;

import java.util.concurrent.Executor;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;

@Configuration
@EnableAsync
public class AsyncConfig {
  @Bean(name = "tokenServiceTaskExecutor")
  public Executor threadPoolTaskExecutor() {
    LinkedBlockingQueue<Runnable> queue = new LinkedBlockingQueue<>(100);
    return new ThreadPoolExecutor(10, 50, 10, TimeUnit.SECONDS, queue);
  }
}

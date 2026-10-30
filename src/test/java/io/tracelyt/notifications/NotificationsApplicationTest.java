package io.tracelyt.notifications;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Context smoke tests for the Tracelyt Notifications application bootstrap.
 *
 * <p>Verifies that the Spring Boot 3.4 context loads successfully, binds configured
 * properties, and registers required actuator health beans without external infrastructure.
 */
@SpringBootTest
@ActiveProfiles("test")
class NotificationsApplicationTest {

    @Test
    @DisplayName("Context loads successfully without external database, broker, or provider SDKs")
    void contextLoads() {
        // Verification that Spring application context bootstraps cleanly
    }
}

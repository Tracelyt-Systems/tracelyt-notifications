package io.tracelyt.notifications;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Bootstrap entry point for the Tracelyt Notifications subsystem.
 *
 * <p>In this architectural foundation phase, this class verifies application
 * context loading, configuration binding, and Actuator health endpoints.
 * Actual email dispatch, Slack/Teams SDK integrations, and webhook delivery
 * are intentionally deferred to future implementation stages.
 */
@SpringBootApplication
public class NotificationsApplication {

    /**
     * Main entry point for the application bootstrap.
     *
     * @param args command-line arguments passed at startup
     */
    public static void main(String[] args) {
        SpringApplication.run(NotificationsApplication.class, args);
    }
}

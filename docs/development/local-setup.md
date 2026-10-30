# Local Development Setup Guide

This guide walks you through setting up your local environment to build, test, and contribute to `tracelyt-notifications`.

---

## 1. Prerequisites

Before getting started, ensure the following tools are installed:

- **Java Development Kit (JDK)**: Java 21 (LTS) or higher (Eclipse Temurin, Microsoft Build of OpenJDK, or Amazon Corretto).
- **Git**: 2.40+ with standard command-line tooling.
- **Python 3.10+**: Required for executing repository documentation and link validation scripts.
- **Make** (Optional): Convenient for executing common workflow targets (`make test`, `make build`).

Verify your local Java installation:
```bash
java -version
```

---

## 2. Cloning the Repository

```bash
git clone https://github.com/Tracelyt-Systems/tracelyt-notifications.git
cd tracelyt-notifications
```

---

## 3. Build & Test Commands

The repository includes the Maven Wrapper (`mvnw` for Linux/macOS and `mvnw.cmd` for Windows). No local Maven installation is required.

### 3.1 Compile & Validate Static Code Analysis
Run Checkstyle static analysis and validate the project model:
```bash
# Linux / macOS
./mvnw -B -ntp clean validate checkstyle:check

# Windows (Command Prompt / PowerShell)
mvnw.cmd -B -ntp clean validate checkstyle:check
```

### 3.2 Run Unit Tests
Execute all unit tests (in headless non-blocking mode):
```bash
# Linux / macOS
./mvnw -B -ntp test

# Windows (Command Prompt / PowerShell)
mvnw.cmd -B -ntp test
```

### 3.3 Package Runnable JAR
Package the application JAR:
```bash
# Linux / macOS
./mvnw -B -ntp package -DskipTests

# Windows (Command Prompt / PowerShell)
mvnw.cmd -B -ntp package -DskipTests
```

### 3.4 Using the Makefile
If `make` is installed on your workstation:
```bash
make validate    # Runs checkstyle static analysis
make test        # Runs unit tests
make build       # Compiles and packages application
make docs-check  # Runs python tools/validate_docs.py
make clean       # Removes target build artifacts
```

---

## 4. Documentation Validation

To verify that all internal documentation links and references resolve without broken paths or exposed secrets:
```bash
python tools/validate_docs.py
```

---

## 5. IDE Configuration

### 5.1 IntelliJ IDEA
1. Open IntelliJ IDEA and select **Open** -> choose `tracelyt-notifications/pom.xml`.
2. Configure Project SDK: Ensure JDK 21 is selected in **File -> Project Structure -> Project**.
3. Enable Checkstyle: Install the **Checkstyle-IDEA** plugin and point it to `.checkstyle.xml` in the repository root.

### 5.2 VS Code
1. Install the **Extension Pack for Java** and **Checkstyle for Java**.
2. Configure `.vscode/settings.json` with `"java.configuration.checkstyle.configFile": ".checkstyle.xml"`.

---

## 6. Offline Development Considerations

If working in an air-gapped or restricted network environment:
- Pre-download all Maven dependencies in an online environment:
  ```bash
  ./mvnw dependency:go-offline
  ```
- Store the `.m2/repository` cache locally.

---

## 7. Related Documentation

- [Project Structure](project-structure.md)
- [Coding Standards](coding-standards.md)
- [Testing Strategy](testing-strategy.md)

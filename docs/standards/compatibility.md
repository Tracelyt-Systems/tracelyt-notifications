# Compatibility and Versioning Policy

This document defines the semantic versioning rules, API compatibility guarantees, and deprecation policies for `tracelyt-notifications`.

---

## 1. Semantic Versioning (SemVer 2.0)

All releases and contract interfaces follow [Semantic Versioning 2.0.0](https://semver.org/):

$$\text{MAJOR}.\text{MINOR}.\text{PATCH}$$

- **MAJOR**: Incompatible API or event schema changes that require callers to alter their code or message structures.
- **MINOR**: Backward-compatible functionality additions (e.g., adding an optional field to a notification request).
- **PATCH**: Backward-compatible bug fixes and security patches.

---

## 2. API Compatibility Rules

### 2.1 Backward Compatibility Guarantees
- **Additive Schema Changes**: New fields added to JSON payloads must always be optional. Callers that do not provide the field must continue to receive valid responses.
- **Tolerant Reader**: Internal deserializers must ignore unknown properties (`DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES = false`) to permit independent upgrades of upstream producers.
- **No In-Place Type Changes**: The data type or format of an existing field cannot be altered within the same major version (e.g., changing an integer timestamp to an ISO-8601 string requires a new field or major version).

### 2.2 Deprecation Process
1. **Notice**: Mark the endpoint or property with `@Deprecated` in code and document the planned sunset in release notes.
2. **Transition Window**: The deprecated feature must remain functional for at least one minor release cycle (minimum 90 days).
3. **Removal**: The feature is removed in the subsequent major version.

---

## 3. Related Documentation

- [Contract Governance](contract-governance.md)
- [Error Handling Standards](error-handling.md)
- [Milestone Roadmap](../roadmap/README.md)

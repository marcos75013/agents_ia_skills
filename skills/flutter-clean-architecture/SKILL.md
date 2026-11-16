---
name: flutter-clean-architecture
description: Design or implement a Flutter feature with proportionate feature-first Clean Architecture. Use for new Flutter features, boundary decisions, or explicitly requested incremental refactors; do not use to force a repository-wide migration.
---

# Flutter Clean Architecture

Build the requested Flutter change with clear, testable boundaries while preserving the project's working conventions.

## Before changing code

1. Read the applicable repository instructions, `pubspec.yaml`, Flutter/Dart constraints, current feature layout, dependency injection, navigation, error model and representative tests.
2. Determine whether the request concerns a new feature, an extension of an existing feature, or an explicitly authorized refactor. For an existing project, prefer its established architecture unless a concrete problem justifies a local change.
3. State the intended slice and files before a broad structural change. Never turn a feature request into a repository-wide migration without separate authorization.

## Target structure

For a new feature where layered separation is proportionate, prefer:

```text
lib/features/<feature>/
├── presentation/
├── domain/
└── data/
```

- `presentation` owns widgets, UI coordination and state management. It may depend on `domain`, not on concrete infrastructure details.
- `domain` owns business entities, use cases and repository contracts. Keep it independent of Flutter and `data` when the project and feature complexity justify a domain layer.
- `data` owns DTOs, mappings, data sources and repository implementations. Convert infrastructure failures into the project's explicit error model at the appropriate boundary.
- Assemble implementations at an existing composition root. Do not introduce a second dependency-injection mechanism solely for the new feature.

Use the smallest structure that preserves useful boundaries. Do not create empty layers, one-line abstractions, use cases without business or orchestration value, or duplicate models without a real boundary.

## Implementation rules

- Keep dependency direction toward business rules; avoid imports from `domain` to Flutter, `presentation` or `data`.
- Follow the project's naming, routing, serialization and result/error conventions when they are sound.
- Preserve public APIs unless the request explicitly authorizes a breaking change.
- Add tests at the cheapest level that proves the behavior: domain logic first, then mappings or repositories, then widgets/integration paths where risk warrants them.
- Verify with the project's existing formatter, analyzer and targeted tests. Do not install dependencies or execute unknown scripts without authorization.

## Completion report

Summarize the feature boundary, dependency direction, files changed, tests and commands actually run, and any architectural compromise left in place. Distinguish verified results from checks not run.

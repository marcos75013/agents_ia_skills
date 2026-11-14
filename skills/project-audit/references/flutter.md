# Flutter / Dart audit profile

Read only when Flutter or Dart is detected.

- Establish Flutter and Dart constraints from `pubspec.yaml`, lock/configuration files and available version output; do not infer an installed SDK version from a constraint.
- Map platforms, flavors, entry points, packages, state management, navigation, dependency injection, persistence, networking, code generation and platform channels.
- Observe the actual feature/module boundaries and dependency direction before comparing them with a target architecture.
- For the toolkit target, compare objectively with feature-first Clean Architecture: `presentation`, `domain`, `data`; Cubit/`flutter_bloc`; use cases; repository interfaces in Domain and implementations in Data.
- Treat deviations as findings only when they create observable coupling, testability or maintenance costs. Never propose an automatic migration.
- Inspect analyzer options, tests, golden/integration coverage, semantics, focus, text scaling, reduced motion, asset sizes, rebuilds, startup, background work and release signing configuration without exposing secrets.

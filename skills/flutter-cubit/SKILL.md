---
name: flutter-cubit
description: Implement or revise Flutter state management with Cubit and flutter_bloc, including explicit states and focused tests. Use when a Flutter task calls for Cubit or the project already uses it; do not migrate another state-management approach without explicit authorization.
---

# Flutter Cubit

Implement predictable state transitions with the project's installed `flutter_bloc` version and existing conventions.

## Before changing code

1. Inspect `pubspec.yaml`, the relevant widgets, existing Cubits/states, dependency injection, error handling and tests. Confirm the installed APIs instead of assuming the latest package behavior.
2. Define the observable UI states and user/system actions for the requested scope. Keep business rules in domain services or use cases when those boundaries already exist.
3. If the project uses another state-management approach, preserve it unless the user explicitly requests a scoped migration. Never propose a repository-wide migration merely because Cubit is the toolkit default for new Flutter work.

## Cubit design

- Give the Cubit one cohesive responsibility and inject its dependencies; do not reach into service locators from transition methods when the project supports constructor injection.
- Model states so the UI can distinguish initial, loading, success, empty and failure outcomes only when those outcomes are real. Avoid Boolean combinations that permit contradictory states.
- Keep state immutable using the project's established value-equality or code-generation approach. Do not add a package solely to avoid a small explicit implementation.
- Prevent stale asynchronous results, duplicate submissions and emissions after cancellation where the observed flow makes those races possible.
- Expose failures without secrets or infrastructure-only details, using the project's error model and accessible UI feedback.
- Keep widgets declarative: trigger actions, render states and handle navigation or transient effects at the appropriate presentation boundary.

## Tests and verification

- Test initial state, meaningful transitions, failures and relevant edge cases. Prefer behavior assertions over private implementation details.
- For asynchronous work, cover ordering, cancellation or repeated actions only when the production flow can encounter them.
- Add widget tests when state rendering, accessibility semantics, navigation or transient feedback is part of the change.
- Run the existing formatter, analyzer and smallest relevant test set. Do not install packages or run unknown project scripts without authorization.

## Completion report

Report the state model, transitions implemented, dependencies used, tests and commands actually run, and remaining unverified paths. Do not claim race safety, coverage or compatibility that was not observed.

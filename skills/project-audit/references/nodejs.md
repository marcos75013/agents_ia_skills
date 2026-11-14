# Node.js audit profile

Read only when Node.js is detected, excluding an Angular workspace unless it also contains a distinct Node backend or service.

- Establish Node, framework, TypeScript, module format and package manager from manifests, lockfiles and configuration; do not equate an engine constraint with the installed runtime.
- Map transport, validation, business orchestration, persistence, queues/jobs and external services without demanding empty layers.
- Inspect runtime input validation, authentication/authorization, rate limiting, security headers, timeouts, cancellation, process errors and graceful shutdown.
- Review scripts and lifecycle hooks without executing unknown ones; inspect lockfile presence, dependency overrides and production dependency scope.
- Assess unit, integration, contract and HTTP tests, plus resource isolation and determinism.
- Examine event-loop blocking, connection reuse, bundle/cold-start size, memory, serverless duration and background polling as performance and cost signals.

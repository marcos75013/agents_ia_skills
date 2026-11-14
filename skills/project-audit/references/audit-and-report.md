# Common audit and report guide

Read this reference after the initial inventory.

## Analysis dimensions

For each applicable dimension, capture evidence, current behavior, risk and uncertainty:

- architecture: applications, modules, boundaries, dependency direction, data flows, external contracts and cross-repository coupling;
- development: repository layout, branching/release signals, formatting, linting, error handling, documentation and reproducible commands;
- quality and tests: test levels, critical paths, determinism, coverage signals and missing risk-based checks;
- security: trust boundaries, authentication, authorization, validation, secrets handling, personal data, dependency controls and CI permissions;
- accessibility: semantic structure, keyboard/focus, labels/states, contrast, reduced motion and evidence of manual testing;
- eco-design and performance: unnecessary features or transfers, media, caching, background work, CPU/memory/startup/network budgets and measurements;
- delivery: CI triggers, pinned actions, least privilege, artifacts, environments, rollback, observability and protected production steps;
- infrastructure cost: providers, billable resources, free-tier limits, quotas, storage, bandwidth, build/runtime usage, alerts and credible billing risks;
- automation: repeated deterministic work suitable for linting, tests, hooks, CI or a focused skill.

Do not claim compliance from configuration or an automated score alone. Current prices and service limits require a dated authoritative source; otherwise mark them unverified.

## Evidence levels

- **Fact:** directly supported by a file, version output or repository setting.
- **Finding:** interpretation of facts with a stated impact or risk.
- **Recommendation:** proportionate next action and success criterion.
- **Unverified:** relevant item that could not be observed or safely tested.

Use `P0` only for an immediate credible threat or outage, `P1` for high-impact near-term risk, `P2` for planned improvement and `P3` for optional optimization. Rate effort `S/M/L` and change risk `low/medium/high`.

## Report shape

1. Executive summary and scope, including repositories and exclusions.
2. Technology/version table with evidence and confidence.
3. Architecture map and delivery path.
4. Prioritized findings table: ID, evidence, impact, priority, effort, change risk, recommendation and success check.
5. AI integration: concise proposed `AGENTS.md` topics, toolkit skills, possible specialized agents, CI improvements and token-saving routes. Do not create them.
6. Unverified items and how to verify them safely.
7. Commands and checks run, including failures or skipped checks.

For multiple repositories, add a contract matrix with owners, versions, compatibility, delivery order and rollback dependencies. Keep repository-specific facts separate from system-wide inferences.

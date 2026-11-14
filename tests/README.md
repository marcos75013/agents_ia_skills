# Validation scenarios

Run all synthetic scenarios with:

```bash
python3 -m unittest discover -s tests -v
```

The fixtures are created in temporary directories and contain only minimal manifests. They verify routing for:

- Flutter from `pubspec.yaml`;
- Angular without classifying its build-time Node dependency as a Node backend;
- Spring Boot from a Maven build;
- a Node.js backend from its runtime framework;
- a multi-technology workspace containing all four profiles.

Installer scenarios verify `CREATE`, `UNCHANGED` and `CONFLICT` states and assert that preview mode creates no target files. They validate instruction routing and deterministic helpers; they do not fabricate or assert real audit findings.

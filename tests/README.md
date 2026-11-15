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
- a plain Node.js project without a known server framework;
- a multi-technology workspace containing all four profiles.

They also verify pruning of generated/dependency directories and safe handling of malformed JSON. Installer scenarios cover project and user destinations, `CREATE`, `UNCHANGED`, `CONFLICT`, invalid manifests and unknown technology filters while asserting that preview mode creates no target files. The toolkit validation scenario checks the manifest, skill frontmatter, UI metadata, internal links and common secret patterns. These tests validate routing and deterministic helpers; they do not fabricate or assert real audit findings.

Additional contract tests cover incomplete repositories, Flutter projects without Cubit, the detector's read-only invariant, evidence levels and the minimal GitHub Actions workflow. These assertions prove deterministic behavior and instruction presence only. Architecture judgment, prioritization and model compliance require the independent evaluation described in [`docs/project-audit-evaluation.md`](../docs/project-audit-evaluation.md).

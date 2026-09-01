# Agent guide

This is the independent BlueMap add-on repository for the exact Connected
Glass 1.1.14 plus Fusion 1.3.12 tuple in All the Mons 1.2.0. Read the workspace
and portfolio guides, this README, `docs/ARCHITECTURE.md`,
`docs/PROVENANCE.md`, and `docs/RELEASING.md` before changing it.

## Boundaries

- Java 21, Minecraft 1.21.1, and BlueMap 5.23 feature-backport commit
  `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac` with API commit
  `285c9a60eff3ac2b0cab308ce1058d1565be0971`.
- Release candidate version `0.1.0-alpha.3` uses Adapter API
  `0.1.0-alpha.2` at commit `e81f08bc4bfbf02d810ec8949a019130e2e61634`.
- Source-bundle BlueMap Fusion Resource Models `0.1.0-alpha.1` only from
  commit `3ddd5d39bb7cc8664c242aedd849a636316075c2`, source tree
  `6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a`.
- Own only the generated 119-ID `connectedglass:*` allowlist: 68 full cubes,
  51 panes, and exactly 1,700 legal states.
- Never register `fusion:*`, route another namespace, or add a runtime provider
  dependency on another add-on.
- Bundle no Connected Glass/Fusion code, classes, JSON, PNG, metadata, or JARs.
  Both exact artifacts are All Rights Reserved. Interpret only
  operator-installed resources with independently authored code.
- Preserve stock rendering outside the exact route and atomically fall back on
  malformed state/resource observations. Propagate BlueMap capacity failures.
- Structural JSON and metadata are hash-locked. PNG pixel overrides are allowed
  only when exact dimensions remain unchanged.
- Treat vertical pane-cap behavior as release-blocking until the exact-client
  gallery observation agrees with the independently authored overlap rule.
- Keep identifiers under `bluemap_connectedglass`, Java under
  `io.github.janguenter.bluemap.connectedglass`, extension ID
  `bluemap_connectedglass:exact_profile`, and renderer ID
  `bluemap_connectedglass:fusion_model`.
- Do not change cluster, production, remotes, tags, or releases without the
  separate operational/release gate.
- Keep local profile parsing, predicates, catalogs, routes, fallback, and
  emission policy outside the shared Fusion model package.

## Generated inputs

Run `tools/generate_profile.py` only with the exact artifacts pinned in README.
Generated profile and gallery files must be reproducible and checked in. Never
hand-edit generated TSV, JSON, mcfunction, or checksum output.

## Validation

Use focused compilation/tests while implementing a coherent tranche. Before a
runtime candidate or release, run the full clean gate from README, inspect both
JARs, freeze the tree, and obtain an independent read-only audit. Record only
tests actually observed. Before presenting a BlueMap URL, open that exact URL
and perform the workspace-required lightweight visual sanity check.

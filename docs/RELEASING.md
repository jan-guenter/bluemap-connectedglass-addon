# Releasing

Version `0.1.0-alpha.2` is a source-consolidation candidate. Its exact
production JAR identity is recorded outside the packaged provenance in
`provenance/release.json`. The `0.1.0-alpha.1` authorization and frozen hashes
below do not authorize publishing changed `0.1.0-alpha.2` assets.

Initialize both source submodules before any gate:

```bash
git submodule update --init --recursive -- \
  tooling/bluemap-addon-toolkit modules/bluemap-fusion-resource-models
```

The settings preflight must accept both gitlinks and reject a changed Fusion
module HEAD, index, worktree, or `src/main/java` tree.

The locally sealed `0.1.0-alpha.2` payloads are:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `bluemap-connectedglass-addon-0.1.0-alpha.2.jar` | 158,546 | `f73841c78da88808bbb9a5a630526e75902a2c56bfc9f7600ccbc39d3572e446` |
| `bluemap-connectedglass-addon-0.1.0-alpha.2-sources.jar` | 94,085 | `ee652f580e614e6dd52db181519d50a38183e001b8e2239e3d829bc8f49b4da9` |
| `bluemap-connectedglass-addon-0.1.0-alpha.2.pom` | 1,375 | `3f6a1e8250bd0dbf62ff046605e7d3d3bec80ae6b8a24444c14aa7f2306c38ec` |
| `bluemap-connectedglass-addon-0.1.0-alpha.2.module.json` | 2,868 | `c76ad74c76aedf7886060071cad0507aa1d81f745fb39e7972b50095fbc78f59` |

Two clean local builds produced byte-identical copies of all four payloads.
`provenance/release.json` is the machine-readable lock.

The owner explicitly accepted the frozen candidate's visual result on
2026-08-16 after its exact-client pane calibration, isolated BlueMap staging,
restart-scoped disabled control, and physical rollback passed. Publication of
the exact assets below as immutable prerelease `0.1.0-alpha.1` is authorized,
including the reviewed merge, annotated tag, Maven publication, and GitHub
Release required by this procedure. This candidate-specific authorization does
not authorize production deployment, alter production state, or establish a
supported production version.

The intended coordinates are:

- GitHub repository: `jan-guenter/bluemap-connectedglass-addon`;
- Maven: `io.github.jan-guenter:bluemap-connectedglass-addon:<version>`;
- release assets: binary JAR, sources JAR, POM, Gradle module metadata, and
  `SHA256SUMS`.

The frozen candidate asset identities are:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| `bluemap-connectedglass-addon-0.1.0-alpha.1.jar` | 155,396 | `eb1dc07a6f9906f83a710e175cb8c119f0464bda73f651fa13a6e24900ffb70e` |
| `bluemap-connectedglass-addon-0.1.0-alpha.1-sources.jar` | 92,165 | `a2f65dd74c439ab6b1152db6e3255a7f4d282b4870b56c0c8e7f1ee65f2999f9` |
| `bluemap-connectedglass-addon-0.1.0-alpha.1.pom` | 1,375 | `87489782df3acdad2046243d840bb4f1d81cf5cf685298f66072f6b883d0dc38` |
| `bluemap-connectedglass-addon-0.1.0-alpha.1.module.json` | 2,868 | `209c4f441d9e2e5a3eb0da13a136c955d54de7cc09875bb677317a2aed6c1c8b` |
| `SHA256SUMS` | 476 | `ca45c8f69e865d0d47ce665355e28069d6d928ff806c6f86d2e686b47fcb7cdc` |

Documentation and workflow hardening may occur after the candidate freeze only
if the release gate proves the five asset identities above unchanged.

Release authorization is limited to the exact five identities above and the
bounded release contents described here. Any changed release asset requires a
new freeze, validation cycle, and explicit owner acceptance.

Before tagging:

1. regenerate/check the exact profile and gallery from the pinned artifacts;
2. run the full clean README gate and inspect JAR/source/POM/module contents;
3. run `actionlint .github/workflows/*.yml`;
4. confirm the tree is clean, the version changed through a reviewed PR, and
   PR CI is green;
5. tag the reviewed main-branch merge commit with an annotated
   `v<addon_version>` tag;
6. let the release workflow reproducibly build and compare the candidate,
   create a draft, attest both JARs, publish Maven resumably, verify exact
   bytes/sidecars, and only then publish the release;
7. update the private workspace gitlink and exact release identity separately.

Never attach Connected Glass/Fusion JARs or assets, the gallery datapack,
runtime logs, screenshots, worlds, or reports to the public release.

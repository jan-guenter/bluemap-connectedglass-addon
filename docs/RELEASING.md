# Releasing

There is no release authorization yet. The frozen candidate passed exact-client
pane calibration, isolated BlueMap staging, the restart-scoped disabled
control, and physical rollback on 2026-08-16. Owner visual acceptance remains
pending and is a release blocker; technical completion alone does not permit a
merge, tag, Maven publication, or GitHub Release.

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

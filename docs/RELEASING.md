# Releasing

There is no release authorization yet. Release only after exact-client pane
calibration, isolated BlueMap staging, physical rollback, owner visual
acceptance, and a frozen independent artifact audit.

The intended coordinates are:

- GitHub repository: `jan-guenter/bluemap-connectedglass-addon`;
- Maven: `io.github.jan-guenter:bluemap-connectedglass-addon:<version>`;
- release assets: binary JAR, sources JAR, POM, Gradle module metadata, and
  `SHA256SUMS`.

Before tagging:

1. regenerate/check the exact profile and gallery from the pinned artifacts;
2. run the full clean README gate and inspect JAR/source/POM/module contents;
3. run `actionlint .github/workflows/*.yml`;
4. confirm the tree is clean, the version changed through a reviewed PR, and
   PR CI is green;
5. tag the reviewed main-branch merge commit with an annotated
   `v<addon_version>` tag;
6. let the release workflow build once, create a draft, attest JARs, publish
   Maven resumably, verify bytes/sidecars, and only then publish the release;
7. update the private workspace gitlink and exact release identity separately.

Never attach Connected Glass/Fusion JARs or assets, the gallery datapack,
runtime logs, screenshots, worlds, or reports to the public release.

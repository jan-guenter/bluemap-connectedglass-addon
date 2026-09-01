# Third-party and provenance inventory

| Component | Role | Exact identity | License | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile-time ABI and adapted renderer mechanics | Feature backport `5.22-feature.backport-5.23-stateless-java-web-server-46`, commit `7e07f4e74ec1e92a6ead9aa1e66054af3e133aac` | MIT | License notice only |
| BlueMap Add-on Adapter API | Four narrow 5.23 adapter helpers | `0.1.0-alpha.2`, commit `e81f08bc4bfbf02d810ec8949a019130e2e61634`, source tree `2f974c9bb2ba13888d69682f86f30f58922d30eb` | MIT | Four sources compile into this add-on; no module JAR |
| BlueMap Rechiseled Add-on | First-party scaffold and independent Fusion interpreter substrate | peeled tag commit `8588d99388c213b938d79931dd6d9e9ef8e4099c` | MIT | Source adapted; no binary/assets |
| BlueMap Fusion Resource Models | First-party neutral Fusion model source | `0.1.0-alpha.1`, commit `3ddd5d39bb7cc8664c242aedd849a636316075c2`, source tree `6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a` | MIT | Five sources compile into this add-on; no module JAR |
| Connected Glass | Operator-installed blocks/models/textures | `1.1.14`, 819,976 bytes, SHA-256 `e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe` | All Rights Reserved | No |
| Fusion | Operator-installed model/texture format resources | `1.3.12`, 923,270 bytes, SHA-256 `17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa` | All Rights Reserved | No |
| JUnit Jupiter | Tests | 5.11.4 BOM | EPL-2.0 | No |
| Checkstyle | Source style | 10.18.2 | LGPL-2.1-or-later | No |

The profile generator records only independently derived identities, paths,
sizes, hashes, dimensions, shapes, legal-state counts, and bounded schema
facts. No Connected Glass or Fusion source expression was copied or adapted.
Production and sources JAR gates reject their classes, archives, namespaces,
assets, and data resources.

BlueMap's complete MIT notice is retained in `LICENSE-BlueMap` and packaged as
`META-INF/LICENSE-BlueMap` in the binary and sources JARs. The machine-readable
record is `provenance/upstreams.json`.

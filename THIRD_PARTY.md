# Third-party and provenance inventory

| Component | Role | Exact identity | License | Bundled |
| --- | --- | --- | --- | --- |
| BlueMap | Compile-time ABI and adapted renderer mechanics | Backport `5.22-agent.backport-5.22-mc1.21.1-2`, commit `9be321df995a1103808621d529eb72773e719d4d` | MIT | License notice only |
| BlueMap Rechiseled Add-on | First-party scaffold and independent Fusion interpreter substrate | peeled tag commit `8588d99388c213b938d79931dd6d9e9ef8e4099c` | MIT | Source adapted; no binary/assets |
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

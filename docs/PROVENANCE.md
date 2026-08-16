# Provenance and clean-room boundary

The current profile derives from the exact operator-installed All the Mons
1.2.0 artifacts listed in README. The generator records only factual archive
metadata and independently derived structural observations: resource paths,
byte sizes, hashes, image dimensions, placed block IDs, legal state schemas,
model selections, predicate names, modifier targets, and aggregate counts.

Connected Glass 1.1.14 and Fusion 1.3.12 both declare All Rights Reserved and
contain no standalone license grant. Their code, classes, JSON, models,
textures, metadata, and binaries are never committed or packaged. No upstream
source checkout is used or correlated for implementation.

The Fusion interpreter and selectors are independently authored against the
bounded installed resource contract and runtime observations. The repository
starts from the project's own MIT BlueMap Rechiseled Add-on scaffold at peeled
tag commit `8588d99388c213b938d79931dd6d9e9ef8e4099c`; Connected Glass-specific
profile facts, pane/state semantics, tests, and gallery replace all Rechiseled
generated content.

`FusionModelEmitter` includes MIT mechanics adapted from BlueMap 5.22's
renderer with its notice retained in the file and `LICENSE-BlueMap`.

The binary and sources JAR audits reject Connected Glass/Fusion namespaces,
third-party classes, data/assets, nested archives, and Minecraft/NeoForge/
BlueMap implementation classes. The complete factual record is
`provenance/upstreams.json`.

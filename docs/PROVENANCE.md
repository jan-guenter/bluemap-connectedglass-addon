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
bounded installed resource contract and runtime observations. Version
`0.1.0-alpha.2` source-bundles five neutral MIT model types from BlueMap Fusion
Resource Models `0.1.0-alpha.1`, exact commit
`3ddd5d39bb7cc8664c242aedd849a636316075c2` and `src/main/java` tree
`6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a`. The module supplies no profile,
resource admission, predicate, catalog, route, fallback, or emitter policy.
Its JAR is neither nested nor installed.

The repository starts from the project's own MIT BlueMap Rechiseled Add-on
scaffold at peeled tag commit
`8588d99388c213b938d79931dd6d9e9ef8e4099c`; Connected Glass-specific profile
facts, pane/state semantics, tests, and gallery replace all Rechiseled
generated content.

`FusionModelEmitter` includes MIT mechanics adapted from BlueMap 5.22's
renderer with its notice retained in the file and `LICENSE-BlueMap`.

The binary and sources JAR audits reject Connected Glass/Fusion namespaces,
third-party classes, data/assets, nested archives, and Minecraft/NeoForge/
BlueMap implementation classes. They require the five shared sources and eight
resulting class files exactly once and reject the displaced local class names.
The complete factual record is `provenance/upstreams.json`.

The frozen `0.1.0-alpha.1` artifact retains its embedded
`"status": "unreleased-implementation"` marker. Version `0.1.0-alpha.2` is a
new reviewed build, so its packaged manifest records
`"status": "fusion-source-module-migration-candidate"`. Release-only artifact
hashes remain outside the JAR in `provenance/release.json`.

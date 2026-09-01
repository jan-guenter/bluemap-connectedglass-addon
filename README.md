# BlueMap Connected Glass Add-on

This standalone MIT BlueMap add-on restores the connected textures and pane
models installed by Connected Glass 1.1.14 and Fusion 1.3.12 on the exact All
the Mons 1.2.0 baseline. Version `0.1.0-alpha.3` targets the exact BlueMap 5.23
feature backport and source-bundles the released MIT Adapter API and Fusion
Resource Models modules from exact gitlinks. The migration replaces local
registry, extension, and dispatch helpers without changing the two-layout
profile, predicates, route, fallback, or emitter. The frozen `0.1.0-alpha.1`
candidate passed its
technical staging, exact-client calibration, disabled-control, and physical
rollback gates on 2026-08-16. The owner explicitly accepted the candidate's
visual result on 2026-08-16 and authorized publication as the immutable
`0.1.0-alpha.1` prerelease. That acceptance does not authorize production
deployment or establish a supported production release.

## Exact contract

Activation requires both byte-exact operator-installed artifacts:

- `connectedglass-1.1.14-neoforge-mc1.21.jar`, 819,976 bytes, SHA-256
  `e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe`;
- `fusion-1.3.12-neoforge-mc1.21.1.jar`, 923,270 bytes, SHA-256
  `17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa`.

The generated profile owns all 119 placed `connectedglass:*` block IDs and
exactly 1,700 legal states:

| Shape | IDs | Legal states |
| --- | ---: | ---: |
| Full cube | 68 | 68 |
| Pane | 51 | 1,632 |
| **Total** | **119** | **1,700** |

The structural closure is 737 operator-installed paths: 119 blockstates, 430
models (425 placed Fusion programs plus five pane parents), 119 PNGs, 68
PIECED metadata files, and one 51-target pane modifier. Three exact Minecraft
host models form a separate geometry ABI. The add-on bundles none of those
third-party resources.

## Rendering behavior

The renderer preserves BlueMap's original blockstate selection, multipart
geometry, model/variant transforms, UV rotation and lock, AO, lighting, cave
removal, top-only rendering, map color, alpha, and capacity failures. It
supports the two layouts present in this exact profile:

- 68 80x16 PIECED sheets, selected from the eight-neighbor connection mask;
- 51 16x16 plain pane-edge textures.

The bounded predicate interpreter accepts only `fusion:or`,
`fusion:is_direction`, `fusion:match_state`, and `fusion:is_same_block`.
Same-block comparisons intentionally ignore `waterlogged`, while the route
itself accepts only the exact five-property pane schema. Full cubes accept no
properties.

Same-ID full cubes cull shared faces. Pane arm ends cull only across reciprocal
native arms. Vertical pane caps are removed per overlapping geometric piece;
the representative two-layer straight and cross pane stacks matched the exact
client on 2026-08-16, with no internal horizontal caps. This calibration
remains a required regression gate for any changed profile or renderer.

Any tuple, structural-resource, host-ABI, or registry mismatch leaves the
whole route inactive. An invalid individual state or render observation
atomically discards partial geometry and uses BlueMap's stock path.
`MaxCapacityReachedException` propagates unchanged. Dimension-preserving PNG
pixel overrides remain supported; structural overrides do not.

The shared module supplies axis arithmetic, direction masks, texture
orientation, layout names, and sheet selection. `TextureLayout` remains local
and maps by enum name at the selector call. Only `PLAIN` and `PIECED` are
admitted by this profile.

## Technical validation status

The accepted `0.1.0-alpha.3` production JAR is 162,427 bytes with SHA-256
`a4ee3f4e398f2bdec3739724027d785e2697417dad92d73dcdb06bbd2a7df240`.
On the reusable disposable host, the 2026-08-16 lifecycle established:

- an active exact-profile route with all 425 programs after byte-exact input
  and BlueMap pack-root-order checks;
- all eight gallery cells, 71 placements, and 72 observations verified with
  zero failed cells and zero failures, followed by a completed BlueMap render;
- agreement between the exact client and BlueMap for the representative cube,
  pane, and two-layer vertical-pane cases;
- an `operator-disabled` restart control that restored the expected incorrect
  stock Connected Glass rendering; and
- physical add-on/alias removal, clean restart, and successful stock rerender,
  after which the disposable Deployment was scaled to zero with no Pods.

The agent-side BlueMap sanity check passed while the active candidate was
rendered. The later rollback deliberately replaced that output with the stock
control, so it is not a current review endpoint. After reviewing the active
gallery presentation, the owner explicitly accepted the exact frozen
candidate on 2026-08-16 and authorized its immutable `0.1.0-alpha.1`
prerelease publication. This is release authorization only, not production
deployment authorization. See [docs/STAGING.md](docs/STAGING.md) and
[docs/ROLLBACK.md](docs/ROLLBACK.md).

## Generate and validate

Java 21 and the exact local BlueMap backport are required. Example exact local
inputs follow. Clone with `--recurse-submodules`, or initialize an existing
checkout with `git submodule update --init --recursive`, before invoking
Gradle. The settings preflight rejects missing, dirty, staged, wrong-commit,
or source-tree-mismatched Adapter API and Fusion module checkouts.

```bash
connectedglass_jar='/absolute/path/connectedglass-1.1.14-neoforge-mc1.21.jar'
fusion_jar='/absolute/path/fusion-1.3.12-neoforge-mc1.21.1.jar'

python3 tools/verify_pinned_artifacts.py \
  --connectedglass "$connectedglass_jar" --fusion "$fusion_jar"
python3 gallery/generate.py --check \
  --connectedglass-jar "$connectedglass_jar" --fusion-jar "$fusion_jar"
(cd gallery && sha256sum --check SHA256SUMS)
python3 -m unittest discover -s tools/tests -p 'test_*.py'
python3 -m unittest discover -s gallery/tests -p 'test_*.py'

gradle --no-daemon \
  -PbluemapSourcePath=/absolute/path/BlueMap \
  -PconnectedglassJar="$connectedglass_jar" \
  -PfusionJar="$fusion_jar" \
  clean check build generatePomFileForAddonPublication \
  generateMetadataFileForAddonPublication verifyPinnedArtifacts
```

The binary and sources JAR gates require the exact shared class/source roster
once and reject displaced local types, upstream namespaces, assets, data,
foreign classes, and nested archives. The sealed `0.1.0-alpha.3` publication
payload identities are recorded in `provenance/release.json`.

## Gallery

`gallery/` deterministically generates eight representative cells with 71
placements and 72 exact observations. It covers isolated and connected cubes,
an L-shaped missing diagonal, family/color boundaries, isolated/straight/L/T/
cross panes, two-layer pane stacks, mixed-ID pane joins, a waterlogged same-ID
pane, and untouched vanilla controls. See [gallery/README.md](gallery/README.md).

## Licensing

Project code is MIT. BlueMap-derived MIT renderer mechanics retain attribution.
Connected Glass and Fusion both declare All Rights Reserved and are exact
runtime inputs only; no upstream code, JSON, models, textures, metadata, or
binaries are redistributed. See [LICENSE-BlueMap](LICENSE-BlueMap),
[THIRD_PARTY.md](THIRD_PARTY.md), and
[docs/PROVENANCE.md](docs/PROVENANCE.md).

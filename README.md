# BlueMap Connected Glass Add-on

This standalone MIT BlueMap add-on restores the connected textures and pane
models installed by Connected Glass 1.1.14 and Fusion 1.3.12 on the exact All
the Mons 1.2.0 baseline. It is currently under implementation and is not yet a
published or owner-accepted release.

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
the representative two-layer pane cases remain a required exact-client
calibration before release.

Any tuple, structural-resource, host-ABI, or registry mismatch leaves the
whole route inactive. An invalid individual state or render observation
atomically discards partial geometry and uses BlueMap's stock path.
`MaxCapacityReachedException` propagates unchanged. Dimension-preserving PNG
pixel overrides remain supported; structural overrides do not.

## Generate and validate

Java 21 and the exact local BlueMap backport are required. Example exact local
inputs:

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

The binary and sources JAR gates reject upstream namespaces, assets, data,
classes, and nested archives.

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

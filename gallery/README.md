# Connected Glass staging gallery

This deterministic datapack is the representative visual fixture for the exact
All the Mons 1.2.0 Connected Glass 1.1.14 plus Fusion 1.3.12 renderer. It has
eight cells, 71 placed subject blocks, and 72 exact observations. The extra
observation locks the intentional air diagonal in cell 2.

| Cell | Contract |
| ---: | --- |
| 1 | `clear_glass` isolated cube and 3x3 wall |
| 2 | `scratched_glass_red` L wall with its corner diagonal missing |
| 3 | `tinted_borderless_glass` 2x2 wall beside vanilla stone |
| 4 | Same-ID clear pair followed by colored and borderless cube boundaries |
| 5 | `clear_glass_pane` isolated, straight, L, T, and cross topologies |
| 6 | Two-high straight and cross `borderless_glass_red_pane` stacks |
| 7 | Mixed-ID pane boundary and a contained, waterlogged same-ID pane cross |
| 8 | Vanilla glass pair, isolated vanilla glass pane, and stone controls |

The placement census is 23 Connected Glass cubes, 40 Connected Glass panes,
and eight vanilla controls. Every pane observation names all five legal state
properties (`east`, `north`, `south`, `west`, and `waterlogged`). Cell 7 keeps
the mixed pane IDs geometrically joined, as inherited from `IronBarsBlock`,
while preserving their different block identities for the renderer predicate.

## Evidence and generation

The selected IDs, cube variant shape, and pane multipart directions were
derived from the operator-installed 819,976-byte
`connectedglass-1.1.14-neoforge-mc1.21.jar`, SHA-256
`e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe`.
The paired Fusion input is the 923,270-byte
`fusion-1.3.12-neoforge-mc1.21.1.jar`, SHA-256
`17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa`.

Regenerate with optional byte-exact source verification, then check the
checked-in outputs:

```bash
python3 gallery/generate.py \
  --connectedglass-jar /absolute/path/connectedglass-1.1.14-neoforge-mc1.21.jar \
  --fusion-jar /absolute/path/fusion-1.3.12-neoforge-mc1.21.1.jar
python3 gallery/generate.py --check
(cd gallery && sha256sum --check SHA256SUMS)
python3 -m unittest discover -s gallery/tests -p 'test_*.py'
```

`cases.json` and `cases.tsv` are the canonical coordinate/state manifests.
The generator owns those manifests, every function, `pack.mcmeta`, the load
tag, and `SHA256SUMS`; do not hand-edit them.

## Staging use

Package into the canonical
`bluemap-connectedglass-gallery-atmons-1.2.0.zip` name:

```bash
gallery/package.sh /absolute/output/directory
```

Install that ZIP only in a disposable All the Mons 1.2.0 staging world, reload
datapacks, and run:

```text
/function connectedglass_gallery:build
/function connectedglass_gallery:verify
/function connectedglass_gallery:status
/function connectedglass_gallery:pose
```

`build` also runs `verify`. Acceptance requires `cells=8`, `placements=71`,
`checked=72`, `failed_cells=0`, and `failures=0`. The fixture occupies the
overworld cuboid from `189 100 201` through `251 106 231`; its review center is
`220 100 216`. Build force-loads the 15 intersecting chunks so console-driven
placement and rendering are stable. When the disposable review is finished,
run:

```text
/function connectedglass_gallery:release
```

`release` clears that exact cuboid and removes its force-load range. It is not
a production-world cleanup command.

The datapack contains only first-party manifests/functions plus factual block
IDs, states, coordinates, and vanilla commands. It redistributes no Connected
Glass or Fusion JSON, models, textures, code, classes, metadata, or binaries.

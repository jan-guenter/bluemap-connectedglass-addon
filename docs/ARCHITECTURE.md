# Architecture

## Activation

```text
BlueMap ResourcePack construction
  -> verify exact Fusion model source gitlink, index, HEAD, clean state, and source tree
  -> detect exactly one Connected Glass 1.1.14 JAR and one Fusion 1.3.12 JAR
  -> validate first-wins 737-path structural closure
  -> validate three Minecraft host-model ABI paths
  -> compile exactly 425 bounded Fusion programs
  -> validate the synthetic dispatch model
  -> crop collision-safe local textures during ResourcePack bake
  -> activate the single process-scoped route
```

Every structural resource is size/SHA-256 locked. The first physical resource
winner is claimed before reading, so an unreadable higher-priority pack entry
cannot fall through to a lower root. PNG bytes may differ only when decoded
dimensions match the exact catalog.

## Route and state boundary

The generated allowlist contains 68 propertyless full cubes and 51 panes. A
pane state is legal only when its property set is exactly `north`, `east`,
`south`, `west`, and `waterlogged`, each with a Boolean string value. This is
the complete 1,700-state boundary. Unknown IDs or invalid property maps use the
original stock blockstate and properties.

## Model interpretation

The active blockstate is evaluated by BlueMap, preserving multipart selection
and rotations. The renderer then resolves the selected model to one of 425
exact programs. The predicate AST accepts only the four types present in the
installed closure. Missing cube `connections` means native same-block.

Plain 16x16 edge textures bypass neighbor-mask calculation. PIECED faces use
the face-local texture frame, evaluate eight neighbors, and either select a
whole 16x16 cell or split the polygon into four UV quadrants. Geometry,
lighting, tint, AO, cave/top-only behavior, map color, and UV-lock follow the
attributed BlueMap renderer mechanics.

Five neutral model types compile from the exact source-module gitlink into the
add-on JAR. The consumer-local `TextureLayout` maps by enum name only at the
selector call. Resource admission, profile parsing, predicates, tile catalogs,
route activation, fallback, and mesh emission remain local.

Same-ID full cubes cull shared faces. Pane arm ends cull only for reciprocal
native arms. For top/bottom pane quads, geometric centroid classifies the
center post or one cardinal arm; only the corresponding overlap in a same-ID
vertical neighbor is removed. On 2026-08-16, exact-client calibration passed
for both representative two-block-high straight and cross pane stacks: the
client and BlueMap each omitted the internal horizontal caps while retaining
the external geometry. Repeating this calibration remains mandatory after any
profile, modifier, or emitter change.

## Failure policy

Tuple, resource, program, dispatch, or generated-texture failure makes the
whole route inactive. Invalid per-block state/resource observations reset all
partial triangles and map color, then invoke BlueMap's stock multipart path.
The stock path uses BlueMap's per-variant premultiplied-color aggregation.
Capacity exceptions are never converted to fallback.

The add-on registers no blocks, items, entities, menus, commands, packets, or
required client resources. Removing its JAR and restarting restores stock
BlueMap behavior.

That removal invariant was exercised on the disposable host on 2026-08-16.
The active 425-program route, operator-disabled stock control, and physical-JAR
removal were each observed in separate clean starts; the final stock render
completed after prior add-on output and aliases were removed.

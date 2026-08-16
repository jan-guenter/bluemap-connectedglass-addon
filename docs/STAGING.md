# Disposable staging gate

The frozen 155,396-byte candidate with SHA-256
`eb1dc07a6f9906f83a710e175cb8c119f0464bda73f651fa13a6e24900ffb70e`
passed the technical disposable-host gate on 2026-08-16. This pass does not
include owner visual acceptance and does not authorize publication or
production use. Use only the reusable disposable BlueMap namespace/PVC
authorized by the workspace; never production.

## Observed 2026-08-16 pass

Clean init verified the exact Connected Glass, Fusion, add-on, and gallery
hashes. BlueMap resolved the pack roots in this order before the corresponding
add-on and mod roots:

```text
config/bluemap/packs/zz-0246-connectedglass.zip
config/bluemap/packs/zz-0049-fusion.zip
```

The read-only runtime probe reported:

```text
CONNECTEDGLASS_RUNTIME_SNAPSHOT route=connectedglass-fusion-1.1.14-1.3.12 state=ACTIVE detail=exact-profile catalogSize=425
```

Gallery build/verification reported `cells=8`, `placements=71`,
`observations=72`, `ready=1`, `checked=72`, `failed_cells=0`, `failures=0`,
and zero failures in each of cases 01 through 08. The forced BlueMap update
finished with no pending tasks and no tile, capacity, out-of-memory, inactive,
or fallback error from this route.

The exact All the Mons 1.2.0 client and the active BlueMap render agreed on the
representative custom cube and pane cells. In particular, the two-block-high
straight and cross pane stacks had no internal horizontal caps in either view.
An agent opened the exact active BlueMap URL and confirmed that the intended
map/view was not blank, black, missing, or grossly broken. This lightweight
check is not owner acceptance.

The restart-scoped disabled control reported an inactive
`operator-disabled` route with `catalogSize=null` and produced the expected
incorrect stock Connected Glass geometry. Physical removal then removed the
add-on, both aliases, and prior map output; a clean stock startup and forced
render completed with 23 tile files and no relevant errors. The Deployment was
finally scaled to zero and its Pods removed. Consequently, the prior public
active render is no longer a live candidate-review endpoint.

## Reproduction and owner-acceptance gate

Before starting:

1. freeze and independently audit a clean production JAR;
2. verify the exact Connected Glass, Fusion, BlueMap, add-on, and gallery
   identities;
3. stop/scale the disposable host to zero before changing its PVC;
4. configure the workspace's stable no-time/weather/ticks/mobs/damage staging
   baseline;
5. install only the exact candidate and deterministic gallery;
6. prove pack-root priority and route activation from retained logs/state.

Run the gallery from console:

```text
function connectedglass_gallery:build
function connectedglass_gallery:verify
function connectedglass_gallery:status
bluemap force-update connectedglass_staging
bluemap tasks
```

Require `cells=8`, `placements=71`, `checked=72`, `failed_cells=0`, and
`failures=0`, followed by a completed map render with no tile exception.
Inspect both two-layer pane stacks against the exact client before accepting a
changed candidate's vertical-cap behavior. Also inspect all other custom cells
and unchanged vanilla controls, then open the exact BlueMap URL for a
lightweight sanity check and obtain explicit owner visual acceptance.

Finally perform a restart-scoped disable/stock comparison and a
physical-removal plus clean-restart rollback. The disable property is read at
startup; it is not a same-JVM toggle. Record exact commit/JAR/gallery identities
and only the tests actually observed. The exact zero-replica manifests and
runbook are in `lab/`.

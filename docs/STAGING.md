# Disposable staging gate

No staging pass is accepted yet. Use only the reusable disposable BlueMap
namespace/PVC authorized by the workspace; never production.

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
Inspect both two-layer pane stacks against the exact client before accepting
vertical cap behavior. Also inspect all other custom cells and unchanged
vanilla controls, then open the exact BlueMap URL for a lightweight sanity
check and obtain owner visual acceptance.

Finally perform a restart-scoped disable/stock comparison and a
physical-removal plus clean-restart rollback. The disable property is read at
startup; it is not a same-JVM toggle. Record exact commit/JAR/gallery identities
and only the tests actually observed. The exact zero-replica manifests and
runbook are in `lab/`.

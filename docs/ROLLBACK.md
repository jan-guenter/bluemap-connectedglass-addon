# Rollback

The add-on owns no persisted world or BlueMap state. To restore stock behavior:

1. stop or scale the disposable server to zero;
2. remove only the exact Connected Glass add-on JAR;
3. remove only the two BlueMap pack aliases and the disposable
   `connectedglass_staging` rendered map output;
4. keep the gallery/map configuration temporarily and restart with the original
   Connected Glass and Fusion mod JARs untouched;
5. force a clean stock BlueMap render and verify the vanilla controls plus the
   expected stock Connected Glass mismatch.

The operator-disable property
`bluemap.connectedglass.disabledProfiles=connectedglass-fusion-1.1.14-1.3.12`
is useful for a restart-scoped comparison, but is not a same-JVM toggle.
Physical JAR removal plus restart is the required rollback proof. Never delete
a namespace, PVC, PV, or production map as part of this project rollback.

## Observed 2026-08-16 proof

The restart-scoped control started with the exact candidate still installed.
Its read-only runtime snapshot reported route
`connectedglass-fusion-1.1.14-1.3.12` as `INACTIVE`, detail
`operator-disabled`, and `catalogSize=null`. The stock render completed and
showed the expected sliced texture-sheet and pane-geometry mismatch, proving
that the active candidate had materially changed the Connected Glass result.

At zero replicas, the physical rollback patch then removed the exact add-on
JAR, both BlueMap pack aliases, and the previous rendered map output. Init
reported `CONNECTEDGLASS_ADDON_REMOVED`; filesystem checks confirmed those
targets absent while the original Connected Glass and Fusion JARs remained.
Minecraft and BlueMap restarted cleanly without add-on discovery or baking,
and the forced stock render completed with no pending tasks, 23 tile files,
and no relevant tile, capacity, out-of-memory, or add-on errors. The Deployment
was scaled back to zero and its Pod deleted. No namespace, PVC, PV, or
production state was removed.

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

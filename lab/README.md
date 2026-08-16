# Disposable Connected Glass staging

This directory targets only the existing disposable
`bluemap-sophisticated-staging` host and PVC. It is not a production
deployment. Keep `deployment/minecraft` at zero replicas while uploading or
patching, and never delete the namespace, PVC, PV, or original mod JARs.

The frozen candidate inputs are:

- add-on JAR: 155,396 bytes, SHA-256
  `eb1dc07a6f9906f83a710e175cb8c119f0464bda73f651fa13a6e24900ffb70e`;
- gallery ZIP: 11,686 bytes, SHA-256
  `3d1d004acab93d725e4437d3d900a884b2a113caaeb04025b9c15030eaa12f78`;
- Connected Glass 1.1.14: 819,976 bytes, SHA-256
  `e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe`;
- Fusion 1.3.12: 923,270 bytes, SHA-256
  `17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa`.

The original Connected Glass and Fusion JARs remain in `/data/mods`. Two
`.zip`-named symlinks expose those exact files to BlueMap in reverse-sorted
client priority without duplicating their All Rights Reserved bytes. The
add-on and gallery are uploaded to the private
`/data/.bluemap-sophisticated-staging` directory and hash-verified before use.

## Controlled sequence

Use kubeconfig `/root/.kube/guenter-cloud`, context `guenter.cloud`, and
namespace `bluemap-sophisticated-staging` for every command.

1. Scale `deployment/minecraft` to zero and wait for every Minecraft Pod to
   disappear.
2. Delete any old `stone-artifact-loader` and `connectedglass-artifact-loader`
   Pods with `--ignore-not-found --wait`.
3. Apply `kubernetes/config.yaml`, `kubernetes/pins.yaml`, and
   `kubernetes/artifact-loader.yaml`; wait for `READY_FOR_UPLOAD`.
4. Copy the frozen add-on and gallery to `.part` names below
   `/data/.bluemap-sophisticated-staging`, atomically rename them, create
   `.connectedglass-upload-complete`, and require
   `LOCAL_ARTIFACTS_VERIFIED`.
5. Delete the loader and wait for its Pod to disappear so the RWO PVC is free.
6. Server-dry-run the Deployment, disabled-control, rollback, and Ingress
   patches. Apply the Deployment only with the strategic patch command below;
   it is intentionally not a standalone Deployment manifest.
7. Confirm the merged Deployment still has zero replicas, no Stone pose
   variables/annotations, the Connected Glass ConfigMaps, and exactly the new
   install script. Patch the Ingress, then scale to one.
8. Require clean init hashes/startup and BlueMap root order
   `zz-0246-connectedglass.zip`, then `zz-0049-fusion.zip` before the mod roots.
9. Run the gallery commands in `docs/STAGING.md`, force-update
   `connectedglass_staging`, and wait for no pending BlueMap tasks.
10. Inspect `https://bluemap-connectedglass.guenter.cloud/`, including the two
    vertical pane-stack cases, and compare them against the exact client.
11. Run the restart-scoped disabled control with
    `disabled-deployment-patch.yaml`; this is not a live same-JVM toggle.
12. Perform the physical-removal rollback proof. The rollback deliberately
    keeps the gallery and map configuration for a clean stock comparison, but
    removes the add-on, its two aliases, and the prior rendered map output.
13. Scale back to zero when review and rollback evidence are complete.

```bash
kubectl --kubeconfig /root/.kube/guenter-cloud --context guenter.cloud \
  -n bluemap-sophisticated-staging patch deployment minecraft \
  --type=strategic --patch-file kubernetes/deployment-patch.yaml

kubectl --kubeconfig /root/.kube/guenter-cloud --context guenter.cloud \
  -n bluemap-sophisticated-staging patch ingress \
  bluemap-sophisticated-review-public --type=strategic \
  --patch-file kubernetes/ingress-patch.yaml

# Restart-scoped stock control, only while the Deployment is at zero:
kubectl --kubeconfig /root/.kube/guenter-cloud --context guenter.cloud \
  -n bluemap-sophisticated-staging patch deployment minecraft \
  --type=strategic --patch-file kubernetes/disabled-deployment-patch.yaml

# Physical rollback, only while the Deployment is at zero:
kubectl --kubeconfig /root/.kube/guenter-cloud --context guenter.cloud \
  -n bluemap-sophisticated-staging patch deployment minecraft \
  --type=strategic --patch-file kubernetes/rollback-deployment-patch.yaml
```

The performance datapack maps the workspace policy to the available vanilla
1.21.1 gamerules, including `disableElytraMovementCheck=true`. Vanilla has no
`spawnerBlocksWork` gamerule; the flat structure-free disposable world and
bounded cleared fixture are the enforceable equivalent for this run.

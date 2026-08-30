# ADR 0001: source-bundle the stable Fusion model helpers

- Status: supersedes the first-release repository-local decision
- Date: 2026-08-30

## Decision

Pin BlueMap Fusion Resource Models `0.1.0-alpha.1` as an exact source
submodule. Compile its five neutral model types into this add-on, while keeping
the exact generated `connectedglass:*` allowlist and every runtime policy
local. The module is not an installed service or nested JAR.

## Rationale

Connected Glass, Glassential, Rechiseled, and Rechiseled Create now provide
accepted, independently reviewed evidence for the same axis, direction,
orientation, and selector behavior. The module contains that stable code only.
Connected Glass remains the independent two-layout pilot and maps its local
layout enum by name.

Predicate schemas, multipart panes, state validation, culling, resource
admission, catalogs, routes, fallback, and emitters remain consumer-specific.
The exact gitlink, checkout HEAD, clean state, and source tree fail closed
before Gradle loads the shared sources.

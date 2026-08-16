# ADR 0001: keep the Fusion interpreter repository-local

## Decision

Keep the adapted MIT Fusion interpreter source in this standalone Connected
Glass add-on for the first release. It owns only the exact generated
`connectedglass:*` allowlist and provides no runtime service to other add-ons.

## Rationale

Rechiseled and Connected Glass are now two consumers, but their exact product
contracts differ materially: layout roster, predicate schema, multipart panes,
state validation, and culling rules. Extracting a shared artifact before both
implementations are independently accepted would freeze the wrong boundary and
couple rollback/release mechanics.

After Connected Glass and the next Glassential consumer are accepted, compare
the three reviewed implementations. Only then consider a separate stable MIT
source module. Fusion remains a source interpreter, never an installed block
owner or runtime provider.

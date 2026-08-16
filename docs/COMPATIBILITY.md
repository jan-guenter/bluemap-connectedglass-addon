# Compatibility contract

Supported only for this exact tuple:

- All the Mons 1.2.0, pack commit
  `c7bb230f21d14d26859d0b92548f089b3a493ad9`;
- Minecraft 1.21.1, NeoForge 21.1.248, Java 21;
- BlueMap backport commit `9be321df995a1103808621d529eb72773e719d4d`;
- Connected Glass 1.1.14, 819,976 bytes, SHA-256 `e5b2a1cd...d49fe`;
- Fusion 1.3.12, 923,270 bytes, SHA-256 `17f52156...f2fa`.

This is an evidence lock, not a range claim. A pack, mod, Minecraft, loader,
or BlueMap change requires a fresh artifact/resource census, regenerated
profile, tests, staging render, rollback test, version change, and review.

Dimension-preserving PNG pixel overrides are supported. Structural model,
blockstate, metadata, modifier, and host-model overrides deactivate the route.
No arbitrary resource-pack, Connected Glass fork, Fusion version, or other
namespace is claimed.

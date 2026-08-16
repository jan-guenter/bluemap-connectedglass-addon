#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fail-closed review gate for exact Connected Glass 1.1.14/Fusion 1.3.12."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import zipfile

import generate_profile


def _verify_mod_metadata(connectedglass: Path, fusion: Path) -> None:
    with zipfile.ZipFile(connectedglass) as archive:
        try:
            metadata = archive.read("META-INF/neoforge.mods.toml")
        except KeyError as error:
            raise ValueError("missing ConnectedGlass NeoForge metadata") from error
        if (b'modId = "connectedglass"' not in metadata
                or b'version = "1.1.14"' not in metadata
                or b'license = "All rights reserved"' not in metadata):
            raise ValueError("ConnectedGlass NeoForge metadata identity changed")
        names = archive.namelist()
        if not any(name.startswith("assets/connectedglass/") for name in names):
            raise ValueError("ConnectedGlass archive has no installed resource root")
        if not any(
            name.startswith("com/supermartijn642/connectedglass/") for name in names
        ):
            raise ValueError("ConnectedGlass archive has no expected implementation package")
        if any(name.startswith("com/supermartijn642/fusion/") for name in names):
            raise ValueError("ConnectedGlass archive unexpectedly embeds Fusion classes")

    with zipfile.ZipFile(fusion) as archive:
        names = archive.namelist()
        if "META-INF/neoforge.mods.toml" not in names:
            raise ValueError("Fusion archive has no NeoForge metadata")
        metadata = archive.read("META-INF/neoforge.mods.toml")
        if (b'modId = "fusion"' not in metadata
                or b'version = "1.3.12"' not in metadata
                or b'license = "All rights reserved"' not in metadata):
            raise ValueError("Fusion NeoForge metadata identity changed")
        if not any(name.startswith("com/supermartijn642/fusion/") for name in names):
            raise ValueError("Fusion archive has no expected implementation package")


def verify(connectedglass: Path, fusion: Path) -> None:
    outputs = generate_profile.build_outputs(connectedglass, fusion)
    generate_profile.write_or_check(outputs, check=True)
    _verify_mod_metadata(connectedglass, fusion)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connectedglass", required=True, type=Path)
    parser.add_argument("--fusion", required=True, type=Path)
    args = parser.parse_args()
    try:
        verify(args.connectedglass, args.fusion)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"artifact verification failed: {error}", file=sys.stderr)
        return 1
    print(
        "Verified exact Connected Glass 1.1.14 + Fusion 1.3.12 artifacts, "
        "119 routed definitions, 1,700 legal states, and the 737-path "
        "metadata-only closure."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

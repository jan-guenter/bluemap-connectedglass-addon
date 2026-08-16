# SPDX-License-Identifier: MIT
"""Contract tests for the deterministic representative gallery."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest


GALLERY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "connectedglass_gallery_generate", GALLERY / "generate.py"
)
assert SPEC is not None and SPEC.loader is not None
GENERATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GENERATOR
SPEC.loader.exec_module(GENERATOR)


class GalleryGeneratorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = GENERATOR.cases()

    def test_exact_representative_census(self) -> None:
        self.assertEqual(
            {
                "cells": 8,
                "connected_glass_cube_placements": 23,
                "connected_glass_pane_placements": 40,
                "negative_space_observations": 1,
                "observations": 72,
                "placements": 71,
                "vanilla_placements": 8,
                "waterlogged_panes": 1,
            },
            GENERATOR.counts(self.cases),
        )
        self.assertEqual(
            {
                "connectedglass:borderless_glass",
                "connectedglass:borderless_glass_pane",
                "connectedglass:borderless_glass_red_pane",
                "connectedglass:clear_glass",
                "connectedglass:clear_glass_pane",
                "connectedglass:clear_glass_red",
                "connectedglass:clear_glass_red_pane",
                "connectedglass:scratched_glass_red",
                "connectedglass:tinted_borderless_glass",
            },
            GENERATOR.source_block_ids(self.cases),
        )

    def test_all_panes_have_complete_states(self) -> None:
        pane_states = [
            observation.block_state
            for case in self.cases
            for observation in case.observations
            if "pane" in observation.block_state
        ]
        self.assertEqual(41, len(pane_states))
        for state in pane_states:
            properties = state.split("[", 1)[1].removesuffix("]").split(",")
            self.assertEqual(
                ["east", "north", "south", "waterlogged", "west"],
                [property_.split("=", 1)[0] for property_ in properties],
            )

    def test_mixed_panes_connect_geometrically(self) -> None:
        mixed = self.cases[6].observations[:3]
        self.assertIn("east=true", mixed[0].block_state)
        self.assertIn("east=true", mixed[1].block_state)
        self.assertIn("west=true", mixed[1].block_state)
        self.assertIn("west=true", mixed[2].block_state)

    def test_generated_manifest_matches_checked_in_rows(self) -> None:
        payload = json.loads((GALLERY / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual(GENERATOR.counts(self.cases), payload["counts"])
        self.assertEqual(8, len(payload["cases"]))
        self.assertEqual(
            73,
            len((GALLERY / "cases.tsv").read_text(encoding="utf-8").splitlines()),
        )

    def test_generation_is_byte_deterministic_and_asset_free(self) -> None:
        first = GENERATOR.generated_files(self.cases)
        second = GENERATOR.generated_files(GENERATOR.cases())
        self.assertEqual(first, second)
        for path in first:
            lowered = path.as_posix().lower()
            self.assertFalse(lowered.endswith((".class", ".jar", ".png")))
            self.assertNotIn("assets/connectedglass", lowered)
            self.assertNotIn("assets/fusion", lowered)


if __name__ == "__main__":
    unittest.main()

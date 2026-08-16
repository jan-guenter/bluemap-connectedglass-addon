# SPDX-License-Identifier: MIT
"""Unit coverage for deterministic fail-closed profile generation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "generate_profile", ROOT / "tools/generate_profile.py"
)
assert SPEC is not None and SPEC.loader is not None
generate_profile = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generate_profile)


class ProfileHelpersTest(unittest.TestCase):
    def test_roster_digest_is_sorted_and_newline_terminated(self) -> None:
        self.assertEqual(
            generate_profile.roster_digest(["z", "a"]),
            generate_profile.digest_bytes(b"a\nz\n"),
        )

    def test_resource_path_rejects_parent_escape(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsafe resource key"):
            generate_profile.resource_path("connectedglass:../escape", "models", ".json")

    def test_identity_gate_rejects_wrong_filename_before_hashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.jar"
            path.write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "unexpected artifact path"):
                generate_profile._verify_identity(  # noqa: SLF001 - exact helper test
                    path,
                    filename="expected.jar",
                    size=0,
                    sha1="",
                    sha256="",
                    sha512="",
                )

    def test_canonical_json_is_order_independent(self) -> None:
        self.assertEqual(
            generate_profile.canonical_json({"b": 2, "a": 1}),
            b'{\n  "a": 1,\n  "b": 2\n}\n',
        )

    def test_full_profile_constants_lock_exact_closure(self) -> None:
        self.assertEqual(119, generate_profile.ROUTED_COUNT)
        self.assertEqual(1_700, generate_profile.ROUTED_STATE_COUNT)
        self.assertEqual(425, generate_profile.DIRECT_MODEL_COUNT)
        self.assertEqual(430, generate_profile.MODEL_COUNT)
        self.assertEqual(119, generate_profile.PNG_COUNT)
        self.assertEqual(68, generate_profile.MCMETA_COUNT)
        self.assertEqual(1, generate_profile.MODIFIER_COUNT)
        self.assertEqual(737, generate_profile.RESOURCE_COUNT)
        self.assertEqual(3, generate_profile.HOST_MODEL_COUNT)
        host_rows = "".join(
            f"model\t{path}\t{size}\t{sha256}\n"
            for path, size, sha256 in generate_profile.HOST_MODELS
        ).encode("ascii")
        self.assertEqual(
            "7eddb8d22e773bea816d180e8fe93d89ab7e0bd770e8520a0eb15b6a573d0230",
            generate_profile.digest_bytes(host_rows),
        )
        self.assertEqual(
            "651a2b74e897295353e6a53f950fbbd14dba8859623007060d5036a3b972b042",
            generate_profile.PATH_CLOSURE_DIGEST,
        )

    def test_exact_shape_and_program_census(self) -> None:
        self.assertEqual(68, generate_profile.FULL_COUNT)
        self.assertEqual(51, generate_profile.PANE_COUNT)
        self.assertEqual(
            {"default": 68, "same_block": 153, "pane_side": 204},
            generate_profile.PROGRAM_COUNTS,
        )
        self.assertEqual(
            {"pieced": (68, 80, 16), "plain": (51, 16, 16)},
            generate_profile.LAYOUTS,
        )


if __name__ == "__main__":
    unittest.main()

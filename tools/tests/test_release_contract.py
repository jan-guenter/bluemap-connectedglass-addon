# SPDX-License-Identifier: MIT
"""Static release-boundary regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha3_candidate_locks_modules_and_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.3", release["version"])
        self.assertEqual("v0.1.0-alpha.3", release["tag"])
        self.assertEqual(
            "e81f08bc4bfbf02d810ec8949a019130e2e61634",
            release["adapter_api_migration"]["commit"],
        )
        self.assertEqual(
            "2f974c9bb2ba13888d69682f86f30f58922d30eb",
            release["adapter_api_migration"]["source_tree"],
        )
        self.assertEqual(
            "3ddd5d39bb7cc8664c242aedd849a636316075c2",
            release["fusion_source_migration"]["commit"],
        )
        self.assertEqual(
            "6e85031ff2f0e7417a7a2fb0babbf7ed5a4f218a",
            release["fusion_source_migration"]["source_tree"],
        )
        self.assertEqual(
            {
                "production_jar",
                "sources_jar",
                "pom",
                "gradle_module",
            },
            set(release["final_release_artifacts"]),
        )
        self.assertEqual(
            {
                "file_name": "bluemap-connectedglass-addon-0.1.0-alpha.3.jar",
                "size": 162_427,
                "sha256": (
                    "a4ee3f4e398f2bdec3739724027d785e2697417dad92d73dcdb06bbd2a7df240"
                ),
            },
            release["final_release_artifacts"]["production_jar"],
        )


if __name__ == "__main__":
    unittest.main()

# SPDX-License-Identifier: MIT
"""Static release-boundary regression coverage."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ReleaseContractTest(unittest.TestCase):
    def test_alpha2_candidate_locks_module_and_all_publication_payloads(self) -> None:
        release = json.loads((ROOT / "provenance/release.json").read_text())
        self.assertEqual("owner-accepted-release-candidate", release["status"])
        self.assertEqual("0.1.0-alpha.2", release["version"])
        self.assertEqual("v0.1.0-alpha.2", release["tag"])
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
                "file_name": "bluemap-connectedglass-addon-0.1.0-alpha.2.jar",
                "size": 158_546,
                "sha256": (
                    "f73841c78da88808bbb9a5a630526e75902a2c56bfc9f7600ccbc39d3572e446"
                ),
            },
            release["final_release_artifacts"]["production_jar"],
        )


if __name__ == "__main__":
    unittest.main()

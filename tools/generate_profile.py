#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the metadata-only exact Connected Glass/Fusion rendering profile.

The generator consumes the operator-supplied, hash-pinned runtime artifacts.
It emits only identities, hashes, allowlists, and compact format metadata; no
third-party JSON, model, texture, class, source, or binary is redistributed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import struct
from typing import Any, Iterable
import zipfile


PROFILE_ROOT = Path("src/main/resources/bluemap-connectedglass/profiles")
PROFILE_DIRECTORY = PROFILE_ROOT / "connectedglass/1.1.14-fusion-1.3.12"
CATALOG_PATH = PROFILE_ROOT / "exact-artifacts.json"
PROFILE_PATH = PROFILE_DIRECTORY / "profile.json"
DEFINITIONS_PATH = PROFILE_DIRECTORY / "definitions.tsv"
RESOURCES_PATH = PROFILE_DIRECTORY / "required-resources.tsv"
TEXTURES_PATH = PROFILE_DIRECTORY / "textures.tsv"
HOST_MODELS_PATH = PROFILE_DIRECTORY / "host-models.tsv"

CONNECTEDGLASS_FILENAME = "connectedglass-1.1.14-neoforge-mc1.21.jar"
CONNECTEDGLASS_SIZE = 819_976
CONNECTEDGLASS_SHA1 = "0a44c13d6744e0eeec5bf38f58756a8e86e96f55"
CONNECTEDGLASS_SHA256 = "e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe"
CONNECTEDGLASS_SHA512 = (
    "c0db64151d850d568386b4c287e75fa882a4590802a0a9bc0eec7d47240e56dbc"
    "3215b4edede97204d7817afc097cba5e438a66eb58b956213b2289e342823a5"
)
FUSION_FILENAME = "fusion-1.3.12-neoforge-mc1.21.1.jar"
FUSION_SIZE = 923_270
FUSION_SHA1 = "79c0c6b6a2d9c9a04298df9a88bb71a93e885235"
FUSION_SHA256 = "17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa"
FUSION_SHA512 = (
    "a13d2a654988f021106f8a455134da1b515872e9122cf70bda064e663749f1c11"
    "aeddc3def23a621e236f2ffeefb6f56b15c2c63eeb2bca5f9833c5a2dc23a93"
)

ALL_BLOCKSTATES_COUNT = 119
ROUTED_COUNT = 119
FULL_COUNT = 68
PANE_COUNT = 51
ROUTED_STATE_COUNT = 1_700
DIRECT_MODEL_COUNT = 425
MODEL_COUNT = 430
PNG_COUNT = 119
MCMETA_COUNT = 68
MODIFIER_COUNT = 1
RESOURCE_COUNT = 737
HOST_MODEL_COUNT = 3

BLOCKSTATE_DIGEST = "42f516bb1847dab2d86aae75593c92c703e384d55a1ffe89de4ba787a9e80023"
FULL_DIGEST = "5ddf17a1451a8158b24b2923f6f25a03d9c334ae3682812d3a7c5607da08681b"
PANE_DIGEST = "e8addad49b35323bca21b2e951fb9f805e9d2bb160a88aa9c5d843a33b04d730"
DIRECT_MODEL_DIGEST = "61d9e6fd44a64e2f253ac05f8aba41056b9216f6cc38c9ac3eef2413f029b6fe"
MODEL_DIGEST = "a04e7bd6474af198a01c2e08c6a58a8629de46b65b8c741bec0da1e9846cc258"
PNG_DIGEST = "7f462b426c0b136c29364f0762afa183688d977b67c31a4e475ca7eb5c4be013"
MCMETA_DIGEST = "7e389fd428143f6b827391adc2d15f02a6ec8a4ac58caf13e1d436dfe0b46fcf"
MODIFIER_TARGET_DIGEST = (
    "445a71e4283a6b6943bae9825a02564a24f99892219b2029ddb650d480e98a60"
)
PATH_CLOSURE_DIGEST = (
    "651a2b74e897295353e6a53f950fbbd14dba8859623007060d5036a3b972b042"
)
LEGAL_STATE_DIGEST = "65a55b1ee27d4b90845e30fd41166a5c014cc3637b48788cb79c7eef34a7adb9"

PANE_MODIFIER_PATH = (
    "assets/connectedglass/fusion/model_modifiers/blocks/pane_culling_fix.json"
)
PANE_DIRECTIONS = ("north", "east", "south", "west")
DIAGONAL_DIRECTIONS = (
    "bottom_left",
    "bottom_right",
    "left",
    "right",
    "top_left",
    "top_right",
)
PREDICATE_TYPES = {
    "fusion:or",
    "fusion:is_direction",
    "fusion:match_state",
    "fusion:is_same_block",
}
PROGRAM_COUNTS = {"default": 68, "same_block": 153, "pane_side": 204}
LAYOUTS = {"pieced": (68, 80, 16), "plain": (51, 16, 16)}

MINECRAFT_CLIENT_SHA256 = (
    "499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99"
)
HOST_MODELS = (
    (
        "assets/minecraft/models/block/block.json",
        997,
        "3ef6c442f1ab55d2a57fa58e28bb831268159052659f12b453b637b31ded1da8",
    ),
    (
        "assets/minecraft/models/block/cube.json",
        584,
        "3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e",
    ),
    (
        "assets/minecraft/models/block/cube_all.json",
        227,
        "be3205d629ffb9e03834c3d1d083f8a2c62e9f9ae80820755129408634e9144a",
    ),
)


def digest_bytes(raw: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, raw).hexdigest()


def digest_path(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def roster_digest(values: Iterable[str]) -> str:
    payload = "".join(f"{value}\n" for value in sorted(values)).encode("utf-8")
    return digest_bytes(payload)


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode("ascii")


def resource_path(key: str, kind: str, suffix: str) -> str:
    if ":" in key:
        namespace, value = key.split(":", 1)
    else:
        namespace, value = "minecraft", key
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"unsafe resource key: {key}")
    return f"assets/{namespace}/{kind}/{value}{suffix}"


def _verify_identity(
    path: Path, *, filename: str, size: int, sha1: str, sha256: str, sha512: str
) -> None:
    if not path.is_file() or path.name != filename:
        raise ValueError(f"unexpected artifact path: {path}")
    if path.stat().st_size != size:
        raise ValueError(f"unexpected artifact size for {path}")
    for algorithm, expected in (
        ("sha1", sha1),
        ("sha256", sha256),
        ("sha512", sha512),
    ):
        actual = digest_path(path, algorithm)
        if actual != expected:
            raise ValueError(
                f"{path.name} {algorithm} changed: got {actual}, expected {expected}"
            )


def _model_key(value: str, default_namespace: str = "minecraft") -> str:
    return value if ":" in value else f"{default_namespace}:{value}"


def _path_for_model(model: str) -> str:
    return resource_path(model, "models", ".json")


def _path_for_texture(texture: str, suffix: str = ".png") -> str:
    return resource_path(texture, "textures", suffix)


def _walk_predicate(value: Any, found: set[str]) -> None:
    if isinstance(value, dict):
        predicate_type = value.get("type")
        if isinstance(predicate_type, str) and predicate_type.startswith("fusion:"):
            found.add(predicate_type)
        for child in value.values():
            _walk_predicate(child, found)
    elif isinstance(value, list):
        for child in value:
            _walk_predicate(child, found)


def _single_apply(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("model"), str):
        raise ValueError(f"{context} model application changed")
    if not set(value).issubset({"model", "x", "y", "uvlock"}):
        raise ValueError(f"{context} model application keys changed")
    for rotation in ("x", "y"):
        if rotation in value and value[rotation] not in (0, 90, 180, 270):
            raise ValueError(f"{context} model rotation changed")
    if "uvlock" in value and not isinstance(value["uvlock"], bool):
        raise ValueError(f"{context} uvlock changed")
    return value


def _parse_blockstate(
    block: str, value: Any
) -> tuple[str, int, list[dict[str, Any]], set[str], list[str]]:
    block_id = f"connectedglass:{block}"
    applications: list[dict[str, Any]] = []
    models: set[str] = set()
    legal_states: list[str] = []
    if isinstance(value, dict) and set(value) == {"variants"}:
        variants = value["variants"]
        if not isinstance(variants, dict) or list(variants) != [""]:
            raise ValueError(f"{block} full-cube blockstate schema changed")
        application = _single_apply(variants[""], block)
        applications.append({"selector": "", "apply": application})
        models.add(_model_key(application["model"], "connectedglass"))
        legal_states.append(f"{block_id}\t")
        return "full", 1, applications, models, legal_states

    if not isinstance(value, dict) or set(value) != {"multipart"}:
        raise ValueError(f"{block} blockstate root schema changed")
    multipart = value["multipart"]
    if not block.endswith("_pane") or not isinstance(multipart, list) or len(multipart) != 9:
        raise ValueError(f"{block} pane multipart schema changed")
    for index, part in enumerate(multipart):
        if not isinstance(part, dict) or not set(part).issubset({"apply", "when"}):
            raise ValueError(f"{block} multipart part changed")
        if "apply" not in part or (index > 0 and "when" not in part):
            raise ValueError(f"{block} multipart condition changed")
        if index == 0 and set(part) != {"apply"}:
            raise ValueError(f"{block} unconditional pane post changed")
        when = part.get("when")
        if when is not None:
            if (
                not isinstance(when, dict)
                or len(when) != 1
                or next(iter(when)) not in PANE_DIRECTIONS
                or next(iter(when.values())) not in ("true", "false")
            ):
                raise ValueError(f"{block} multipart predicate changed")
        application = _single_apply(part["apply"], block)
        applications.append({"when": when, "apply": application})
        models.add(_model_key(application["model"], "connectedglass"))
    if len(models) != 7:
        raise ValueError(f"{block} direct pane model roster changed")
    observed_conditions = [row["when"] for row in applications[1:]]
    expected_conditions = [
        {direction: state}
        for state in ("true", "false")
        for direction in PANE_DIRECTIONS
    ]
    if sorted(observed_conditions, key=canonical_json) != sorted(
        expected_conditions, key=canonical_json
    ):
        raise ValueError(f"{block} pane connection-state coverage changed")
    for bits in range(16):
        connections = [
            f"{direction}={str(bool(bits & (1 << index))).lower()}"
            for index, direction in enumerate(PANE_DIRECTIONS)
        ]
        for waterlogged in ("false", "true"):
            properties = sorted(connections + [f"waterlogged={waterlogged}"])
            legal_states.append(f"{block_id}\t{','.join(properties)}")
    return "pane", 32, applications, models, legal_states


def _classify_connections(model: str, value: dict[str, Any]) -> str:
    connections = value.get("connections")
    if connections is None:
        return "default"
    if set(connections) != {"type", "predicates"} or connections.get("type") != "fusion:or":
        raise ValueError(f"{model} connection root changed")
    predicates = connections.get("predicates")
    if not isinstance(predicates, list) or len(predicates) != 1:
        raise ValueError(f"{model} connection predicate count changed")
    child = predicates[0]
    if child == {"type": "fusion:is_same_block"}:
        return "same_block"
    if (
        not isinstance(child, dict)
        or set(child) != {"type", "predicates"}
        or child.get("type") != "fusion:or"
        or not isinstance(child.get("predicates"), list)
        or len(child["predicates"]) != 2
    ):
        raise ValueError(f"{model} pane-side connection predicate changed")
    match_state, is_direction = child["predicates"]
    if (
        not isinstance(match_state, dict)
        or set(match_state) != {"type", "block", "properties"}
        or match_state.get("type") != "fusion:match_state"
        or not isinstance(match_state.get("block"), str)
        or not isinstance(match_state.get("properties"), dict)
        or len(match_state["properties"]) != 1
    ):
        raise ValueError(f"{model} match-state predicate changed")
    property_name, allowed = next(iter(match_state["properties"].items()))
    if property_name not in PANE_DIRECTIONS or allowed != ["true"]:
        raise ValueError(f"{model} match-state property changed")
    expected_block = model.removesuffix(f"_side_{property_name}")
    if match_state["block"] != expected_block:
        raise ValueError(f"{model} match-state block changed")
    if is_direction != {
        "type": "fusion:is_direction",
        "directions": list(DIAGONAL_DIRECTIONS),
    }:
        raise ValueError(f"{model} direction predicate changed")
    return "pane_side"


def build_outputs(connectedglass: Path, fusion: Path) -> dict[Path, bytes]:
    _verify_identity(
        connectedglass,
        filename=CONNECTEDGLASS_FILENAME,
        size=CONNECTEDGLASS_SIZE,
        sha1=CONNECTEDGLASS_SHA1,
        sha256=CONNECTEDGLASS_SHA256,
        sha512=CONNECTEDGLASS_SHA512,
    )
    _verify_identity(
        fusion,
        filename=FUSION_FILENAME,
        size=FUSION_SIZE,
        sha1=FUSION_SHA1,
        sha256=FUSION_SHA256,
        sha512=FUSION_SHA512,
    )

    definitions: list[str] = []
    legal_states: list[str] = []
    full_paths: list[str] = []
    pane_paths: list[str] = []
    direct_models: set[str] = set()
    model_paths: set[str] = set()
    texture_keys: set[str] = set()
    png_paths: set[str] = set()
    metadata_paths: set[str] = set()
    predicate_types: set[str] = set()
    program_counts = {key: 0 for key in PROGRAM_COUNTS}
    layouts: dict[str, tuple[str, int, int, str]] = {}

    with zipfile.ZipFile(connectedglass) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Connected Glass JAR contains duplicate ZIP entries")
        available = set(names)
        blockstate_paths = sorted(
            path
            for path in available
            if path.startswith("assets/connectedglass/blockstates/")
            and path.endswith(".json")
        )
        if (
            len(blockstate_paths) != ALL_BLOCKSTATES_COUNT
            or roster_digest(blockstate_paths) != BLOCKSTATE_DIGEST
        ):
            raise ValueError("Connected Glass blockstate roster changed")

        for path in blockstate_paths:
            block = path.removeprefix(
                "assets/connectedglass/blockstates/"
            ).removesuffix(".json")
            raw_blockstate = archive.read(path)
            value = json.loads(raw_blockstate)
            shape, state_count, selections, models, states = _parse_blockstate(
                block, value
            )
            (full_paths if shape == "full" else pane_paths).append(path)
            direct_models.update(models)
            legal_states.extend(states)
            definitions.append(
                "\t".join(
                    (
                        f"connectedglass:{block}",
                        shape,
                        str(state_count),
                        digest_bytes(raw_blockstate),
                        digest_bytes(canonical_json(selections)),
                    )
                )
            )

        if len(full_paths) != FULL_COUNT or roster_digest(full_paths) != FULL_DIGEST:
            raise ValueError("Connected Glass full-cube roster changed")
        if len(pane_paths) != PANE_COUNT or roster_digest(pane_paths) != PANE_DIGEST:
            raise ValueError("Connected Glass pane roster changed")
        direct_model_paths = [_path_for_model(model) for model in direct_models]
        if (
            len(direct_models) != DIRECT_MODEL_COUNT
            or roster_digest(direct_model_paths) != DIRECT_MODEL_DIGEST
        ):
            raise ValueError("Connected Glass direct Fusion model roster changed")

        pending = list(direct_models)
        external_parents: set[str] = set()
        while pending:
            model = pending.pop()
            if model in model_paths:
                continue
            if not model.startswith("connectedglass:"):
                external_parents.add(model)
                continue
            path = _path_for_model(model)
            if path not in available:
                raise ValueError(f"missing Connected Glass model {path}")
            model_paths.add(model)
            value = json.loads(archive.read(path))
            if not isinstance(value, dict):
                raise ValueError(f"{path} model root changed")
            parent = value.get("parent")
            if isinstance(parent, str):
                pending.append(_model_key(parent, "connectedglass"))
            textures = value.get("textures", {})
            if not isinstance(textures, dict):
                raise ValueError(f"{path} texture map changed")
            for texture in textures.values():
                if isinstance(texture, str) and not texture.startswith("#"):
                    texture_keys.add(_model_key(texture, "connectedglass"))
            if model in direct_models:
                if value.get("type") != "fusion:connecting" or value.get(
                    "loader"
                ) != "fusion:model":
                    raise ValueError(f"{path} Fusion model schema changed")
                classification = _classify_connections(model, value)
                program_counts[classification] += 1
                if classification == "default" and parent != "minecraft:block/cube_all":
                    raise ValueError(f"{path} default connection geometry changed")
                pane_suffixes = (
                    "_pane_post",
                    "_pane_noside",
                    "_pane_noside_alt",
                    "_pane_side_north",
                    "_pane_side_east",
                    "_pane_side_south",
                    "_pane_side_west",
                )
                if classification != "default" and not model.endswith(pane_suffixes):
                    raise ValueError(f"{path} pane program ownership changed")
                _walk_predicate(value.get("connections"), predicate_types)

        model_resource_paths = [_path_for_model(model) for model in model_paths]
        if (
            len(model_paths) != MODEL_COUNT
            or roster_digest(model_resource_paths) != MODEL_DIGEST
        ):
            raise ValueError("Connected Glass model closure changed")
        if external_parents != {"minecraft:block/cube_all"}:
            raise ValueError("Connected Glass external model-parent ABI changed")
        if program_counts != PROGRAM_COUNTS:
            raise ValueError("Connected Glass Fusion program census changed")
        if predicate_types != PREDICATE_TYPES:
            raise ValueError("Connected Glass Fusion predicate type roster changed")

        for texture in sorted(texture_keys):
            if not texture.startswith("connectedglass:"):
                raise ValueError("Connected Glass active texture leaves its namespace")
            png = _path_for_texture(texture)
            if png not in available:
                raise ValueError(f"missing Connected Glass texture {png}")
            png_paths.add(png)
            raw = archive.read(png)
            if raw[:8] != b"\x89PNG\r\n\x1a\n" or len(raw) < 24:
                raise ValueError(f"invalid PNG {png}")
            width, height = struct.unpack(">II", raw[16:24])
            metadata = f"{png}.mcmeta"
            if metadata in available:
                metadata_paths.add(metadata)
                meta_raw = archive.read(metadata)
                meta = json.loads(meta_raw)
                if meta != {"fusion": {"type": "connecting", "layout": "pieced"}}:
                    raise ValueError(f"{metadata} Fusion metadata schema changed")
                layouts[texture] = (
                    "pieced",
                    width,
                    height,
                    digest_bytes(meta_raw),
                )
            else:
                if not texture.endswith("_edge"):
                    raise ValueError(f"{texture} unexpectedly lacks Fusion metadata")
                layouts[texture] = ("plain", width, height, "-")

        if len(png_paths) != PNG_COUNT or roster_digest(png_paths) != PNG_DIGEST:
            raise ValueError("Connected Glass active PNG roster changed")
        if (
            len(metadata_paths) != MCMETA_COUNT
            or roster_digest(metadata_paths) != MCMETA_DIGEST
        ):
            raise ValueError("Connected Glass Fusion metadata roster changed")
        observed_layouts = {
            layout: sum(1 for row in layouts.values() if row[0] == layout)
            for layout in LAYOUTS
        }
        if observed_layouts != {key: value[0] for key, value in LAYOUTS.items()}:
            raise ValueError("Connected Glass Fusion layout counts changed")
        for texture, (layout, width, height, _digest) in layouts.items():
            if (width, height) != LAYOUTS[layout][1:]:
                raise ValueError(f"{texture} dimensions changed for {layout}")

        modifiers = sorted(
            path
            for path in available
            if path.startswith("assets/connectedglass/fusion/model_modifiers/")
            and path.endswith(".json")
        )
        if modifiers != [PANE_MODIFIER_PATH]:
            raise ValueError("Connected Glass model modifier roster changed")
        modifier = json.loads(archive.read(PANE_MODIFIER_PATH))
        if (
            not isinstance(modifier, dict)
            or set(modifier) != {"pane_culling_fix", "targets"}
            or modifier.get("pane_culling_fix") is not True
            or not isinstance(modifier.get("targets"), list)
            or modifier["targets"] != sorted(set(modifier["targets"]))
            or set(modifier["targets"])
            != {
                "connectedglass:"
                + path.removeprefix("assets/connectedglass/blockstates/").removesuffix(
                    ".json"
                )
                for path in pane_paths
            }
            or roster_digest(modifier["targets"]) != MODIFIER_TARGET_DIGEST
        ):
            raise ValueError("Connected Glass pane culling modifier changed")

        closure = sorted(
            blockstate_paths
            + model_resource_paths
            + list(png_paths)
            + list(metadata_paths)
            + modifiers
        )
        if (
            len(closure) != RESOURCE_COUNT
            or len(closure) != len(set(closure))
            or roster_digest(closure) != PATH_CLOSURE_DIGEST
        ):
            raise ValueError("Connected Glass exact resource closure changed")
        resource_rows: list[str] = []
        for path in closure:
            if "/blockstates/" in path:
                kind = "blockstate"
            elif "/models/" in path:
                kind = "model"
            elif path.endswith(".png.mcmeta"):
                kind = "metadata"
            elif path.endswith(".png"):
                kind = "texture"
            else:
                kind = "modifier"
            raw = archive.read(path)
            resource_rows.append(f"{kind}\t{path}\t{len(raw)}\t{digest_bytes(raw)}")

    if (
        len(legal_states) != ROUTED_STATE_COUNT
        or roster_digest(legal_states) != LEGAL_STATE_DIGEST
    ):
        raise ValueError("Connected Glass routed legal-state roster changed")

    definitions_raw = ("\n".join(sorted(definitions)) + "\n").encode("ascii")
    resources_raw = ("\n".join(resource_rows) + "\n").encode("ascii")
    textures_raw = (
        "\n".join(
            "\t".join((texture, layout, str(width), str(height), meta_digest))
            for texture, (layout, width, height, meta_digest) in sorted(layouts.items())
        )
        + "\n"
    ).encode("ascii")
    host_models_raw = (
        "\n".join(
            f"model\t{path}\t{size}\t{sha256}" for path, size, sha256 in HOST_MODELS
        )
        + "\n"
    ).encode("ascii")
    if len(HOST_MODELS) != HOST_MODEL_COUNT:
        raise ValueError("host geometry ABI roster changed")

    catalog = {
        "schema": 1,
        "artifacts": [
            {
                "modId": "connectedglass",
                "version": "1.1.14",
                "filename": CONNECTEDGLASS_FILENAME,
                "size": CONNECTEDGLASS_SIZE,
                "sha1": CONNECTEDGLASS_SHA1,
                "sha256": CONNECTEDGLASS_SHA256,
                "sha512": CONNECTEDGLASS_SHA512,
            },
            {
                "modId": "fusion",
                "version": "1.3.12",
                "filename": FUSION_FILENAME,
                "size": FUSION_SIZE,
                "sha1": FUSION_SHA1,
                "sha256": FUSION_SHA256,
                "sha512": FUSION_SHA512,
            },
        ],
        "requiredForStaticRendering": ["connectedglass", "fusion"],
    }
    profile = {
        "schema": 1,
        "profileId": "connectedglass-fusion-1.1.14-1.3.12",
        "namespaceOwner": "connectedglass",
        "formatOwner": "fusion",
        "counts": {
            "allBlockstates": ALL_BLOCKSTATES_COUNT,
            "routedBlocks": ROUTED_COUNT,
            "routedLegalStates": ROUTED_STATE_COUNT,
            "directFusionModels": DIRECT_MODEL_COUNT,
            "modelClosure": MODEL_COUNT,
            "textures": PNG_COUNT,
            "fusionMetadata": MCMETA_COUNT,
            "modelModifiers": MODIFIER_COUNT,
            "resourceClosure": RESOURCE_COUNT,
            "hostGeometryModels": HOST_MODEL_COUNT,
        },
        "shapes": {"full": FULL_COUNT, "pane": PANE_COUNT},
        "layouts": {key: value[0] for key, value in LAYOUTS.items()},
        "connectionPrograms": PROGRAM_COUNTS,
        "predicateTypes": sorted(PREDICATE_TYPES),
        "digests": {
            "blockstateRoster": BLOCKSTATE_DIGEST,
            "fullCubeRoster": FULL_DIGEST,
            "paneRoster": PANE_DIGEST,
            "legalStateRoster": LEGAL_STATE_DIGEST,
            "directModelRoster": DIRECT_MODEL_DIGEST,
            "modelRoster": MODEL_DIGEST,
            "pngRoster": PNG_DIGEST,
            "metadataRoster": MCMETA_DIGEST,
            "modifierTargetRoster": MODIFIER_TARGET_DIGEST,
            "resourcePathClosure": PATH_CLOSURE_DIGEST,
            "definitions": digest_bytes(definitions_raw),
            "requiredResources": digest_bytes(resources_raw),
            "textures": digest_bytes(textures_raw),
            "hostGeometryModels": digest_bytes(host_models_raw),
        },
        "hostGeometryAbi": {
            "owner": "minecraft",
            "clientJarSha256": MINECRAFT_CLIENT_SHA256,
            "pathsAreOutsideConnectedGlassClosure": True,
        },
        "textureOverridePolicy": "pixel-only-exact-dimensions",
        "failurePolicy": "route-wide-inactive-or-atomic-stock-fallback",
        "assetPolicy": "operator-installed-only",
    }
    return {
        CATALOG_PATH: canonical_json(catalog),
        PROFILE_PATH: canonical_json(profile),
        DEFINITIONS_PATH: definitions_raw,
        RESOURCES_PATH: resources_raw,
        TEXTURES_PATH: textures_raw,
        HOST_MODELS_PATH: host_models_raw,
    }


def write_or_check(outputs: dict[Path, bytes], check: bool) -> str:
    changed: list[str] = []
    for path, raw in outputs.items():
        if not path.is_file() or path.read_bytes() != raw:
            changed.append(str(path))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
    if check and changed:
        raise ValueError("generated profile is stale: " + ", ".join(changed))
    return "verified" if check else "generated"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connectedglass", required=True, type=Path)
    parser.add_argument("--fusion", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    outputs = build_outputs(arguments.connectedglass, arguments.fusion)
    action = write_or_check(outputs, arguments.check)
    print(
        f"{action} exact Connected Glass/Fusion profile "
        f"({ROUTED_COUNT} routed blocks)"
    )


if __name__ == "__main__":
    main()

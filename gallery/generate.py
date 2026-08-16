#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate the bounded ATM 1.2.0 Connected Glass review gallery."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parent

PACK_VERSION = "1.2.0"
MINECRAFT_VERSION = "1.21.1"
CONNECTED_GLASS_VERSION = "1.1.14"
CONNECTED_GLASS_FILE = "connectedglass-1.1.14-neoforge-mc1.21.jar"
CONNECTED_GLASS_SIZE = 819_976
CONNECTED_GLASS_SHA256 = (
    "e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe"
)
FUSION_VERSION = "1.3.12"
FUSION_FILE = "fusion-1.3.12-neoforge-mc1.21.1.jar"
FUSION_SIZE = 923_270
FUSION_SHA256 = (
    "17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa"
)

OBJECTIVE = "cg_gallery"
NAMESPACE = "connectedglass_gallery"
FLOOR_Y = 100
CELL_HALF_SIZE = 6
REGION_MIN = (189, 100, 201)
REGION_MAX = (251, 106, 231)
POSE = (220, 122, 259, 180, 24)
CELL_ANCHORS = (
    (196, FLOOR_Y, 208),
    (212, FLOOR_Y, 208),
    (228, FLOOR_Y, 208),
    (244, FLOOR_Y, 208),
    (196, FLOOR_Y, 224),
    (212, FLOOR_Y, 224),
    (228, FLOOR_Y, 224),
    (244, FLOOR_Y, 224),
)


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int
    z: int

    def offset(self, relative: "Position") -> "Position":
        return Position(
            self.x + relative.x,
            self.y + relative.y,
            self.z + relative.z,
        )

    def command(self) -> str:
        return f"{self.x} {self.y} {self.z}"

    def payload(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass(frozen=True)
class Observation:
    relative: Position
    block_state: str
    role: str
    placed: bool = True


@dataclass(frozen=True)
class GalleryCase:
    number: int
    case_id: str
    title: str
    anchor: Position
    notes: str
    observations: tuple[Observation, ...]

    @property
    def function_id(self) -> str:
        return f"{self.number:02d}_{self.case_id}"


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def pane_state(
    block_id: str,
    *,
    north: bool = False,
    east: bool = False,
    south: bool = False,
    west: bool = False,
    waterlogged: bool = False,
) -> str:
    """Return one complete, canonical IronBars-derived pane state."""
    return (
        f"{block_id}[east={bool_text(east)},north={bool_text(north)},"
        f"south={bool_text(south)},waterlogged={bool_text(waterlogged)},"
        f"west={bool_text(west)}]"
    )


def obs(
    x: int,
    y: int,
    z: int,
    block_state: str,
    role: str,
    *,
    placed: bool = True,
) -> Observation:
    return Observation(Position(x, y, z), block_state, role, placed)


def pane(
    x: int,
    y: int,
    z: int,
    block_id: str,
    role: str,
    **states: bool,
) -> Observation:
    return obs(x, y, z, pane_state(block_id, **states), role)


def cases() -> tuple[GalleryCase, ...]:
    clear_pane = "connectedglass:clear_glass_pane"
    red_borderless_pane = "connectedglass:borderless_glass_red_pane"

    result = (
        GalleryCase(
            1,
            "clear_glass_wall",
            "Clear glass: isolated cube and 3x3 wall",
            Position(*CELL_ANCHORS[0]),
            "Compares an isolated cube with the internal seams and perimeter "
            "of a 3x3 same-ID wall.",
            (
                obs(-4, 1, -3, "connectedglass:clear_glass", "isolated cube"),
                *tuple(
                    obs(x, y, 1, "connectedglass:clear_glass", "3x3 wall")
                    for y in range(1, 4)
                    for x in range(-1, 2)
                ),
            ),
        ),
        GalleryCase(
            2,
            "scratched_red_l",
            "Scratched red glass: L wall with missing diagonal",
            Position(*CELL_ANCHORS[1]),
            "The lower-left corner has up and east neighbors while its diagonal remains air.",
            (
                obs(-2, 1, 0, "connectedglass:scratched_glass_red", "L corner"),
                obs(-1, 1, 0, "connectedglass:scratched_glass_red", "lower arm"),
                obs(0, 1, 0, "connectedglass:scratched_glass_red", "lower arm"),
                obs(-2, 2, 0, "connectedglass:scratched_glass_red", "upright arm"),
                obs(-2, 3, 0, "connectedglass:scratched_glass_red", "upright arm"),
                obs(
                    -1,
                    2,
                    0,
                    "minecraft:air",
                    "intentional missing diagonal",
                    placed=False,
                ),
            ),
        ),
        GalleryCase(
            3,
            "tinted_beside_stone",
            "Tinted borderless glass: 2x2 beside stone",
            Position(*CELL_ANCHORS[2]),
            "A 2x2 tinted wall shares a vertical boundary with an opaque 2x2 "
            "vanilla stone control.",
            (
                *tuple(
                    obs(x, y, 0, "connectedglass:tinted_borderless_glass", "2x2 tinted wall")
                    for y in range(1, 3)
                    for x in (-2, -1)
                ),
                *tuple(
                    obs(x, y, 0, "minecraft:stone", "opaque boundary control")
                    for y in range(1, 3)
                    for x in (0, 1)
                ),
            ),
        ),
        GalleryCase(
            4,
            "mixed_cube_boundary",
            "Mixed clear, colored, and borderless cube boundary",
            Position(*CELL_ANCHORS[3]),
            "Two identical clear cubes establish the positive control before "
            "colored and borderless ID boundaries.",
            (
                obs(-3, 1, 0, "connectedglass:clear_glass", "same-ID clear pair"),
                obs(-2, 1, 0, "connectedglass:clear_glass", "same-ID clear pair"),
                obs(-1, 1, 0, "connectedglass:clear_glass_red", "colored boundary"),
                obs(0, 1, 0, "connectedglass:borderless_glass", "borderless boundary"),
            ),
        ),
        GalleryCase(
            5,
            "clear_pane_topologies",
            "Clear pane: isolated, straight, L, T, and cross",
            Position(*CELL_ANCHORS[4]),
            "Five separated pane networks lock all horizontal multipart "
            "connection combinations needed by the fixture.",
            (
                pane(-4, 1, -4, clear_pane, "isolated pane"),
                pane(-4, 1, 0, clear_pane, "straight north end", south=True),
                pane(-4, 1, 1, clear_pane, "straight middle", north=True, south=True),
                pane(-4, 1, 2, clear_pane, "straight south end", north=True),
                pane(0, 1, -4, clear_pane, "L north end", south=True),
                pane(0, 1, -3, clear_pane, "L corner", north=True, east=True),
                pane(1, 1, -3, clear_pane, "L east end", west=True),
                pane(0, 1, 1, clear_pane, "T center", north=True, east=True, west=True),
                pane(0, 1, 0, clear_pane, "T north end", south=True),
                pane(1, 1, 1, clear_pane, "T east end", west=True),
                pane(-1, 1, 1, clear_pane, "T west end", east=True),
                pane(
                    4,
                    1,
                    1,
                    clear_pane,
                    "cross center",
                    north=True,
                    east=True,
                    south=True,
                    west=True,
                ),
                pane(4, 1, 0, clear_pane, "cross north end", south=True),
                pane(5, 1, 1, clear_pane, "cross east end", west=True),
                pane(4, 1, 2, clear_pane, "cross south end", north=True),
                pane(3, 1, 1, clear_pane, "cross west end", east=True),
            ),
        ),
        GalleryCase(
            6,
            "red_pane_stacks",
            "Borderless red pane: two-high straight and cross stacks",
            Position(*CELL_ANCHORS[5]),
            "Duplicated vertical layers exercise pane top/bottom culling "
            "without changing horizontal state properties.",
            tuple(
                pane(-4, y, -1, red_borderless_pane, "two-high straight north end", south=True)
                for y in (1, 2)
            )
            + tuple(
                pane(
                    -4,
                    y,
                    0,
                    red_borderless_pane,
                    "two-high straight middle",
                    north=True,
                    south=True,
                )
                for y in (1, 2)
            )
            + tuple(
                pane(-4, y, 1, red_borderless_pane, "two-high straight south end", north=True)
                for y in (1, 2)
            )
            + tuple(
                item
                for y in (1, 2)
                for item in (
                    pane(
                        3,
                        y,
                        0,
                        red_borderless_pane,
                        "two-high cross center",
                        north=True,
                        east=True,
                        south=True,
                        west=True,
                    ),
                    pane(3, y, -1, red_borderless_pane, "two-high cross north end", south=True),
                    pane(4, y, 0, red_borderless_pane, "two-high cross east end", west=True),
                    pane(3, y, 1, red_borderless_pane, "two-high cross south end", north=True),
                    pane(2, y, 0, red_borderless_pane, "two-high cross west end", east=True),
                )
            ),
        ),
        GalleryCase(
            7,
            "mixed_and_waterlogged_panes",
            "Mixed pane boundary and contained waterlogged pane",
            Position(*CELL_ANCHORS[6]),
            "Adjacent distinct pane IDs connect geometrically but retain "
            "separate material identity; a same-ID cross contains one "
            "waterlogged center.",
            (
                pane(-4, 1, -3, clear_pane, "mixed boundary: clear", east=True),
                pane(
                    -3,
                    1,
                    -3,
                    "connectedglass:clear_glass_red_pane",
                    "mixed boundary: red",
                    east=True,
                    west=True,
                ),
                pane(
                    -2,
                    1,
                    -3,
                    "connectedglass:borderless_glass_pane",
                    "mixed boundary: borderless",
                    west=True,
                ),
                pane(2, 1, 0, clear_pane, "waterlogged cross north end", south=True),
                pane(3, 1, 1, clear_pane, "waterlogged cross east end", west=True),
                pane(2, 1, 2, clear_pane, "waterlogged cross south end", north=True),
                pane(1, 1, 1, clear_pane, "waterlogged cross west end", east=True),
                pane(
                    2,
                    1,
                    1,
                    clear_pane,
                    "contained waterlogged cross center",
                    north=True,
                    east=True,
                    south=True,
                    west=True,
                    waterlogged=True,
                ),
            ),
        ),
        GalleryCase(
            8,
            "vanilla_controls",
            "Vanilla glass, pane, and stone controls",
            Position(*CELL_ANCHORS[7]),
            "A same-ID vanilla glass pair, isolated vanilla pane, and isolated "
            "stone remain outside the add-on route.",
            (
                obs(-4, 1, 0, "minecraft:glass", "vanilla glass pair"),
                obs(-3, 1, 0, "minecraft:glass", "vanilla glass pair"),
                pane(0, 1, 0, "minecraft:glass_pane", "isolated vanilla pane"),
                obs(4, 1, 0, "minecraft:stone", "isolated stone"),
            ),
        ),
    )
    validate_cases(result)
    return result


def validate_cases(items: tuple[GalleryCase, ...]) -> None:
    if len(items) != 8:
        raise AssertionError(f"expected eight gallery cells, found {len(items)}")
    if tuple(item.number for item in items) != tuple(range(1, 9)):
        raise AssertionError("gallery cells must be numbered 1 through 8")
    if len({item.case_id for item in items}) != len(items):
        raise AssertionError("duplicate gallery case ID")

    pane_pattern = re.compile(
        r"^[a-z0-9_.-]+:[a-z0-9_./-]+\["
        r"east=(?:false|true),north=(?:false|true),south=(?:false|true),"
        r"waterlogged=(?:false|true),west=(?:false|true)\]$"
    )
    absolute_positions: set[Position] = set()
    placement_count = 0
    observation_count = 0
    for item in items:
        local_positions: set[Position] = set()
        for observation in item.observations:
            observation_count += 1
            if observation.relative in local_positions:
                raise AssertionError(
                    f"duplicate relative position in {item.case_id}: {observation.relative}"
                )
            local_positions.add(observation.relative)
            absolute = item.anchor.offset(observation.relative)
            if absolute in absolute_positions:
                raise AssertionError(f"gallery observation overlap at {absolute}")
            absolute_positions.add(absolute)
            if not (
                item.anchor.x - 5 <= absolute.x <= item.anchor.x + 5
                and FLOOR_Y + 1 <= absolute.y <= FLOOR_Y + 5
                and item.anchor.z - 5 <= absolute.z <= item.anchor.z + 5
            ):
                raise AssertionError(
                    f"observation outside bounded cell {item.case_id}: {absolute}"
                )
            if observation.placed:
                placement_count += 1
                if observation.block_state == "minecraft:air":
                    raise AssertionError("placed observations cannot be air")
            elif observation.block_state != "minecraft:air":
                raise AssertionError("negative observations must expect air")
            if "pane" in observation.block_state and not pane_pattern.fullmatch(
                observation.block_state
            ):
                raise AssertionError(
                    f"pane observation lacks a complete canonical state: "
                    f"{observation.block_state}"
                )

    if placement_count != 71 or observation_count != 72:
        raise AssertionError(
            f"fixture census changed: {placement_count} placements / "
            f"{observation_count} observations"
        )
    waterlogged = sum(
        "waterlogged=true" in observation.block_state
        for item in items
        for observation in item.observations
    )
    if waterlogged != 1:
        raise AssertionError("fixture must contain exactly one waterlogged pane")


def source_block_ids(items: tuple[GalleryCase, ...]) -> set[str]:
    result: set[str] = set()
    for item in items:
        for observation in item.observations:
            block_id = observation.block_state.split("[", 1)[0]
            if block_id.startswith("connectedglass:"):
                result.add(block_id)
    return result


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_connected_glass_jar(path: Path, items: tuple[GalleryCase, ...]) -> None:
    if not path.is_file():
        raise ValueError(f"Connected Glass artifact does not exist: {path}")
    if path.stat().st_size != CONNECTED_GLASS_SIZE:
        raise ValueError("Connected Glass artifact size does not match the exact input")
    if file_sha256(path) != CONNECTED_GLASS_SHA256:
        raise ValueError("Connected Glass artifact SHA-256 does not match the exact input")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        for block_id in sorted(source_block_ids(items)):
            path_name = (
                "assets/connectedglass/blockstates/"
                f"{block_id.split(':', 1)[1]}.json"
            )
            if path_name not in names:
                raise ValueError(f"exact blockstate resource is missing: {path_name}")
            payload = json.loads(archive.read(path_name))
            if block_id.endswith("_pane"):
                conditions = {
                    key
                    for part in payload.get("multipart", [])
                    for key in part.get("when", {})
                }
                if conditions != {"north", "east", "south", "west"}:
                    raise ValueError(
                        f"pane multipart property contract changed for {block_id}"
                    )
            elif set(payload) != {"variants"}:
                raise ValueError(f"cube blockstate contract changed for {block_id}")


def verify_fusion_jar(path: Path) -> None:
    if not path.is_file():
        raise ValueError(f"Fusion artifact does not exist: {path}")
    if path.stat().st_size != FUSION_SIZE:
        raise ValueError("Fusion artifact size does not match the exact input")
    if file_sha256(path) != FUSION_SHA256:
        raise ValueError("Fusion artifact SHA-256 does not match the exact input")


def counts(items: tuple[GalleryCase, ...]) -> dict[str, int]:
    observations = [obs_ for item in items for obs_ in item.observations]
    placements = [obs_ for obs_ in observations if obs_.placed]
    return {
        "cells": len(items),
        "connected_glass_cube_placements": sum(
            obs_.placed
            and obs_.block_state.startswith("connectedglass:")
            and "pane" not in obs_.block_state
            for obs_ in observations
        ),
        "connected_glass_pane_placements": sum(
            obs_.placed
            and obs_.block_state.startswith("connectedglass:")
            and "pane" in obs_.block_state
            for obs_ in observations
        ),
        "negative_space_observations": sum(not obs_.placed for obs_ in observations),
        "observations": len(observations),
        "placements": len(placements),
        "vanilla_placements": sum(
            obs_.placed and obs_.block_state.startswith("minecraft:")
            for obs_ in observations
        ),
        "waterlogged_panes": sum(
            obs_.placed and "waterlogged=true" in obs_.block_state
            for obs_ in observations
        ),
    }


def cases_json(items: tuple[GalleryCase, ...]) -> str:
    payload = {
        "cases": [
            {
                "anchor": item.anchor.payload(),
                "case_id": item.case_id,
                "index": item.number,
                "notes": item.notes,
                "observations": [
                    {
                        "absolute": item.anchor.offset(observation.relative).payload(),
                        "block_state": observation.block_state,
                        "placed": observation.placed,
                        "relative": observation.relative.payload(),
                        "role": observation.role,
                    }
                    for observation in item.observations
                ],
                "title": item.title,
            }
            for item in items
        ],
        "counts": counts(items),
        "evidence": {
            "all_the_mons": PACK_VERSION,
            "connected_glass": {
                "filename": CONNECTED_GLASS_FILE,
                "sha256": CONNECTED_GLASS_SHA256,
                "size_bytes": CONNECTED_GLASS_SIZE,
                "version": CONNECTED_GLASS_VERSION,
            },
            "fusion": {
                "filename": FUSION_FILE,
                "sha256": FUSION_SHA256,
                "size_bytes": FUSION_SIZE,
                "version": FUSION_VERSION,
            },
            "minecraft": MINECRAFT_VERSION,
        },
        "gallery": {
            "dimension": "minecraft:overworld",
            "floor_y": FLOOR_Y,
            "pose": {
                "pitch": POSE[4],
                "x": POSE[0],
                "y": POSE[1],
                "yaw": POSE[3],
                "z": POSE[2],
            },
            "region_max": {
                "x": REGION_MAX[0],
                "y": REGION_MAX[1],
                "z": REGION_MAX[2],
            },
            "region_min": {
                "x": REGION_MIN[0],
                "y": REGION_MIN[1],
                "z": REGION_MIN[2],
            },
        },
        "schema": 1,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def tsv_text(value: str) -> str:
    return value.replace("\t", " ").replace("\r", " ").replace("\n", " ")


def cases_tsv(items: tuple[GalleryCase, ...]) -> str:
    header = (
        "case_index\tcase_id\ttitle\tanchor_x\tanchor_y\tanchor_z\t"
        "observation_index\tx\ty\tz\tblock_state\tplaced\trole\tnotes"
    )
    lines = [header]
    for item in items:
        for index, observation in enumerate(item.observations, start=1):
            absolute = item.anchor.offset(observation.relative)
            lines.append(
                "\t".join(
                    (
                        str(item.number),
                        item.case_id,
                        tsv_text(item.title),
                        str(item.anchor.x),
                        str(item.anchor.y),
                        str(item.anchor.z),
                        str(index),
                        str(absolute.x),
                        str(absolute.y),
                        str(absolute.z),
                        observation.block_state,
                        bool_text(observation.placed),
                        tsv_text(observation.role),
                        tsv_text(item.notes),
                    )
                )
            )
    return "\n".join(lines) + "\n"


def generated_header() -> str:
    return "# Generated by gallery/generate.py; do not edit.\n"


def case_build_function(item: GalleryCase) -> str:
    lines = [generated_header().rstrip(), f"# Cell {item.number}: {item.title}"]
    for observation in item.observations:
        absolute = item.anchor.offset(observation.relative)
        state = observation.block_state if observation.placed else "minecraft:air"
        lines.append(f"setblock {absolute.command()} {state} replace")
    return "\n".join(lines) + "\n"


def case_verify_function(item: GalleryCase) -> str:
    case_score = f"#case{item.number:02d}"
    lines = [
        generated_header().rstrip(),
        f"# Cell {item.number}: {item.title}",
        f"scoreboard players set {case_score} {OBJECTIVE} 0",
    ]
    for observation in item.observations:
        absolute = item.anchor.offset(observation.relative)
        check = f"unless block {absolute.command()} {observation.block_state}"
        lines.extend(
            (
                f"scoreboard players add #checked {OBJECTIVE} 1",
                f"execute {check} run scoreboard players add #failures {OBJECTIVE} 1",
                f"execute {check} run scoreboard players add {case_score} {OBJECTIVE} 1",
            )
        )
    failure_message = json.dumps(
        {
            "color": "red",
            "text": f"Connected Glass gallery cell {item.number} failed: {item.title}",
        },
        separators=(",", ":"),
    )
    lines.extend(
        (
            f"execute if score {case_score} {OBJECTIVE} matches 1.. run "
            f"scoreboard players add #failed_cells {OBJECTIVE} 1",
            f"execute if score {case_score} {OBJECTIVE} matches 1.. run "
            f"tellraw @a {failure_message}",
        )
    )
    return "\n".join(lines) + "\n"


def clear_function() -> str:
    minimum = Position(*REGION_MIN).command()
    maximum = Position(*REGION_MAX).command()
    return (
        generated_header()
        + f"execute in minecraft:overworld run forceload add "
        f"{REGION_MIN[0]} {REGION_MIN[2]} {REGION_MAX[0]} {REGION_MAX[2]}\n"
        + f"execute in minecraft:overworld run fill {minimum} {maximum} minecraft:air replace\n"
    )


def build_function(items: tuple[GalleryCase, ...]) -> str:
    census = counts(items)
    lines = [
        generated_header().rstrip(),
        f"scoreboard objectives add {OBJECTIVE} dummy",
        f"function {NAMESPACE}:clear",
    ]
    for item in items:
        anchor = item.anchor
        lines.extend(
            (
                "execute in minecraft:overworld run fill "
                f"{anchor.x - CELL_HALF_SIZE} {FLOOR_Y} {anchor.z - CELL_HALF_SIZE} "
                f"{anchor.x + CELL_HALF_SIZE} {FLOOR_Y} {anchor.z + CELL_HALF_SIZE} "
                "minecraft:deepslate_tiles replace",
                "execute in minecraft:overworld run fill "
                f"{anchor.x - CELL_HALF_SIZE + 1} {FLOOR_Y} {anchor.z - CELL_HALF_SIZE + 1} "
                f"{anchor.x + CELL_HALF_SIZE - 1} {FLOOR_Y} {anchor.z + CELL_HALF_SIZE - 1} "
                "minecraft:smooth_stone replace",
                f"execute in minecraft:overworld run function "
                f"{NAMESPACE}:cell_build/{item.function_id}",
            )
        )
    lines.extend(
        (
            f"scoreboard players set #cells {OBJECTIVE} {census['cells']}",
            f"scoreboard players set #placements {OBJECTIVE} {census['placements']}",
            f"scoreboard players set #observations {OBJECTIVE} {census['observations']}",
            f"scoreboard players set #ready {OBJECTIVE} 1",
            f"function {NAMESPACE}:verify",
        )
    )
    return "\n".join(lines) + "\n"


def status_function() -> str:
    payload = [
        {"color": "aqua", "text": "Connected Glass gallery: "},
        {"text": "cells="},
        {"score": {"name": "#cells", "objective": OBJECTIVE}},
        {"text": ", placements="},
        {"score": {"name": "#placements", "objective": OBJECTIVE}},
        {"text": ", checked="},
        {"score": {"name": "#checked", "objective": OBJECTIVE}},
        {"text": ", failed_cells="},
        {"score": {"name": "#failed_cells", "objective": OBJECTIVE}},
        {"text": ", failures="},
        {"score": {"name": "#failures", "objective": OBJECTIVE}},
    ]
    return generated_header() + "tellraw @a " + json.dumps(
        payload, separators=(",", ":")
    ) + "\n"


def verify_function(items: tuple[GalleryCase, ...]) -> str:
    lines = [
        generated_header().rstrip(),
        f"scoreboard players set #checked {OBJECTIVE} 0",
        f"scoreboard players set #failed_cells {OBJECTIVE} 0",
        f"scoreboard players set #failures {OBJECTIVE} 0",
    ]
    lines.extend(
        f"execute in minecraft:overworld run function {NAMESPACE}:cell_verify/{item.function_id}"
        for item in items
    )
    lines.extend(
        (
            f"function {NAMESPACE}:status",
            f"execute if score #failures {OBJECTIVE} matches 0 run tellraw @a "
            '{"color":"green","text":"Connected Glass gallery verification passed."}',
            f"execute unless score #failures {OBJECTIVE} matches 0 run tellraw @a "
            '{"color":"red","text":"Connected Glass gallery verification failed."}',
        )
    )
    return "\n".join(lines) + "\n"


def generated_files(items: tuple[GalleryCase, ...]) -> dict[Path, bytes]:
    files: dict[Path, bytes] = {
        Path("cases.json"): cases_json(items).encode("utf-8"),
        Path("cases.tsv"): cases_tsv(items).encode("utf-8"),
        Path("datapack/pack.mcmeta"): (
            json.dumps(
                {
                    "pack": {
                        "description": (
                            "ATM 1.2.0 Connected Glass 1.1.14 + Fusion 1.3.12 "
                            "BlueMap review gallery"
                        ),
                        "pack_format": 48,
                    }
                },
                indent=2,
            )
            + "\n"
        ).encode("utf-8"),
        Path("datapack/data/minecraft/tags/function/load.json"): (
            json.dumps({"values": [f"{NAMESPACE}:load"]}, indent=2) + "\n"
        ).encode("utf-8"),
        Path(f"datapack/data/{NAMESPACE}/function/load.mcfunction"): (
            generated_header() + f"scoreboard objectives add {OBJECTIVE} dummy\n"
        ).encode("utf-8"),
        Path(f"datapack/data/{NAMESPACE}/function/clear.mcfunction"): (
            clear_function().encode("utf-8")
        ),
        Path(f"datapack/data/{NAMESPACE}/function/build.mcfunction"): (
            build_function(items).encode("utf-8")
        ),
        Path(f"datapack/data/{NAMESPACE}/function/verify.mcfunction"): (
            verify_function(items).encode("utf-8")
        ),
        Path(f"datapack/data/{NAMESPACE}/function/status.mcfunction"): (
            status_function().encode("utf-8")
        ),
        Path(f"datapack/data/{NAMESPACE}/function/pose.mcfunction"): (
            generated_header()
            + "execute in minecraft:overworld run tp @s "
            + " ".join(str(value) for value in POSE)
            + "\n"
        ).encode("utf-8"),
        Path(f"datapack/data/{NAMESPACE}/function/release.mcfunction"): (
            generated_header()
            + f"function {NAMESPACE}:clear\n"
            + f"scoreboard players set #ready {OBJECTIVE} 0\n"
            + f"execute in minecraft:overworld run forceload remove "
            + f"{REGION_MIN[0]} {REGION_MIN[2]} {REGION_MAX[0]} {REGION_MAX[2]}\n"
        ).encode("utf-8"),
    }
    for item in items:
        files[
            Path(
                f"datapack/data/{NAMESPACE}/function/cell_build/{item.function_id}.mcfunction"
            )
        ] = case_build_function(item).encode("utf-8")
        files[
            Path(
                f"datapack/data/{NAMESPACE}/function/cell_verify/{item.function_id}.mcfunction"
            )
        ] = case_verify_function(item).encode("utf-8")

    checksum_lines = [
        f"{hashlib.sha256(content).hexdigest()}  {path.as_posix()}"
        for path, content in sorted(files.items(), key=lambda pair: pair[0].as_posix())
    ]
    files[Path("SHA256SUMS")] = ("\n".join(checksum_lines) + "\n").encode("ascii")
    return files


def existing_generated_paths() -> set[Path]:
    result = {
        path
        for path in (Path("cases.json"), Path("cases.tsv"), Path("SHA256SUMS"))
        if (ROOT / path).exists()
    }
    datapack = ROOT / "datapack"
    if datapack.exists():
        result.update(
            path.relative_to(ROOT) for path in datapack.rglob("*") if path.is_file()
        )
    return result


def write_or_check(files: dict[Path, bytes], check: bool) -> None:
    expected_paths = set(files)
    if check:
        differences: list[str] = []
        for path, content in sorted(files.items(), key=lambda pair: pair[0].as_posix()):
            target = ROOT / path
            if not target.is_file():
                differences.append(f"missing:{path.as_posix()}")
            elif target.read_bytes() != content:
                differences.append(f"changed:{path.as_posix()}")
        for path in sorted(existing_generated_paths() - expected_paths):
            differences.append(f"unexpected:{path.as_posix()}")
        if differences:
            raise ValueError("generated gallery differs: " + ", ".join(differences))
        return

    for path in sorted(existing_generated_paths() - expected_paths, reverse=True):
        (ROOT / path).unlink()
    for path, content in sorted(files.items(), key=lambda pair: pair[0].as_posix()):
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify checked-in generated outputs instead of writing them",
    )
    parser.add_argument(
        "--connectedglass-jar",
        type=Path,
        help="optionally verify the exact Connected Glass JAR and selected blockstates",
    )
    parser.add_argument(
        "--fusion-jar",
        type=Path,
        help="optionally verify the exact Fusion JAR identity",
    )
    arguments = parser.parse_args()

    try:
        items = cases()
        if arguments.connectedglass_jar:
            verify_connected_glass_jar(arguments.connectedglass_jar, items)
        if arguments.fusion_jar:
            verify_fusion_jar(arguments.fusion_jar)
        write_or_check(generated_files(items), arguments.check)
    except (AssertionError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"gallery generation failed: {error}", file=sys.stderr)
        return 1

    census = counts(items)
    action = "checked" if arguments.check else "generated"
    print(
        f"{action} {census['cells']} cells, {census['placements']} placements, "
        f"and {census['observations']} exact observations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

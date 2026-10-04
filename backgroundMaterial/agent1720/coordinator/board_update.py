"""Append patches and journal entries to docs/navigator/planning.json.

Usage: python board_update.py update.json

``update.json`` has the shape ``{"journal": [...], "patches": [...]}`` using the
same patch format that ``applyPlanningBoard`` in docs/navigator/app.js reads.
The revision is bumped by one so browsers re-apply the board.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BOARD = Path(__file__).resolve().parents[3] / "docs" / "navigator" / "planning.json"
STATUSES = {"unstarted", "exploring", "in-progress", "proved", "killed", "blocked"}


def validate(patch: dict) -> None:
    """Raise ValueError when a patch would be ignored or misread by app.js."""
    if patch.get("op") == "insert":
        node = patch.get("node") or {}
        for key in ("id", "title", "statement", "status"):
            if key not in node:
                raise ValueError(f"insert missing node.{key}: {patch}")
        if node["status"] not in STATUSES:
            raise ValueError(f"bad status {node['status']}")
        node.setdefault("approach", "")
        node.setdefault("killCriteria", "")
        node.setdefault("files", [])
        node.setdefault("notes", [])
        node.setdefault("evidence", "")
        node.setdefault("expanded", False)
        node.setdefault("children", [])
        if "parentId" not in patch:
            raise ValueError(f"insert missing parentId: {patch}")
    else:
        if "id" not in patch:
            raise ValueError(f"update missing id: {patch}")
        if "status" in patch and patch["status"] not in STATUSES:
            raise ValueError(f"bad status {patch['status']}")


def main(update_path: str) -> None:
    """Merge ``update_path`` into the board and bump the revision."""
    board = json.loads(BOARD.read_text())
    update = json.loads(Path(update_path).read_text())
    for p in update.get("patches", []):
        validate(p)
    board["journal"].extend(update.get("journal", []))
    board["patches"].extend(update.get("patches", []))
    board["revision"] = board.get("revision", 0) + 1
    board["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    BOARD.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
    print(f"revision {board['revision']}: +{len(update.get('patches', []))} patches")


if __name__ == "__main__":
    main(sys.argv[1])

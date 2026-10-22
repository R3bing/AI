"""JARVIS Autonomous System Tools & Second Brain Connector.

Enables JARVIS to:
1. Search local files across the workspace.
2. Read, create, and sync markdown notes directly into the HOLO 3D Second Brain (port 4890).
3. Track focus sessions and productivity ("Focus Lock: Sir, Instagram can wait").
4. Execute sandboxed terminal checks.
"""

from __future__ import annotations

import os
import glob
import time
import json
from typing import List, Dict, Any, Optional

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HOLO_DIR = os.path.join(WORKSPACE_ROOT, "data", "holo-gestures")
HOLO_NOTES_DIR = os.path.join(HOLO_DIR, "sample-notes")


class JarvisSystemTools:
    """Core executive tools for the JARVIS operating system."""

    def __init__(self):
        os.makedirs(HOLO_NOTES_DIR, exist_ok=True)
        self.focus_mode_active = False
        self.focus_goal = ""
        self.focus_start_time = 0

    def find_files(self, keyword: str, root_dir: Optional[str] = None, max_results: int = 12) -> List[Dict[str, Any]]:
        """Searches files by keyword across the workspace."""
        if not root_dir:
            root_dir = WORKSPACE_ROOT

        results = []
        clean_kw = keyword.lower().strip()

        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip hidden and cache folders
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ("__pycache__", "node_modules", ".venv", ".git")]
            for f in filenames:
                if clean_kw in f.lower():
                    full_p = os.path.join(dirpath, f)
                    rel_p = os.path.relpath(full_p, WORKSPACE_ROOT)
                    try:
                        sz = os.path.getsize(full_p)
                        results.append({
                            "name": f,
                            "relative_path": rel_p,
                            "full_path": full_p,
                            "size_bytes": sz,
                            "size_kb": round(sz / 1024, 1),
                        })
                    except OSError:
                        pass
                if len(results) >= max_results:
                    break
            if len(results) >= max_results:
                break

        return results

    def read_file_preview(self, file_path: str, max_chars: int = 2000) -> Dict[str, Any]:
        """Reads a preview of a local file."""
        target = file_path if os.path.isabs(file_path) else os.path.join(WORKSPACE_ROOT, file_path)
        if not os.path.exists(target):
            return {"success": False, "error": f"File '{file_path}' does not exist."}

        try:
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_chars)
            return {
                "success": True,
                "path": file_path,
                "content": content,
                "char_count": len(content),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_second_brain_notes(self) -> List[Dict[str, Any]]:
        """Lists all notes currently residing in the 3D Second Brain."""
        notes = []
        if not os.path.exists(HOLO_NOTES_DIR):
            return notes

        for f in sorted(os.listdir(HOLO_NOTES_DIR)):
            if f.endswith((".md", ".txt")):
                full_p = os.path.join(HOLO_NOTES_DIR, f)
                try:
                    with open(full_p, "r", encoding="utf-8", errors="ignore") as fp:
                        raw = fp.read()
                    lines = [l.strip() for l in raw.splitlines() if l.strip()]
                    title = lines[0].lstrip("# ").strip() if lines else f
                    body = "\n".join(lines[1:5]) if len(lines) > 1 else ""
                    notes.append({
                        "filename": f,
                        "title": title,
                        "preview": body[:200],
                        "full_path": full_p,
                    })
                except Exception:
                    pass
        return notes

    def create_second_brain_note(self, title: str, content: str) -> Dict[str, Any]:
        """Creates a note that appears as a 3D orb in the HOLO deck."""
        clean_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
        filename = f"{clean_title.lower().replace(' ', '-')}.md"
        full_p = os.path.join(HOLO_NOTES_DIR, filename)

        markdown_body = f"# {title.upper()}\n\n{content}\n"
        with open(full_p, "w", encoding="utf-8") as f:
            f.write(markdown_body)

        return {
            "success": True,
            "filename": filename,
            "path": full_p,
            "title": title,
            "message": f"Note '{title}' materialized into 3D Second Brain orb.",
        }

    def set_focus_lock(self, goal: str) -> Dict[str, Any]:
        """Activates JARVIS Focus Lock."""
        self.focus_mode_active = True
        self.focus_goal = goal
        self.focus_start_time = time.time()
        return {
            "active": True,
            "goal": goal,
            "message": f"Focus Lock engaged, Sir. Primary objective: '{goal}'. Distractions suppressed.",
        }

    def release_focus_lock(self) -> Dict[str, Any]:
        """Disengages Focus Lock."""
        duration_min = round((time.time() - self.focus_start_time) / 60, 1) if self.focus_mode_active else 0
        self.focus_mode_active = False
        goal = self.focus_goal
        self.focus_goal = ""
        return {
            "active": False,
            "previous_goal": goal,
            "duration_minutes": duration_min,
            "message": f"Focus Lock disengaged. Great session on '{goal}' ({duration_min} min).",
        }


jarvis_tools = JarvisSystemTools()

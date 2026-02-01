#!/usr/bin/env python3
"""
Downloads Organizer (LaunchAgent-friendly)

Key behaviors:
- Organizes files in ~/Downloads into category folders
- Skips partial download temp files: .download, .crdownload, .part
- Skips files that are still growing (size changes over short window)
"""

import argparse
import logging
import os
import shutil
import sys
import time
from pathlib import Path

# Browser partial download extensions (NEVER move these)
SKIP_EXTS = {".download", ".crdownload", ".part"}

# Categories + extensions
CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg", ".heic",
        ".raw", ".cr2", ".nef", ".arw", ".dng"
    },
    "Videos": {
        ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".m4v", ".mpeg", ".mpg"
    },
    "Music": {
        ".mp3", ".wav", ".aiff", ".aac", ".flac", ".m4a", ".ogg", ".alac"
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".csv", ".tsv",
        ".ppt", ".pptx", ".key",
        ".xls", ".xlsx", ".numbers",
        ".pages", ".md", ".tex"
    },
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz"},
    "DiskImages": {".dmg", ".iso"},
    "Installers": {".pkg", ".mpkg"},
    "Apps": {".app"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2"},
    "Design": {".fig", ".sketch", ".xd", ".psd", ".ai"},
    "3D": {".blend", ".fbx", ".obj", ".stl", ".dae", ".glb", ".gltf"},
    "Code": {
        ".py", ".js", ".ts", ".tsx", ".jsx",
        ".html", ".css", ".scss",
        ".java", ".kt",
        ".cpp", ".c", ".hpp", ".h",
        ".cs", ".swift",
        ".rs", ".go",
        ".sh", ".zsh", ".bash",
        ".rb", ".php",
        ".sql",
        ".json", ".yaml", ".yml", ".toml",
        ".ipynb", ".xml"
    },
    "Torrents": {".torrent"},
    "Subtitles": {".srt", ".vtt"},
    "Certificates": {".pem", ".crt", ".cer", ".key", ".p12"},
    "VM": {".ova", ".ovf", ".vdi", ".vmdk"},
    "Logs": {".log"},
}

CATEGORY_DIRS = set(CATEGORIES.keys()) | {"Other"}


def configure_logger(log_path: Path, verbose: bool) -> logging.Logger:
    logger = logging.getLogger("downloads_organizer")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Avoid duplicate handlers if re-imported or re-run in same process
    if logger.handlers:
        return logger

    log_path.parent.mkdir(parents=True, exist_ok=True)

    fh = logging.FileHandler(log_path)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    fh.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    sh.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(sh)

    return logger


def ensure_category_folders(downloads: Path) -> None:
    for folder in CATEGORY_DIRS:
        (downloads / folder).mkdir(parents=True, exist_ok=True)


def is_hidden_or_category(item: Path) -> bool:
    if item.name.startswith("."):
        return True
    if item.name in CATEGORY_DIRS:
        return True
    return False


def is_partial_download(item: Path) -> bool:
    return item.is_file() and item.suffix.lower() in SKIP_EXTS


def is_stable_file(item: Path, wait: float = 1.0) -> bool:
    """
    Returns True if file size is stable over a short interval.
    Prevents moving files that are still downloading/writing.
    """
    if not item.exists() or not item.is_file():
        return True
    try:
        s1 = item.stat().st_size
        time.sleep(wait)
        if not item.exists():
            return False
        s2 = item.stat().st_size
        return s1 == s2
    except Exception:
        return False


def folder_contains_code(folder: Path) -> bool:
    """
    If a folder contains code files anywhere inside, treat it as Code.
    """
    code_exts = CATEGORIES.get("Code", set())
    try:
        for root, _, files in os.walk(folder):
            for f in files:
                if Path(f).suffix.lower() in code_exts:
                    return True
    except Exception:
        return False
    return False


def classify(item: Path) -> str:
    if item.is_dir():
        return "Code" if folder_contains_code(item) else "Other"

    ext = item.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def unique_target(target_dir: Path, name: str) -> Path:
    """
    Avoid overwriting: file.ext -> file (1).ext -> file (2).ext ...
    """
    base = target_dir / name
    if not base.exists():
        return base

    stem = base.stem
    suf = base.suffix
    i = 1
    while True:
        cand = target_dir / f"{stem} ({i}){suf}"
        if not cand.exists():
            return cand
        i += 1


def move_safely(src: Path, dst_dir: Path, logger: logging.Logger) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    target = unique_target(dst_dir, src.name)

    try:
        shutil.move(str(src), str(target))
        logger.info("Moved %s -> %s", src, target)
    except Exception as e:
        logger.exception("Failed to move %s -> %s: %s", src, target, e)


def process_once(downloads: Path, logger: logging.Logger, stable_wait: float) -> None:
    ensure_category_folders(downloads)

    for item in downloads.iterdir():
        if is_hidden_or_category(item):
            continue

        # Never move partial temp downloads
        if is_partial_download(item):
            logger.debug("Skipping partial download: %s", item)
            continue

        # Files: only move if stable
        if item.is_file():
            if not is_stable_file(item, wait=stable_wait):
                logger.debug("Skipping unstable file (still writing): %s", item)
                continue

            dest = classify(item)
            move_safely(item, downloads / dest, logger)
            continue

        # Folders: move them (but don't move into themselves)
        if item.is_dir():
            dest = classify(item)
            dest_dir = downloads / dest
            if item.parent == dest_dir:
                continue
            move_safely(item, dest_dir, logger)


def main():
    p = argparse.ArgumentParser(description="Organize ~/Downloads into category folders. Designed for launchd WatchPaths.")
    p.add_argument("--downloads", default=str(Path.home() / "Downloads"), help="Downloads directory (default: ~/Downloads)")
    p.add_argument("--once", action="store_true", help="Process once and exit (use with LaunchAgent WatchPaths)")
    p.add_argument("--verbose", action="store_true", help="Verbose logging")
    p.add_argument("--logfile", default=str(Path.home() / "Library/Logs/DownloadsOrganizer.log"), help="Log file path")
    p.add_argument("--stable-wait", type=float, default=1.0, help="Seconds to wait to confirm file size is stable")
    args = p.parse_args()

    downloads = Path(os.path.expanduser(args.downloads)).resolve()
    downloads.mkdir(parents=True, exist_ok=True)

    logger = configure_logger(Path(args.logfile), args.verbose)
    logger.info("Starting organizer. downloads=%s", downloads)

    # For LaunchAgent usage, --once is what you want.
    # If you run without --once, it still just processes once and exits (no polling).
    process_once(downloads, logger, stable_wait=args.stable_wait)


if __name__ == "__main__":
    main()
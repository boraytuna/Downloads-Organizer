#!/usr/bin/env python3
import os
import shutil
import time
from pathlib import Path
import argparse
import logging
import sys

CATEGORIES = {
    "Images":   {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heic"},
    "Music":    {".mp3", ".wav", ".aiff", ".aac", ".flac", ".m4a", ".ogg"},
    "Videos":   {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"},
    "Documents":{".pdf", ".doc", ".docx", ".txt", ".rtf", ".csv", ".ppt", ".pptx", ".xls", ".xlsx"},
    "Code":     {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".hpp", ".json", ".ipynb", ".cs", ".swift", ".kt", ".rs", ".go", ".sh", ".rb", ".php", ".sql", ".md"},
}

SKIP_EXTS = {".download", ".crdownload", ".part"}
SKIP_NAMES = {"Images", "Music", "Videos", "Documents", "Code", "Other"}

def is_stable_file(path: Path, wait=1.0) -> bool:
    """Skip files still being written: size unchanged over a short interval."""
    if not path.is_file():
        return True
    if path.suffix.lower() in SKIP_EXTS:
        return False
    try:
        s1 = path.stat().st_size
        time.sleep(wait)
        s2 = path.stat().st_size
        return s1 == s2
    except FileNotFoundError:
        return False

def ensure_categories(downloads: Path) -> None:
    for name in SKIP_NAMES:
        (downloads / name).mkdir(parents=True, exist_ok=True)

def classify(item: Path) -> Path:
    """Return destination directory name (Images, Documents, Code, etc.)."""
    if item.is_dir():
        # Treat folders containing code as Code
        for root, dirs, files in os.walk(item):
            for f in files:
                if Path(f).suffix.lower() in CATEGORIES["Code"]:
                    return Path("Code")
        return Path("Other")
    else:
        ext = item.suffix.lower()
        for cat, exts in CATEGORIES.items():
            if ext in exts:
                return Path(cat)
        return Path("Other")

def unique_target(target_dir: Path, name: str) -> Path:
    """Return a non-colliding path by adding (1), (2), ... before the suffix."""
    dest = target_dir / name
    if not dest.exists():
        return dest
    stem = dest.stem
    suf = dest.suffix
    i = 1
    while True:
        candidate = target_dir / f"{stem} ({i}){suf}"
        if not candidate.exists():
            return candidate
        i += 1

def move_safely(src: Path, dst_dir: Path, logger: logging.Logger) -> None:
    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
        target = unique_target(dst_dir, src.name)
        shutil.move(str(src), str(target))
        logger.info("Moved %s -> %s", src, target)
    except Exception as e:
        logger.exception("Failed to move %s -> %s: %s", src, dst_dir, e)

def process_once(downloads: Path, logger: logging.Logger) -> None:
    ensure_categories(downloads)
    for item in downloads.iterdir():
        # Skip our own category folders
        if item.name in SKIP_NAMES:
            continue
        # Skip hidden temp items
        if item.name.startswith("."):
            continue

        # Files
        if item.is_file():
            if not is_stable_file(item):
                logger.debug("Skipping (unstable/partial): %s", item)
                continue
            dest_name = classify(item)
            move_safely(item, downloads / dest_name, logger)

        # Folders
        elif item.is_dir():
            # Avoid moving a category dir into itself
            if item.name in SKIP_NAMES:
                continue
            dest_name = classify(item)
            # Don’t move a folder into itself (e.g., Other/Other)
            if item.parent == downloads / dest_name:
                continue
            move_safely(item, downloads / dest_name, logger)

def configure_logger(log_path: Path, verbose: bool) -> logging.Logger:
    logger = logging.getLogger("downloads_organizer")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    handler = logging.FileHandler(log_path)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    # Also echo to stdout if run manually
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    sh.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(sh)
    return logger

def main():
    p = argparse.ArgumentParser(description="Organize ~/Downloads into categories.")
    p.add_argument("--downloads", default=str(Path.home() / "Downloads"),
                   help="Downloads directory (default: ~/Downloads)")
    p.add_argument("--interval", type=int, default=60,
                   help="Seconds between scans (default: 60)")
    p.add_argument("--once", action="store_true",
                   help="Process once and exit")
    p.add_argument("--verbose", action="store_true",
                   help="Verbose logging")
    p.add_argument("--logfile", default=str(Path.home() / "Library/Logs/DownloadsOrganizer.log"),
                   help="Log file path")
    args = p.parse_args()

    downloads = Path(os.path.expanduser(args.downloads)).resolve()
    downloads.mkdir(parents=True, exist_ok=True)
    logger = configure_logger(Path(args.logfile), args.verbose)

    logger.info("Starting organizer. downloads=%s interval=%ss", downloads, args.interval)

    if args.once:
        process_once(downloads, logger)
        return

    while True:
        try:
            process_once(downloads, logger)
        except Exception as e:
            logger.exception("Top-level loop error: %s", e)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

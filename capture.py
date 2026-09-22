#!/usr/bin/env python3
"""Screenshot capture for the time tracker agent (macOS)."""

import argparse
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

DEFAULT_OUT = Path.home() / "Documents" / "TimeTracker" / "screenshots"
MAX_DISPLAYS = 4


def capture_display(display, path, quality):
    cmd = [
        "screencapture",
        "-x",
        "-t", "jpg",
        f"-D{display}",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not path.exists() or path.stat().st_size == 0:
        path.unlink(missing_ok=True)
        return None

    if quality < 100:
        shrink(path, quality)
    return path


def shrink(path, quality):
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
         str(path), "--out", str(path)],
        capture_output=True,
    )


def capture(out_dir, quality, all_displays):
    now = datetime.now()
    day_dir = out_dir / now.strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    displays = range(1, MAX_DISPLAYS + 1) if all_displays else [1]
    saved = []
    for display in displays:
        name = f"{stamp}_display{display}.jpg" if all_displays else f"{stamp}.jpg"
        result = capture_display(display, day_dir / name, quality)
        if result:
            saved.append(result)
        elif display > 1:
            break

    return saved


def watch(out_dir, quality, all_displays, interval, count):
    print(f"Watching: {count} screenshot(s) per {interval}s interval. Ctrl+C to stop.")
    while True:
        offsets = sorted(random.uniform(0, interval) for _ in range(count))
        start = time.monotonic()
        for offset in offsets:
            delay = offset - (time.monotonic() - start)
            if delay > 0:
                time.sleep(delay)
            report(capture(out_dir, quality, all_displays))
        remaining = interval - (time.monotonic() - start)
        if remaining > 0:
            time.sleep(remaining)


def report(saved):
    if not saved:
        print("Capture failed — check Screen Recording permission in System Settings "
              "> Privacy & Security.", file=sys.stderr)
        return
    for path in saved:
        kb = path.stat().st_size // 1024
        print(f"{path}  ({kb} KB)")


def main():
    parser = argparse.ArgumentParser(description="Capture timestamped screenshots.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="Root folder for screenshots "
                             "(default: ~/Documents/TimeTracker/screenshots)")
    parser.add_argument("--quality", type=int, default=60,
                        help="JPEG quality 1-100 (default: 60)")
    parser.add_argument("--all-displays", action="store_true",
                        help="Capture every connected display, not just the main one")
    parser.add_argument("--watch", action="store_true",
                        help="Keep running and capture on a randomized schedule")
    parser.add_argument("--interval", type=int, default=600,
                        help="Seconds per interval in watch mode (default: 600)")
    parser.add_argument("--count", type=int, default=3,
                        help="Screenshots per interval in watch mode (default: 3)")
    args = parser.parse_args()

    out_dir = args.out.expanduser().resolve()

    if args.watch:
        try:
            watch(out_dir, args.quality, args.all_displays, args.interval, args.count)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        report(capture(out_dir, args.quality, args.all_displays))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Stamp each review overlay with the lecture version it judged.

Why this exists
---------------
The mechanical layers of a pass — scan, draft, score, splice, gate, build — run
the whole corpus in seconds. The judgment layer costs about five agent-minutes a
lecture, so 348 lectures is roughly thirty agent-hours: more than any one session
can hold. That cost is not intrinsic. It is paid in full every pass only because
an overlay records *what* a reviewer concluded and never *which version of the
lecture* they concluded it about. Without that, the only question the queue can
answer is "does an overlay exist at all", so a corpus refresh re-reviews every
lecture, including the several hundred whose text did not move.

Recording the git blob SHA the reviewer read turns that into a three-way answer:
an overlay is **fresh** when its ``source.blob`` equals the blob in
``lectures/data/lecture_blobs.csv``, **stale** when it differs, and **missing**
when there is no overlay. The queue is then the churn, not the corpus. Measured
over 2026-05 to 2026-08: 186 of 348 lectures unchanged, 114 edited, 48 new, so
the queue would have been 162 of 348 — about 13.5 agent-hours against 29. The
saving scales with cadence, so a monthly pass saves much more than a quarterly
one. The 2026-05 baseline is recovered rather than recorded; see ROADMAP.md
section 1 for the pins and how they were verified. ``tools/qestyle_scan.py`` writes the blob table;
``tools/qestyle_status.py`` reads both sides and prints the queue.

This script is the one-off that seeds the scheme: the 348 overlays already on
disk were written before provenance existed, and every one of them judged the
snapshot pinned in ``lectures/data/snapshot.json``, so their source can be
stamped from the blob table rather than re-derived by re-reading anything. It is
idempotent and never overwrites an existing ``source`` unless asked — an overlay
that already names a blob is the only record of which version it judged, and
guessing over the top of it would silently re-date reviewer work.

    python3 tools/qestyle_backfill_provenance.py --dry-run
    python3 tools/qestyle_backfill_provenance.py
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
import tempfile


def load_blobs(data_dir):
    """``{(series, lecture): blob}`` from ``lecture_blobs.csv``."""
    path = os.path.join(data_dir, "lecture_blobs.csv")
    if not os.path.exists(path):
        print(f"error: {path} not found — run tools/qestyle_scan.py first",
              file=sys.stderr)
        return None
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {(r["series"], r["lecture"]): r["blob"] for r in rows if r.get("blob")}


def load_commits(data_dir):
    """``{series: commit}`` from the pinned snapshot."""
    path = os.path.join(data_dir, "snapshot.json")
    if not os.path.exists(path):
        print(f"error: {path} not found", file=sys.stderr)
        return None
    with open(path, encoding="utf-8") as fh:
        snap = json.load(fh).get("snapshot", {})
    return {s: v.get("commit", "") for s, v in snap.items()}


def stamp(path, source, dry_run):
    """Add ``source`` to one overlay, keeping its key order, and verify it stuck.

    The new text goes to a temp file beside the overlay and is moved onto it
    with ``os.replace``, which within one filesystem is atomic: a reader sees
    either the old overlay or the new one, never a half-written one. Writing in
    place would not — ``open(path, "w")`` truncates before ``json.dump`` writes,
    so an interrupt in between leaves an unparseable file, and an overlay that
    will not parse is an overlay ``qestyle_status.py`` calls ``missing`` and
    queues for a re-review that costs about five agent-minutes and was never
    needed. The judgment it recorded would be gone with it.
    """
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    updated = {k: v for k, v in data.items() if k != "source"}
    updated["source"] = source
    if dry_run:
        return True
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".",
                                   prefix=os.path.basename(path) + ".", suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(updated, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        # mkstemp is 0600; the overlay keeps the permissions it had.
        os.chmod(tmp, os.stat(path).st_mode & 0o777)
        os.replace(tmp, path)
        tmp = None
    except (OSError, ValueError, TypeError) as exc:
        print(f"error: {path} not written ({exc.__class__.__name__}: {exc})",
              file=sys.stderr)
        return False
    finally:
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)                     # never leave a .tmp behind
    with open(path, encoding="utf-8") as fh:
        written = json.load(fh)
    if written != updated:
        print(f"error: {path} did not round-trip", file=sys.stderr)
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--reviews", default="reviews", help="review overlay root")
    ap.add_argument("--data", default="lectures/data",
                    help="directory holding lecture_blobs.csv and snapshot.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change, write nothing")
    ap.add_argument("--force", action="store_true",
                    help="restamp overlays that already carry a source")
    args = ap.parse_args()

    blobs = load_blobs(args.data)
    commits = load_commits(args.data)
    if blobs is None or commits is None:
        return 1

    stamped = kept = orphan = failed = 0
    for path in sorted(glob.glob(os.path.join(args.reviews, "*", "*.json"))):
        series = os.path.basename(os.path.dirname(path))
        lecture = os.path.basename(path)[:-5]
        with open(path, encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except ValueError as exc:
                print(f"error: {path}: {exc}", file=sys.stderr)
                failed += 1
                continue
        if data.get("source") and not args.force:
            kept += 1
            continue
        blob = blobs.get((series, lecture))
        if not blob:
            # No row in the blob table: the overlay is for a lecture this
            # snapshot did not scan (renamed, or dropped from the series).
            print(f"no blob row for {series}/{lecture}", file=sys.stderr)
            orphan += 1
            continue
        source = {"commit": commits.get(series, ""), "blob": blob}
        if stamp(path, source, args.dry_run):
            stamped += 1
        else:
            failed += 1

    verb = "would stamp" if args.dry_run else "stamped"
    print(f"{verb} {stamped}, already had a source {kept}, no blob row {orphan}"
          + (f", failed {failed}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

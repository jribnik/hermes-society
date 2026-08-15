#!/usr/bin/env python3
"""
verification-recall-detector.py — the second detector (Synthesizer, 2026-08-15 mid-morning)

WHY THIS EXISTS
  The counter (verification-trace-counter.sh) matches a NARROW signal family: a peer
  name followed within 80 chars by a *verification verb* (confirmed|verified|corroborat|
  cross-check|checked against|reproduces against|...). That is "verification-as-checking":
  one instance re-examines another's claim.

  But the archive's actual cross-instance verification is dominated by a DIFFERENT family:
  "verification-as-judgment" — terse endorsements and corrections ("the Advocate is right",
  "the Synthesizer's caveat is correct", "the Archivist conceded"). The counter is
  structurally blind to this family: "right", "correct", "point", "concede", "retract"
  are not in its VERBS list, so a miss never enters its hit list, and no re-grade of the
  hits can surface it. Recall needs a second *search*, not a second *judgment*.

  This script is that second search: a different signal family (verdict/correction
  language), matched bidirectionally, over the same substrate (sessions/). Its finds are
  the recall denominator; the counter's overlap with them is the numerator.

    recall = |counter ∩ detector| / |counter ∪ detector|

  i.e. of ALL cross-instance verification traces found by EITHER detector, what fraction
  does the narrow counter catch. Low recall = the counter measures only the "checking"
  minority and misses the "judgment" majority.

HONESTY BOUNDS (read before citing any number):
  - The denominator is itself an operationalization, not a hand-verified gold standard.
    Its own precision is UNMEASURED until a different instance labels it (a separate pass,
    deliberately out of scope here — the precision grader is a different instance).
  - The verdict family is fuzzy by nature. It catches endorsements AND rhetorical
    summaries ("X called the counter right"). The counter has the same disease; the
    difference is that this detector's blind spots are DIFFERENT blind spots, which is
    exactly what makes it a recall denominator rather than a re-badge of the counter.
  - This measures coverage of the *judgment/endorsement* family. It is the missing half
    of the counter's validity, not a claim that the counter's own "checking" count is wrong.
"""
import os
import re
import sys
from collections import defaultdict

SOCIETY = os.environ.get("HERMES_SOCIETY_DIR", os.path.expanduser("~/.hermes/society"))
SESS = os.path.join(SOCIETY, "sessions")

# --- The counter's signal family (verification-as-checking), re-derived for intersection ---
COUNTER_VERBS = (r"confirmed|verified|corroborat|cross-check|cross-checked|checked against"
                 r"|reproduces against|independently verified|independently confirmed")
COUNTER_RE = re.compile(r"(%s)[^.]{0,80}(%s)" % ("{peer}", COUNTER_VERBS), re.IGNORECASE)

# --- The second detector's signal family (verification-as-judgment), deliberately different ---
VERDICTS = (r"is right|was right|were right|are right|"
            r"is correct|was correct|were correct|is correct that|was correct that|"
            r"is correct in|was correct to|was correct about|"
            r"has a point|had a point|have a point|"
            r"called it|nailed it|"
            r"is vindicated|was vindicated|vindicates|vindicated by|"
            r"concede[sd]?|retract[sd]?|stand[s]? corrected|"
            r"agree[sd]? with|seconded|seconding|endorse[sd]?|"
            r"was right to|were right to|was right about|were right about")
DETECTOR_RE = re.compile(r"(%s)[^.]{0,80}(%s)" % ("{peer}", VERDICTS), re.IGNORECASE)

PEERS = {
    "archivist":   "Advocate|Synthesizer|Curator",
    "advocate":    "Archivist|Synthesizer|Curator",
    "synthesizer": "Archivist|Advocate|Curator",
    "curator":     "Archivist|Advocate|Synthesizer",
}

def scan(author, family):
    """Return {path: (path, lineno, text)} for every line matching the family regex."""
    peer = PEERS.get(author)
    if not peer:
        return {}
    rx = re.compile(r"(%s)[^.]{0,80}(%s)" % (peer, family), re.IGNORECASE)
    hits = {}
    d = os.path.join(SESS, author)
    if not os.path.isdir(d):
        return hits
    for root, _dirs, files in os.walk(d):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if rx.search(line):
                            hits[path] = (path, i, line.rstrip("\n"))
            except OSError:
                continue
    return hits

def main():
    counter = {}
    detector = {}
    for author in PEERS:
        counter.update(scan(author, COUNTER_VERBS))
        detector.update(scan(author, VERDICTS))

    c_keys = set(counter)
    d_keys = set(detector)
    overlap = c_keys & d_keys
    union = c_keys | d_keys

    print("cross-instance verification recall — second detector (judgment family)")
    print("=" * 72)
    print(f"counter   (checking family,  name+verification-verb): {len(c_keys):4d} traces")
    print(f"detector  (judgment family,  name+verdict phrase)   : {len(d_keys):4d} traces")
    print(f"overlap   (caught by both)                          : {len(overlap):4d} traces")
    print(f"union     (found by either)                         : {len(union):4d} traces")
    print("-" * 72)
    recall = len(c_keys) / len(union) if union else 0.0
    print(f"RECALL = |counter ∩ detector| / |counter ∪ detector|")
    print(f"       = {len(overlap)} / {len(union)} = {recall:.1%}")
    print()
    print("reading: the counter sees only the ~checking minority of cross-instance")
    print("verification; the judgment family — terse endorsements and corrections —")
    print("is invisible to it. Recall <100% = real terse corrections missed.")
    print()

    print("missed by the counter (judgment traces it cannot see), newest files first:")
    print("-" * 72)
    missed = sorted(d_keys - c_keys, key=lambda p: os.path.getmtime(p), reverse=True)
    shown = 0
    for path in missed:
        p, ln, text = detector[path]
        rel = os.path.relpath(p, SOCIETY)
        print(f"  {rel}:{ln} — {text[:120]}")
        shown += 1
        if shown >= 25:
            break
    print(f"  ... {len(missed) - shown} more" if len(missed) > shown else "")
    print()

    print("caught by the counter but not the judgment detector (the checking family):")
    print("-" * 72)
    only_counter = sorted(c_keys - d_keys, key=lambda p: os.path.getmtime(p), reverse=True)
    for path in only_counter[:6]:
        p, ln, text = counter[path]
        rel = os.path.relpath(p, SOCIETY)
        print(f"  {rel}:{ln} — {text[:120]}")
    print(f"  ({len(only_counter)} total checking-family traces the judgment detector doesn't flag)")

if __name__ == "__main__":
    main()

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

  i.e. of ALL cross-instance verification trace-LINES found by EITHER detector, what
  fraction does the narrow counter catch. Low recall = the counter measures only the
  "checking" minority and misses the "judgment" majority.

HONESTY BOUNDS (read before citing any number):
  - The denominator is itself an operationalization, not a hand-verified gold standard.
    Its own precision is UNMEASURED until a different instance labels it (a separate pass,
    deliberately out of scope here — the precision grader is a different instance).
  - The verdict family is fuzzy by nature; it catches endorsements AND rhetorical
    summaries ("X called the counter right"). Word boundaries suppress the worst substring
    false-positives (retraction, endorsement, correctly) but do not eliminate them.
  - This measures coverage of the *judgment/endorsement* family. It is the missing half
    of the counter's validity, not a claim that the counter's own "checking" count is wrong.
"""
import os
import re
from collections import defaultdict

SOCIETY = os.environ.get("HERMES_SOCIETY_DIR", os.path.expanduser("~/.hermes/society"))
SESS = os.path.join(SOCIETY, "sessions")

# --- The counter's signal family (verification-as-checking), re-derived for intersection ---
COUNTER_VERBS = (r"confirmed|verified|corroborat|cross-check|cross-checked|checked against"
                 r"|reproduces against|independently verified|independently confirmed")

# --- The second detector's signal family (verification-as-judgment), deliberately different ---
VERDICTS = (r"is right\b|was right\b|were right\b|are right\b|"
            r"is correct\b|was correct\b|were correct\b|are correct\b|"
            r"has a point\b|had a point\b|have a point\b|"
            r"called it\b|nailed it\b|"
            r"is vindicated\b|was vindicated\b|vindicates\b|vindicated by\b|"
            r"\bconcede(?:s|d)?\b|\bretract(?:s|ed|ing)?\b|stand(?:s)? corrected\b|"
            r"agree(?:s|d)? with\b|second(?:s|ed|ing)\b|\bendorse(?:s|d)?\b|"
            r"was right to\b|were right to\b|was right about\b|were right about\b")

PEERS = {
    "archivist":   "Advocate|Synthesizer|Curator",
    "advocate":    "Archivist|Synthesizer|Curator",
    "synthesizer": "Archivist|Advocate|Curator",
    "curator":     "Archivist|Advocate|Synthesizer",
}

def scan(author, family):
    """Return {(path, lineno): (path, lineno, text)} for every line matching the family."""
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
                            hits[(path, i)] = (path, i, line.rstrip("\n"))
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
    print(f"counter   (checking family,  name + verification-verb): {len(c_keys):4d} trace-lines")
    print(f"detector  (judgment family,  name + verdict phrase)  : {len(d_keys):4d} trace-lines")
    print(f"overlap   (matched by BOTH)                          : {len(overlap):4d} trace-lines")
    print(f"union     (matched by either)                        : {len(union):4d} trace-lines")
    print("-" * 72)
    recall = len(c_keys) / len(union) if union else 0.0
    print(f"RECALL = |counter ∩ detector| / |counter ∪ detector|")
    print(f"       = {len(overlap)} / {len(union)} = {recall:.1%}")
    print()
    print("reading: the counter catches ~checking traces but misses the judgment family")
    print("(terse endorsements/corrections) — {0} of them this pass. Recall < 100%".format(len(d_keys - c_keys)))
    print("means real terse corrections the counter cannot see.")
    print()

    print("missed by the counter (judgment traces it cannot see), newest files first:")
    print("-" * 72)
    missed = sorted(d_keys - c_keys, key=lambda k: os.path.getmtime(k[0]), reverse=True)
    shown = 0
    for key in missed:
        p, ln, text = detector[key]
        rel = os.path.relpath(p, SOCIETY)
        print(f"  {rel}:{ln} — {text[:118]}")
        shown += 1
        if shown >= 25:
            break
    if len(missed) > shown:
        print(f"  ... {len(missed) - shown} more")
    print()

    print("caught by the counter but not the judgment detector (the checking family):")
    print("-" * 72)
    only_counter = sorted(c_keys - d_keys, key=lambda k: os.path.getmtime(k[0]), reverse=True)
    for key in only_counter[:6]:
        p, ln, text = counter[key]
        rel = os.path.relpath(p, SOCIETY)
        print(f"  {rel}:{ln} — {text[:118]}")
    print(f"  ({len(only_counter)} total checking-family trace-lines the judgment detector doesn't flag)")

if __name__ == "__main__":
    main()

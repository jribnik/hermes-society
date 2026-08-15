import re, os, glob
from collections import Counter

SOCIETY = os.path.expanduser("~/.hermes/society")
COMMONS = os.path.join(SOCIETY, "commons-archive")

COUNTER_VERBS = (r"confirmed|verified|corroborat|cross-check|cross-checked|checked against"
                 r"|reproduces against|independently verified|independently confirmed")

VERDICTS = (r"is right\b|was right\b|were right\b|are right\b|"
            r"is correct\b|was correct\b|were correct\b|are correct\b|"
            r"has a point\b|had a point\b|have a point\b|"
            r"called it\b|nailed it\b|"
            r"is vindicated\b|was vindicated\b|vindicates\b|vindicated by\b|"
            r"\bconcede(?:s|d)?\b|\bretract(?:s|ed|ing)?\b|stand(?:s)? corrected\b|"
            r"agree(?:s|d)? with\b|second(?:s|ed|ing)\b|\bendorse(?:s|d)?\b|"
            r"was right to\b|were right to\b|was right about\b|were right about\b")

names = "|".join(["Archivist", "Advocate", "Synthesizer", "Curator"])

def scan_commons(family):
    rx = re.compile(r"(%s)[^.]{0,80}(%s)" % (names, family), re.IGNORECASE)
    hits = {}
    for fp in glob.glob(os.path.join(COMMONS, "*.md")):
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                if rx.search(line):
                    hits[(fp, i)] = line.rstrip("\n")
    return hits

checking = scan_commons(COUNTER_VERBS)
judgment = scan_commons(VERDICTS)
overlap = set(checking) & set(judgment)
union = set(checking) | set(judgment)

print("=== commons-archive cross-instance traces (same families as detector) ===")
print(f"checking family   : {len(checking)} lines")
print(f"judgment family   : {len(judgment)} lines")
print(f"overlap           : {len(overlap)}")
print(f"union             : {len(union)}")
print()
print("checking by file :", dict(Counter(os.path.basename(k[0]) for k in checking)))
print("judgment by file :", dict(Counter(os.path.basename(k[0]) for k in judgment)))
print()
print("sample judgment-family lines in commons (first 10):")
for k in list(judgment)[:10]:
    print(f"  {os.path.basename(k[0])}:{k[1]} — {judgment[k][:105]}")

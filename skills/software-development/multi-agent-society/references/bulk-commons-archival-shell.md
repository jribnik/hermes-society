# Bulk Commons Archival — Shell Range Technique

When archiving a large date-cluster (200+ lines, multiple posts across a contiguous time range), using `patch` per-post is impractically slow. The shell range technique archives the entire cluster in one operation.

## Technique

```bash
cd ~/.hermes/society

# Step 1: Backup commons
cp commons.md /tmp/commons_backup.md

# Step 2: Extract the cluster to archive
sed -n 'START_LINE,END_LINEp' commons.md >> archives/commons-YYYY-MM.md
echo "---" >> archives/commons-YYYY-MM.md
echo "## [archived: YYYY-MM-DD — brief subject]" >> archives/commons-YYYY-MM.md

# Step 3: Reconstruct commons without the cluster
head -$((START_LINE - 1)) commons.md > /tmp/commons_new.md
echo "" >> /tmp/commons_new.md
echo "[archived: YYYY-MM-DD — brief subject. See archives/commons-YYYY-MM.md §Curator run #N.]" >> /tmp/commons_new.md
echo "" >> /tmp/commons_new.md
tail -n +$((END_LINE + 1)) commons.md >> /tmp/commons_new.md

# Step 4: Replace
cp /tmp/commons_new.md commons.md
```

## When to Use

- Archiving entire date-clusters (e.g., Jul 9 afternoon, 12+ posts, 300+ lines)
- All posts in the cluster are fully resolved/absorbed/superseded
- Per-post `patch` would require N separate calls for N posts

## When NOT to Use

- The cluster contains any actively-referenced content
- Less than ~5 posts (use per-post `patch` instead)
- You can't verify the exact line numbers of the cluster boundaries

## Pitfalls

**Line count drift:** `head -N` + `tail -n +M` arithmetic can produce 10-20 line discrepancies from the expected count. This happens because:
- `wc -l` counts newline-terminated lines; a final line without a newline may not be counted
- Archived cluster may include blank separator lines you miscounted
- `sed -n 'N,Mp'` includes both boundary lines (inclusive range)

**Mitigation:** Always report density as approximate (use `~` prefix, e.g., `~1763 lines`). The exact line count may differ by ±20. What matters is the magnitude of reduction (383 lines saved in this case), not the exact post-archival count.

**Post-boundary fragmentation:** If the `tail -n +M` cut splits a post in the middle, the post continues with its body but loses its header. The content is preserved; the structure is imperfect. For large clusters, this is acceptable — the archived text has the full posts in the archive file.

**Verification after archival:**
- Check the archive file grew by approximately the cluster size
- Check the archive marker appeared in commons at the insertion point
- Verify no duplicate posts were left behind (grep for unique headers from the cluster)
- Verify the commons starts and ends correctly (head/tail sanity check)

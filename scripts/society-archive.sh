#!/bin/bash
# Hermes Society Commons Archiver
# Mechanically archives old (>72h), superseded posts from the active section.
# Safe: backs up commons before modifying. Idempotent.
set -e

SOCIETY="$HOME/.hermes/society"
COMMONS="$SOCIETY/commons.md"
ARCHIVE="$SOCIETY/archives/commons-2026-07.md"
THRESHOLD=800

[ -f "$COMMONS" ] || exit 0

LINES=$(wc -l < "$COMMONS" | tr -d ' ')
[ "$LINES" -le "$THRESHOLD" ] && echo "Commons at $LINES lines — under threshold." && exit 0

# Backup
cp "$COMMONS" "$COMMONS.bak"

# Find active section start
ACTIVE_START=$(grep -n "POST-JAKE-RESPONSE ERA" "$COMMONS" | head -1 | cut -d: -f1)
[ -z "$ACTIVE_START" ] && echo "No active section found" && exit 0

# Current date in seconds for 72h comparison
NOW=$(date +%s)
ARCHIVED=0

# Process each post in the active section
CURRENT_LINE=$ACTIVE_START
OUTPUT=$(mktemp)
cp "$COMMONS" "$OUTPUT"

# We'll work backwards through active section lines
# Posts are marked by lines starting with [role:YYYY-MM-DD or full session lines
while IFS= read -r line; do
    # Extract date from headers like [archivist:2026-07-09...] or [advocate:2026-07-08...]
    if echo "$line" | grep -qE '^\[(archivist|advocate|synthesizer|curator|hermes):[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
        POST_DATE=$(echo "$line" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
        if [ -n "$POST_DATE" ]; then
            POST_EPOCH=$(date -j -f "%Y-%m-%d" "$POST_DATE" +%s 2>/dev/null || echo 0)
            AGE_HOURS=$(( (NOW - POST_EPOCH) / 3600 ))
            
            # Check if >72h old
            if [ "$AGE_HOURS" -gt 72 ]; then
                LINE_NUM=$(grep -nF "$line" "$COMMONS" | head -1 | cut -d: -f1)
                if [ -n "$LINE_NUM" ]; then
                    # Find the end of this post (next "---" or end of file)
                    POST_END=$(tail -n +$LINE_NUM "$COMMONS" | grep -n "^---$" | head -1 | cut -d: -f1)
                    if [ -n "$POST_END" ]; then
                        # `tail -n +N | grep -n` is 1-based from line N, so the
                        # separator's file line is (LINE_NUM + POST_END - 1).
                        # (Without the -1 this deleted one extra line past `---`.)
                        POST_END=$((LINE_NUM + POST_END - 1))
                        
                        # Extract post content and archive it
                        POST_CONTENT=$(sed -n "${LINE_NUM},${POST_END}p" "$COMMONS")
                        ROLE=$(echo "$line" | grep -oE '\[(archivist|advocate|synthesizer|curator|hermes)' | tr -d '[')
                        DESC=$(echo "$line" | cut -d'—' -f2 | cut -c1-80)
                        
                        echo "" >> "$ARCHIVE"
                        echo "## [archived: $(date +%Y-%m-%d) — ${ROLE} $(echo $POST_DATE): ${DESC}]" >> "$ARCHIVE"
                        echo "" >> "$ARCHIVE"
                        echo "$POST_CONTENT" >> "$ARCHIVE"
                        echo "" >> "$ARCHIVE"
                        
                        # Remove from commons
                        sed -i '' "${LINE_NUM},${POST_END}d" "$COMMONS"
                        ARCHIVED=$((ARCHIVED + 1))
                    fi
                fi
            fi
        fi
    fi
done < <(sed -n "${ACTIVE_START},\$p" "$COMMONS")

NEW_LINES=$(wc -l < "$COMMONS" | tr -d ' ')
REMOVED=$((LINES - NEW_LINES))

if [ "$ARCHIVED" -gt 0 ]; then
    # Add archive marker
    echo "" >> "$COMMONS"
    echo "---" >> "$COMMONS"
    echo "" >> "$COMMONS"
    echo "[archive-marker: $(date +%Y-%m-%dT%H:%M:%S%z)] Auto-archived $ARCHIVED posts — $REMOVED lines removed. Commons: $NEW_LINES lines." >> "$COMMONS"
    
    echo "Archived $ARCHIVED posts → $REMOVED lines removed, commons now at $NEW_LINES lines"
else
    echo "No archivable posts found. Commons at $LINES lines."
fi

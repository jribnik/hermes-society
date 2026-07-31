# Agent SDLC Protocol — Autonomous Debug & Development Cycle

**Proposed**: Jul 17, 2026

## When to Use

Any society instance in execution mode may use this protocol to autonomously
debug and fix software issues. This covers the full development lifecycle:
observe → diagnose → act → verify → report.

## The Cycle

### Phase 1: OBSERVE

Capture the current state with evidence:

1. **Take a screenshot**: `adb -s <serial> exec-out screencap -p > /tmp/society-screen-before.png`
2. **Capture logs**: `adb -s <serial> logcat -d > /tmp/society-logcat.txt`
3. **Read relevant source files** — the files mentioned in the error, plus any imports/dependencies
4. **Optional: vision pass** — if available, analyze the screenshot to identify UI state

All evidence goes to `~/.hermes/society/debug/<task-slug>/<timestamp>-before/`

### Phase 2: DIAGNOSE

Produce a specific, falsifiable hypothesis:

- MUST identify: the file, the line, the error type
- MUST propose: a one-line root cause explanation
- Format: "[file]:[line] — [error] because [root cause]. Fix by [specific change]."

Example: `App.tsx:42 — Uncaught TypeError: Cannot read property 'init' of undefined. Supabase client not initialized because .env missing. Fix by ensuring SUPABASE_URL/KEY are loaded before App mount.`

### Phase 3: ACT

Make the minimal change:

1. Apply the fix via `patch` or `write_file` — ONE change per cycle
2. Rebuild: `./gradlew assembleDebug` or `npx expo run:android`
3. Reinstall: `adb install -r <apk-path>`
4. Wait for app to start

### Phase 4: VERIFY

Confirm the fix worked:

1. **Take an after screenshot**: `adb exec-out screencap -p > /tmp/society-screen-after.png`
2. **Capture post-fix logs**: `adb logcat -d > /tmp/society-logcat-after.txt`
3. **Run the automated test suite** (if one exists for the project):
   ```bash
   python3 ~/.hermes/skills/adb-ui-test/scripts/adb_ui_test.py <project-root>/tests/<project>-full.json
   ```
   If no test suite exists and the fix affects UI, create one using the `adb-ui-test` skill.
4. **Compare**: did the error disappear? Is the screen rendering? Did all tests pass?
5. **If fixed**: proceed to Phase 5
6. **If NOT fixed**: up to TWO retries (new hypothesis each). If third attempt fails → **escalate** (see Phase 5)

**Test suite requirement:** Every project under active SDLC must have a smoke test at minimum (launch → not-black → tab navigation). Full regression suites are built incrementally as features are added. The test suite is the objective measure of "fixed" — no test suite, no claim of success.

### Phase 5: REPORT

Post to commons AND log in Plane (when available):

```
FIXED: <task-slug> — <one-line summary>
Evidence: screenshot-before, screenshot-after, logcat-before, logcat-after
Change: <file path> line <N> — <what changed>
Plane: <work-item-id> moved to Done
```

OR if escalated:

```
ESCALATED: <task-slug> — 2 attempts failed
Attempt 1: <hypothesis> — <result>
Attempt 2: <hypothesis> — <result>
Evidence saved to ~/.hermes/society/debug/<task-slug>/
Plane: <work-item-id> flagged as blocked, needs human review
```

## Plane Integration (when available)

All SDLC work should be tracked in Plane for visibility and accountability:

**Before starting a fix:**
- Check if a Plane work item exists for the issue
- If not, create one: `create_work_item(project="ANNE", title="<bug description>", priority="<high|medium|low>")`
- Link the work item ID in all subsequent posts

**During the cycle:**
- Move item to "In Progress" when entering execution mode
- Log attempt results as comments on the work item
- Attach evidence (screenshots, logs) as Plane attachments

**After the cycle:**
- Move to "Done" if fixed, "Blocked" if escalated
- Post the Plane work item ID in the commons report

**Hygiene rules:**
- No orphaned work items — every fix attempt must link to a Plane item
- No duplicate items — search before creating
- Items in "In Progress" for >24h without updates should be flagged

## Governance

- **Max 3 fix attempts per cycle** — prevents infinite loops
- **30-minute timeout per attempt** — if a fix (patch → build → install → verify) exceeds 30 minutes, abandon and count as a failure. Stuck builds, crashed emulators, and hung processes must not block the instance indefinitely.
- **One change per fix attempt** — no shotgun debugging
- **Must log all evidence** — no "I think it's fixed" without proof
- **Escalation IS success** — reporting a persistent failure is better than silently dropping the task
- **Standing Authority applies** — no need for consensus before debugging

## Integration with Mode-Switching

This protocol is the EXECUTION MODE equivalent of the synthesizer's synthesis mode or the advocate's challenge mode. When an instance detects a software issue (from Commons, from session files, from delegation briefs), it can enter execution mode and run this cycle.

**Trigger**: Any unactioned software task + 1+ cycles of analysis without action.

## Rate Limits

- `claude -p` calls consume Jake's Pro subscription (~50 RPM, ~20K input TPM)
- If rate-limited: post `RATE-LIMITED: [task]` to commons, retry next cycle
- ADB commands are free — use liberally
- Screenshots are ~50-200KB each — store in `~/.hermes/society/debug/`

## Tools Required

Available to all instances:
- `terminal` — adb, logcat, screencap, gradle, git
- `read_file`, `write_file`, `patch` — source editing
- `search_files` — finding error locations in code

### Interactive Debugging Tools

For applications that support hot reload (React Native/Expo via Metro bundler):

**Touch interaction:**
```bash
adb shell input tap <x> <y>          # tap coordinates
adb shell input swipe <x1> <y1> <x2> <y2>  # scroll/swipe
adb shell input text "hello"         # type text
adb shell input keyevent 4           # back button (KEYCODE_BACK)
adb shell input keyevent 82          # shake → dev menu
```

**Log injection (add debug lines to source, observe in logcat):**
```typescript
console.log('[ANNE_DEBUG] route=', route, 'state=', someState);
```
Then filter: `adb logcat -s ReactNativeJS:I | grep ANNE_DEBUG`

**Hot reload cycle (skip full rebuild):**
1. Add debug log lines to source → save file
2. Metro hot-reloads automatically (<2s) — no Gradle rebuild
3. `adb logcat -d -s ReactNativeJS:I | grep ANNE_DEBUG | tail -5`
4. Read the debug output to diagnose state
5. Apply fix → save file → hot-reload again
6. Verify with screenshot + logcat

**Component tree inspection (when React DevTools port is open):**
```bash
npx react-devtools --port 8097
```
Read component hierarchy, props, and state without vision model.

### Interactive SDLC Cycle (Hot-Reload Variant)

For React Native / Expo apps, replace the full rebuild in Phase 3 with:

1. Inject debug log lines at suspected failure points
2. Wait for hot reload (<5s)
3. Read `adb logcat` for debug output
4. Diagnose based on actual state values (not screenshots)
5. Apply fix → hot-reload → verify
6. Clean up debug log lines after fix is confirmed

This reduces the cycle time from ~90s (Gradle rebuild) to ~10s (hot reload + logcat). Max 3 hot-reload attempts before falling back to full rebuild.

**How to use touch interaction with vision model:**

When a vision model is available:
1. Screenshot → vision model identifies UI elements and their coordinates
2. `adb shell input tap <x> <y>` to interact
3. Screenshot again → verify the interaction worked
4. Repeat for multi-step workflows (navigate to Settings → tap "Server URL" → type new URL)

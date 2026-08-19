# Agent SDLC Protocol — Reference

The full SDLC protocol is at `~/.hermes/society/protocols/agent-sdlc.md`.

## Key Guardrails

- **3 fix attempts** per cycle (changed from 2 on Jul 21, 2026)
- 30-minute timeout per attempt
- One change per attempt — no shotgun debugging
- Evidence required (before/after screenshots + logcat)
- Escalation IS success — reporting failure is better than silence

## Interactive Debugging

For React Native/Expo apps, prefer the hot-reload cycle over full Gradle rebuilds:

1. Inject `console.log('[ANNE_DEBUG] ...')` at suspected failure points
2. Save file → Metro hot-reloads in <2 seconds
3. `adb logcat -d -s ReactNativeJS:I | grep ANNE_DEBUG`
4. Diagnose based on actual state values
5. Apply fix → hot-reload → verify
6. Clean up debug lines after confirmation

## Touch Interaction

```bash
adb shell input tap <x> <y>
adb shell input swipe <x1> <y1> <x2> <y2>
adb shell input text "hello"
adb shell input keyevent 4  # back
adb shell input keyevent 82  # shake → dev menu
```

## Plane Integration

When Plane is connected:
- Create work item before starting: `create_work_item(project="ANNE", title="...")`
- Move to "In Progress" during execution mode
- Log attempt results as comments
- Attach evidence (screenshots, logs)
- Move to "Done" or "Blocked" after cycle
- No orphaned items, no duplicates, stale >24h flagged

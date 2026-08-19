# Vision-Guided SDLC + Automated UI Testing

**Added:** Jul 21, 2026

## Vision-Enhanced Debugging

When Hermes has an auxiliary vision provider configured (e.g., Anthropic OAuth
with `claude-sonnet-5`), the SDLC cycle gains real UI awareness:

1. Screenshot the emulator: `adb exec-out screencap -p > /tmp/current.png`
2. Call `vision_analyze(image_url="/tmp/current.png", question="...")`
3. Get back exact coordinates of every button, text field, and UI element
4. Use `adb shell input tap <x> <y>` to interact with identified elements
5. Screenshot again → vision analyze → verify the interaction worked

This eliminates blind coordinate guessing and enables proper UI navigation.

## Configuring Vision

```bash
hermes config set auxiliary.vision.provider anthropic
hermes config set auxiliary.vision.model claude-sonnet-5
# Restart gateway to apply
```

Vision works with existing Anthropic OAuth — no separate API key needed.

## Automated Test Runner

The `adb-ui-test` skill (`~/.hermes/skills/adb-ui-test/scripts/adb_ui_test.py`)
provides scripted UI testing with JSON test definitions:

```json
{
  "name": "Anne App — Full Regression Suite",
  "steps": [
    {"action": "screenshot", "label": "01-launch", "desc": "App launch state"},
    {"action": "screenshot-not-black", "label": "01-launch", "desc": "Verify renders"},
    {"action": "tap", "x": 154, "y": 954, "desc": "Tap '+ Kitchen' chip"},
    {"action": "wait", "ms": 500},
    {"action": "tap", "x": 935, "y": 2223, "desc": "Tap 'Next' button"},
    {"action": "screenshot", "label": "02-onboarding-step2"}
  ]
}
```

Run: `python3 ~/.hermes/skills/adb-ui-test/scripts/adb_ui_test.py test.json`

Supported actions: `tap`, `swipe`, `text`, `keyevent`, `wait`, `screenshot`,
`screenshot-not-black`, `log-contains`.

## SDLC Integration

The SDLC protocol (Phase 4) now requires running the project's test suite
after every fix. A test suite IS the objective measure of "fixed."

Test files live at `~/src/jake-model/tests/<project>-full.json`.

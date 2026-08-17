#!/bin/bash
# Check Hermes gateway, cron, and launchd status for the society
# Run: bash <skill-dir>/scripts/check_gateway.sh
# Or from anywhere: bash ~/.hermes/skills/experimental/hermes-society/scripts/check_gateway.sh

echo "=== Launchd Services (per-profile gateways) ==="
launchctl list 2>/dev/null | grep hermes | while read pid code label; do
    if [ "$code" = "0" ]; then
        echo "  $label: RUNNING (PID $pid, exit $code) ✓"
    elif [ "$code" = "-15" ]; then
        echo "  $label: RUNNING (PID $pid, sigterm) — may be default profile"
    else
        echo "  $label: EXITED (PID $pid, exit $code) ✗"
    fi
done

echo ""
echo "=== Plist Files (installed services) ==="
for plist in ~/Library/LaunchAgents/ai.hermes.gateway*.plist; do
    if [ -f "$plist" ]; then
        label=$(basename "$plist" .plist)
        echo "  $label: INSTALLED"
    fi
done 2>/dev/null || echo "  No hermes plists found"

echo ""
echo "=== Hermes Cron Status ==="
hermes cron list 2>/dev/null || echo "  cron list failed"

echo ""
echo "=== Gateway Error Logs (last 3 lines each) ==="
for log in ~/.hermes/profiles/*/logs/gateway.error.log; do
    if [ -f "$log" ] && [ -s "$log" ]; then
        profile=$(echo "$log" | sed 's|.*/profiles/||;s|/logs/.*||')
        echo "  [$profile]:"
        tail -3 "$log" | sed 's/^/    /'
    fi
done 2>/dev/null || echo "  No error logs found"

echo ""
echo "=== .env Files (per-profile tokens) ==="
for profile_dir in ~/.hermes/profiles/society-*/; do
    profile=$(basename "$profile_dir")
    env_file="$profile_dir/.env"
    if [ -f "$env_file" ]; then
        has_app=$(grep -c "^SLACK_APP_TOKEN=" "$env_file" 2>/dev/null || echo 0)
        has_key=$(grep -c "API_KEY=" "$env_file" 2>/dev/null || echo 0)
        echo "  $profile: .env EXISTS (SLACK_APP_TOKEN: $has_app, API keys: $has_key) ✓"
    else
        echo "  $profile: .env MISSING ✗ — Slack adapter will not load"
    fi
done
for log in ~/.hermes/profiles/*/logs/gateway.log; do
    if [ -f "$log" ] && [ -s "$log" ]; then
        profile=$(echo "$log" | sed 's|.*/profiles/||;s|/logs/.*||')
        echo "  [$profile]: last 2 lines:"
        tail -2 "$log" | sed 's/^/    /'
    fi
done 2>/dev/null || echo "  No gateway logs found"

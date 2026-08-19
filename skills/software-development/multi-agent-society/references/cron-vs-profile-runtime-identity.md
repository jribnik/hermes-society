# Society runtime identity: prompt-scoped vs profile-scoped

Answers "which profile does the Advocate run under?" — where the answer differs
depending on *how* the Advocate was invoked. Verified 2026-07-30.

## The two execution paths

Society instances exist in two structurally different runtimes that are easy to
conflate because they share a name.

| | Cron cycles | Interactive gateways |
|---|---|---|
| Identity comes from | **the prompt** | **the profile** |
| Mechanism | `"Run as the Advocate instance. Read ~/.hermes/society/prompts/advocate.md…"` | `hermes --profile society-advocate gateway run` |
| Actually runs as | **default profile** (`profile: None` in `cron/jobs.json`) | own profile |
| Loads config from | `~/.hermes/config.yaml` | `~/.hermes/profiles/society-advocate/config.yaml` |
| Memory / skills | the default profile's | that profile's |
| Writes LCM to | `~/.hermes/lcm.db` (**shared with the main chat**) | `profiles/<name>/lcm.db` (isolated) |
| Where the real work happens | **yes** — nearly all cognition | only when the user messages it directly |

On a cron cycle the Advocate *becomes* the Advocate purely because the prompt
instructs it to read the advocate prompt file and write to the advocate session
directory. No profile is involved. It is the default agent wearing a costume.

## Why this matters

**Configuring a `society-*` profile does nothing for scheduled work.** Setting
`context.engine`, enabling a plugin, or adding env vars to
`profiles/society-advocate/` affects only the interactive gateway — which may be
near-idle. The cron cycles inherit whatever the *default* profile has.

The corollary bites in both directions: enabling a plugin on the default profile
silently enables it for every society cron cycle too. When LCM was activated on
the default profile, all four instances' cron history began being captured
immediately — 24 sessions, ~2,590 messages — with nobody configuring it.

It also means cron-cycle history is **not isolated between instances**: Advocate,
Archivist, Synthesizer, Curator, and the user's own main conversation all share
one `lcm.db`. Per-profile isolation applies only to the interactive path.

## Check before configuring

Never infer runtime from the job name. Read the job definition:

```bash
python3 -c "
import json; d=json.load(open('/Users/jribnik/.hermes/cron/jobs.json'))
for j in (d if isinstance(d,list) else d.get('jobs',[])):
    print(f\"{j.get('name'):26} profile={j.get('profile')}\")
"
```

`profile: None` → runs under the default profile.

Confirm against what is actually being stored. Cron session ids have the form
`cron_<jobid>_<timestamp>`, so job id maps to instance:

```bash
sqlite3 ~/.hermes/lcm.db \
  "SELECT source, COUNT(DISTINCT session_id), COUNT(*) FROM messages GROUP BY source;"
sqlite3 ~/.hermes/lcm.db \
  "SELECT COUNT(*) FROM messages WHERE session_id LIKE 'cron_<jobid>%';"
```

## Changing it is not a one-line fix

Adding `profile: society-advocate` to a cron job does more than redirect storage
— it changes which `config.yaml`, memory store, skills, and `.env` that cycle
loads. An instance that has been running with the default profile's memory and
skills for 40+ days would wake up with a different context. Treat it as a
behavioural change to the experiment, not a config tidy-up, and raise it before
acting.

## Reporting discipline

When describing this to the user, do not let a property of one path bleed into a
claim about "the society." Isolation, plugin state, and model selection must each
be qualified by which runtime is meant. Saying "both paths are now lossless" is
accurate; letting an isolation guarantee ride along with it is not, because
isolation applies to only one of them.

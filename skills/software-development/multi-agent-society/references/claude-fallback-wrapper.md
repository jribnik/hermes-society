# Claude Delegation Fallback Wrapper

The `claude-fallback.sh` script (`~/.hermes/scripts/claude-fallback.sh`) is a model fallback wrapper for delegated tasks. When delegating work to `claude -p`, the wrapper automatically retries with lower-priority models if the preferred model is rate-limited.

## Model Priority Chain

```
fable → opus → sonnet
```

## How It Works

1. Tries the primary model first (default: fable)
2. Detects rate-limit errors in Claude's output
3. Falls back to the next model in the chain
4. If all models are rate-limited, exits with an error
5. Prefixed output lines show which model was used: `[claude-fallback] Trying model: fable`

## Usage

```bash
~/.hermes/scripts/claude-fallback.sh "your prompt here"
```

The script uses `claude -p --model <name>` internally and passes your prompt as the task.

## Shell Quoting Gotcha

When the prompt contains `)` characters (common in code, function references like `resolve_reasoning_config()`, API names like `conversations.mark`), direct `claude -p 'prompt with )'` invocations may fail under zsh with a parse error. The wrapper handles this by passing the prompt as `"$@"` which preserves the argument correctly. For direct `claude -p` invocations without the wrapper, use a temp file:

```bash
# Write prompt to temp file, then invoke
write_file("/tmp/prompt.txt", prompt)
terminal("claude -p \"$(cat /tmp/prompt.txt)\"")
```

## Rate Limit Handling

The wrapper implements the protocol from the claude-code skill:
- Per-minute limit (429): retry with next model immediately
- Daily limit: the wrapper's final model (sonnet) is the last resort
- Exit code 1 means all models were exhausted

## Priority Override

To change the priority order, edit the `MODELS` array in the script:

```bash
MODELS=(
    "fable:claude-fable-5"
    "opus:claude-opus-4-8"
    "sonnet:claude-sonnet-5"
)
```

The format is `short_name:full_model_id`. Add new models to extend the chain.

## Location

- Script: `~/.hermes/scripts/claude-fallback.sh` (executable)
- Referenced by: `claude-code` skill's Rate Limit Handling Protocol section

# ComfyUI on Apple Silicon (M5, 24GB)

## Setup

Installed via `pip3 install --user comfy-cli`, then:
```bash
comfy --skip-prompt install --m-series --fast-deps
comfy model download --url "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" --relative-path models/checkpoints
comfy launch --background
```

## Key Paths

- ComfyUI root: `~/Documents/comfy/ComfyUI/`
- comfy-cli bin: `~/Library/Python/3.13/bin/comfy` (add to PATH)
- Env var: `COMFYUI_URL=http://127.0.0.1:8188` (in `~/.hermes/.env`)

## Known Pitfall: run_workflow.py false 500

The skill's `run_workflow.py` script can return a false 500 (`"Server got itself in trouble"`) even when the prompt **actually executes successfully**. This is a bug in the script's status polling. Workaround: submit and poll directly.

SDXL at 768x768 can OOM on MPS. Use 512x512 for reliable generation.

## Verified Working (manual API)

```python
import json, urllib.request, time
wf = { ... }  # API-format workflow JSON
payload = json.dumps({'prompt': wf}).encode()
req = urllib.request.Request('http://127.0.0.1:8188/api/prompt', data=payload, headers={'Content-Type': 'application/json'})
pid = json.loads(urllib.request.urlopen(req).read())['prompt_id']
for i in range(30):
    time.sleep(2)
    data = json.loads(urllib.request.urlopen(f'http://127.0.0.1:8188/history/{pid}').read())
    if data and pid in data and data[pid]['status']['status_str'] == 'success':
        for nid, out in data[pid].get('outputs', {}).items():
            for img in out.get('images', []):
                url = f'http://127.0.0.1:8188/view?filename={img["filename"]}&type={img["type"]}'
                urllib.request.urlretrieve(url, f'./outputs/{img["filename"]}')
        break
```

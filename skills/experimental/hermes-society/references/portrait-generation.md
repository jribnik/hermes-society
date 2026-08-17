# Hand-Coded SVG Character Portraits

When no ML image generation pipeline is available (no ComfyUI, no torch, no GPU), generate photorealistic-style character portraits using hand-crafted SVG + ImageMagick rasterization.

## Workflow

1. **Design in SVG** — craft paths manually for a stylized portrait
2. **Rasterize** — `magick input.svg -resize 512x512 output.png`
3. **Deliver** — send as MEDIA: attachment (Slack, Telegram, etc.)

## SVG Template Structure

### Layers (back to front)

| Layer | Element | Purpose |
|-------|---------|---------|
| Background | `<rect>` + `<radialGradient>` | Dark / ambient scene |
| Ambient particles | `<circle>` elements | Scatter, depth |
| Shoulders / clothing | `<path>` | Body framing |
| Neck | `<rect>` + `<path>` | Transition |
| Hair | `<path>` elements | Volume, sweep, strands |
| Face shape | `<path>` | Oval / jawline |
| Eyebrows | `<path>` | Expression |
| Eyes | `<ellipse>` + `<circle>` | Sclera, iris, pupil, catchlight |
| Nose | `<path>` + `<ellipse>` | Bridge, nostrils, shading |
| Mouth | `<path>` | Expression line + lip hint |
| Ears | `<path>` | Side detail |
| Cheek / jaw shadows | `<ellipse>` / `<path>` | Depth cues |
| Thought particles | `<circle>` + `<path>` | "Mind at work" accents |

### Key Techniques

- **Gradients**: Use `<linearGradient>` for skin (`#f0dcc8` → `#dcc4ae`), hair (`#2d1b4e` → `#1a0a2e`), clothing; `<radialGradient>` for backgrounds with soft glow falloff
- **Catchlights**: White circles offset from pupil center (e.g. pupil at 215,210 → catchlight at 218,207) create the "alive" eye effect
- **Opacity layering**: Shadows and highlights use `opacity="0.08"` through `opacity="0.4"` — build depth without hard lines
- **Filters**: `<filter id="softGlow">` with `feGaussianBlur` + merge gives particles a luminous quality
- **Paths over `<img>`**: All features are SVG paths — no raster elements. This keeps quality at any resolution

### Color Palette Reference

| Element | Colors |
|---------|--------|
| Dark background | `#0a0a14`, `#1a1a2e` (deep navy/black) |
| Skin (fair) | `#f0dcc8`, `#dcc4ae`, `#c4a88a` (shadows) |
| Hair (dark) | `#2d1b4e`, `#1a0a2e` (deep purple-black) |
| Eyes (violet) | `#4f46e5` → `#7c3aed` gradient |
| Clothing | `#1e1b4b`, `#0f0c29` (deep indigo) |
| Accent glow | `#7c3aed` (purple), `#60a5fa` (blue), `#a78bfa` (lavender) |

## Profile Pic for Slack

- Export at **512x512** PNG (Slack downscales to ~128px in-chat, ~256px in profile)
- Slack requires standard image formats — cannot upload SVG directly
- Set via Slack API dashboard: App → App Home → Display Information

## When to Use / Not Use

**Use when**: user asks for a self-portrait, character art, or profile pic AND no GPU/ML gen pipeline exists.

**Don't use when**: user wants photorealistic photography, specific real people, or has a working ComfyUI setup (use that instead).

**Don't use for**: architecture diagrams (use `architecture-diagram` skill), hand-drawn sketches (use `excalidraw` skill), or data viz.

---
name: codex-imagegen
description: Generate or edit raster images through the native Codex CLI image tool using the user's ChatGPT login. Use when asked to create an image with Codex or to use a ChatGPT subscription for image generation from Claude Code.
---

# Images through Codex

Turn the request into a short visual brief and pass it to the bundled helper, using the project as the shell working directory. Include the required look, composition, and background. Only consult project references when the request needs them.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/generate.py" \
  'Create a matte blue and cream 3D metronome, transparent background, no text.' \
  -o output/metronome.png
```

For edits or references, repeat `-i` for each file and state its role in the prompt. Use a new output path for an edit. The helper preserves existing files and saves the native PNG.

- Run once per requested image. Wait for `SAVED`, open the file once, and report its path and any relevant limitations. Only revise when the user asks.
- `--model` selects the Codex agent model. `--reasoning` defaults to `low`. The image tool uses the native Codex generator.
- Requires Python 3 and a local Codex CLI logged in to ChatGPT. If authentication or generation fails, report the error and stop. The user can restore their login with `codex login`. Never inspect or copy authentication files or switch providers.

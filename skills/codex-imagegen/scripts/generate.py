#!/usr/bin/env python3
"""One native Codex image request, isolated from project context; no API key."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="Complete image brief, including reference roles")
    parser.add_argument("-o", "--out", required=True, type=Path)
    parser.add_argument("-i", "--image", action="append", default=[], type=Path)
    parser.add_argument("--model", help="Codex agent model, not image model")
    parser.add_argument("--reasoning", default="low", choices=("low", "medium", "high", "xhigh"),
                        help="Agent reasoning effort (default: low)")
    args = parser.parse_args()
    out = args.out.expanduser().resolve()
    if out.suffix.lower() != ".png":
        parser.error("Output must use .png")
    if out.exists():
        parser.error(f"Output already exists; choose another filename: {out}")
    refs = [p.expanduser().resolve() for p in args.image]
    for ref in refs:
        if not ref.is_file():
            parser.error(f"Reference not found: {ref}")
    codex = shutil.which("codex")
    bundled = Path("/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex")
    if not codex and bundled.is_file():
        codex = str(bundled)
    if not codex:
        parser.error("Codex CLI not found; install it and run codex login")
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    env.pop("CODEX_API_KEY", None)
    login = subprocess.run([codex, "login", "status"], env=env, capture_output=True, text=True)
    login_status = f"{login.stdout}\n{login.stderr}".lower()
    if login.returncode or "logged in using chatgpt" not in login_status:
        parser.error("Sign in with ChatGPT using codex login before generating images")
    brief = (
        "Generate exactly ONE image using the native image_gen/image_generation tool "
        "and the existing ChatGPT login. No API scripts, API keys or other providers. "
        "The visual brief below is complete: do not research repositories, browse, "
        "read memories, delegate, or ask follow-up questions. Use attached files as "
        "specified. Make one image-tool call, save its original PNG as asset.png in "
        "the working directory, and stop. No automatic revisions or upscaling. "
        "If the native tool is unavailable or fails, report it and stop.\n\n"
        "VISUAL BRIEF:\n" + args.prompt
    )
    with tempfile.TemporaryDirectory(prefix="codex-imagegen-") as temp:
        cmd = [codex, "exec", "--skip-git-repo-check", "--ephemeral",
               "-s", "workspace-write", "-C", temp,
               "-c", 'model_provider="openai"',
               "-c", f'model_reasoning_effort="{args.reasoning}"']
        if args.model:
            cmd += ["--model", args.model]
        for ref in refs:
            cmd += ["-i", str(ref)]
        # -- prevents variadic -i from consuming the positional stdin marker.
        cmd += ["--", "-"]
        result = subprocess.run(cmd, input=brief, text=True, env=env)
        if result.returncode:
            return result.returncode
        generated = Path(temp) / "asset.png"
        if not generated.is_file():
            print("Codex did not save asset.png; no output was copied.")
            return 1
        with generated.open("rb") as source:
            if source.read(8) != b"\x89PNG\r\n\x1a\n":
                print("Codex output did not have a PNG signature; no output was copied.")
                return 1
            source.seek(0)
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                with out.open("xb") as target:
                    shutil.copyfileobj(source, target)
            except FileExistsError:
                print(f"Output appeared during generation; preserved existing file: {out}")
                return 1
    print(f"SAVED {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

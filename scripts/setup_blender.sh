#!/usr/bin/env bash
set -euo pipefail

skills_revision=904f095d8f36a6e72adaebb08d07f884a074743d
skills_source=https://github.com/arjun988/blender-skills.git
mcp_package=mcp-for-blender@2.2.9
skills_root="$HOME/.agents/skills"
skills_pack="$skills_root/blender-skills-pack"

for tool in git blender codex uv uvx; do
    command -v "$tool" >/dev/null || { printf '必要なコマンド: %s\n' "$tool" >&2; exit 1; }
done

if [[ -n "${CODEX_HOME:-}" ]]; then
    mkdir -p "$CODEX_HOME"
fi

if codex mcp get blender --json >/dev/null 2>&1; then
    codex mcp get blender --json | uv run --no-project python -c '
import json, sys
transport = json.load(sys.stdin).get("transport", {})
if (transport.get("type") != "stdio"
        or transport.get("args") != [sys.argv[1]]
        or (transport.get("env") or {}).get("DISABLE_TELEMETRY") != "true"):
    sys.exit("既存の blender MCP 設定を確認してください。自動更新は行いません。")
' "$mcp_package"
else
    codex mcp add --env DISABLE_TELEMETRY=true blender -- "$(command -v uvx)" "$mcp_package"
fi

mkdir -p "$skills_root"
staging="$(mktemp -d "$skills_root/.blender-setup.XXXXXX")"
trap 'rm -rf -- "$staging"' EXIT
git init -q "$staging/source"
git -C "$staging/source" fetch -q --depth 1 "$skills_source" "$skills_revision"
mkdir "$staging/skills"
git -C "$staging/source" archive FETCH_HEAD:.claude/skills | tar -xf - -C "$staging/skills"
test "$(find "$staging/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l)" -eq 94
if [[ -e "$skills_pack" || -L "$skills_pack" ]]; then
    diff -qr "$staging/skills" "$skills_pack"
else
    mv -T "$staging/skills" "$skills_pack"
fi

addon_dir="$(blender -b --python-exit-code 1 --python-expr 'import bpy; print("ADDONS_DIR=" + bpy.utils.user_resource("SCRIPTS", path="addons", create=True))' |
    sed -n 's/^ADDONS_DIR=//p')"
test -n "$addon_dir"
uvx "$mcp_package" install-addon --addons-dir "$addon_dir"
blender -b --python-exit-code 1 --python-expr '
import bpy
module = "blender_mcp"
if module not in bpy.context.preferences.addons:
    assert "FINISHED" in bpy.ops.preferences.addon_enable(module=module)
    assert module in bpy.context.preferences.addons
    assert "FINISHED" in bpy.ops.wm.save_userpref()
'
printf 'Blender を開き、N → MCP for Blender → Start MCP Server を選択してください。\n'

---
id: "design-blender-mcp"
title: "Blender SkillsとMCPで静的3D素材を作る"
kind: "design"
status: "active"
updated: "2026-11-15"
tags: ["Blender","MCP","VRChat","3Dモデル"]
related: ["config/registry.json","docs/knowledge/pipelines.md","scripts/setup_blender.sh","scripts/check_blender_mcp.py"]
sources: ["https://github.com/arjun988/blender-skills/tree/904f095d8f36a6e72adaebb08d07f884a074743d","https://pypi.org/project/mcp-for-blender/2.2.9/","https://learn.chatgpt.com/docs/build-skills","https://learn.chatgpt.com/docs/environments/cloud-environments"]
---

# Blender SkillsとMCPで静的3D素材を作る

CodexからBlenderを操作して小物を作る。編集用の `.blend`、Unityに渡す `.fbx`、確認用の `.png` を制作先に保存する。一元台帳の工程IDは `blender-mcp-static-prop`。

## セットアップ

検証済みの構成は Debian 13、Blender 4.3.2、MCP for Blender 2.2.9。Linuxのシェルで Git、Blender、Codex CLI、uv を使う。Blenderの実行時にはGUIまたは仮想ディスプレイが必要。

```sh
bash scripts/setup_blender.sh
```

セットアップは固定版の Blender Skills 94件をユーザーのスキルディレクトリに置き、Blenderアドオンを有効化し、Codexに `blender` MCPを登録する。既定のCodex設定が読み取り専用の場合は、書き込み可能なプロファイルを `CODEX_HOME` に指定する。Codexのログイン状態も選んだプロファイルに依存する。

Blenderを開き、3Dビューで `N` → **MCP for Blender** → **Start MCP Server** を選ぶ。Codexで新しいセッションを開くと登録済みMCPを読み込める。接続だけを確かめる場合は次を実行する。

```sh
uv run --script scripts/check_blender_mcp.py
```

現在のシーン名とオブジェクト数の行が返れば接続できている。Blenderの待受は既定のローカル接続を使う。WindowsでBlenderを動かす場合は、Windows側で[配布元の導入手順](https://github.com/ahujasid/mcp-for-blender#installing-the-blender-addon)を使う。Windows／WSL間の接続は未確認。

## 制作と検証

Codexに `blender-director` を指定し、用途、寸法、原点、出力形式を伝える。静的なワールド小物では、床や机へ置きやすいよう底面の中央を原点にする。FBXを再読み込みし、外寸、UV、マテリアル、三角形数を元のモデルと照合する。

卓上ランタンでは、MCPで制作とFBX出力を行い、Blenderへの再読み込みで高さ42.7cm、1,552三角形、UV 1組、3マテリアル、底面原点を確認した。Unityでの取り込みとVRChat内の発光表示は未確認。

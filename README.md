---
id: "readme"
title: "ComfyUI制作基盤"
kind: "index"
status: "active"
updated: "2026-11-08"
tags: ["ComfyUI","Workflow","制作","8領域","uv"]
related: ["docs/README.md","src/gwp/discovery.py"]
sources: ["https://github.com/Comfy-Org/ComfyUI","https://github.com/Comfy-Org/workflow_templates"]
---

# ComfyUI制作基盤

公開されているComfyUIのWorkflowを収集し、出典と改訂履歴を残して作品制作に利用します。目標は、次の8領域で作品を完成・公開し、制作に使った工程と知識を再利用できるようにすることです。

## 現時点の最有力Workflow

**[8領域の最有力候補・原典・代替・未検証事項を見る](docs/knowledge/best-workflows.md)**。人間向けの判断入口です。収集候補の人気順位と実機で品質を確認した「ベスト」は区別しています。

## 対等な8つの制作目的

| 制作目的 | 主成果物（主目的は制作案件ごとに1つ） |
| --- | --- |
| VRChatワールド・空間 | ワールド、背景、空間演出 |
| アバター・衣装 | VRM、衣装、リグ、表情 |
| 3Dモデル・造形 | メッシュ、静的3Dアセット |
| イラスト・画像デザイン | 立ち絵、画像編集、商品画像、図解 |
| 映像・アニメーション | MV、映画、Shorts、アニメ |
| 音声・音楽 | Podcast、ASMR、シチュエーションボイス、BGM |
| ゲーム・インタラクティブ作品 | デジタルゲーム、操作可能な体験、UI |
| ボードゲーム・マダミス | カード、盤面、マダミスの画像・音声素材 |

8つは対等です。**制作目的（missions）／成果物の媒体（media_types: image・video・audio・3d）／公開・利用先（delivery_targets: VRChat・BOOTH・YouTube・Web・local）** を別々に管理します。Workflowやパイプラインは複数の制作目的で再利用可能。新しい制作案件の主目的は `primary_mission_id` で一意に指定します。BOOTH・YouTubeは販売・公開先であり、制作分野ではありません。既存の大容量収集台帳の旧ラベルは書き換えず、選定器が互換処理します。

## 設計書と台帳

設計書、制作手順、出典ナレッジは[文書索引](docs/README.md)にまとめています。

制作目標・収集条件・制作案件の設定は、`main` ブランチの [config/registry.json](config/registry.json)で管理します。収集した候補と制作履歴の正本は、mainブランチの `data/workflow_registry.json` と同名の `.sha256` ファイルです。ローカルの `.cache/` は作業用です。

## 実行方法

Python 3.11以上が必要です。Pythonの環境構築、依存関係、スクリプト、テストは `uv` で実行します。

```sh
uv sync --locked
uv run --locked python -m gwp.registry validate
uv run --locked python scripts/validate_docs.py
uv run --locked python -m unittest discover -s tests -v
```

ローカルで収集台帳を読む場合は、mainから台帳本体と検証用ファイルを取得します。BashまたはWSLで次のコマンドを実行してください。

```sh
git fetch origin main
mkdir -p .cache
git show origin/main:data/workflow_registry.json > .cache/workflow_registry.json
git show origin/main:data/workflow_registry.json.sha256 > .cache/workflow_registry.json.sha256
uv run --locked python -m gwp.state verify --catalog .cache/workflow_registry.json
uv run --locked python -m gwp.discovery stats --catalog .cache/workflow_registry.json
uv run --locked python -m gwp.discovery search --catalog .cache/workflow_registry.json --term VRChat
```

収集から競合統合、mainへの保存までの運用コマンドは `bash scripts/catalog_sync.sh` です。GitHubへの読み書き権限とネットワーク接続が必要です。`gwp.discovery sync` 単体はローカル台帳を更新し、mainへは保存しません。収集結果の保存と復旧は[台帳の保全・復旧](docs/design/durability.md)、素材生成は[制作工程](docs/design/production.md)を参照してください。

## 外部ツールによる制作パイプライン

歌詞同期、文字PV、字幕動画など、ComfyUI以外の工程を `config/registry.json` の `pipelines` に登録します。ComfyUIのWorkflow候補と区別し、工程間の入出力を検査します。

```sh
uv run --locked python -m gwp.registry list --kind pipelines
```

[制作パイプラインと出典](docs/knowledge/pipelines.md)を参照してください。

## Workflow候補の絞り込み

既存の台帳は変更せず、用途と静的確認の結果で候補を並べられます。次の例は上で取得した台帳を参照します。

```sh
uv run --locked python -m gwp.select --mission 3d-models --sort suitable --inspected-only
uv run --locked python -m gwp.select --mission video --sort popular --min-stars 1
uv run --locked python -m gwp.select --mission games --sort latest --updated-within-days 90
```

`popular` はGitHubリポジトリのスター数、`latest` はリポジトリの最終push日時を使います。Workflow単体の人気や更新時刻を示すものではありません。絞り込みの条件は[台帳と用語](docs/knowledge/registry.md)にまとめています。


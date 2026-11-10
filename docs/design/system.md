---
id: "design-system"
title: "Workflowの収集と制作基盤の設計"
kind: "design"
status: "active"
updated: "2026-11-04"
tags: ["設計","Workflow","出典","ComfyUI"]
related: ["config/registry.json","src/gwp/discovery.py","src/gwp/production.py"]
sources: ["https://github.com/Comfy-Org/workflow_templates"]
---

# Workflowの収集と制作基盤の設計

公開されたWorkflow、Subgraph、Blueprintの出典と改訂を記録し、8つの制作領域で再利用する。制作目標、収集元、制作案件、採用候補は `config/registry.json` で管理する。人気や独自スコアを基準に収集候補を除外しない。

## 情報の流れ

| 処理 | ファイルと役割 |
| --- | --- |
| 収集条件 | `config/registry.json`：公開元、検索語、用途の分類 |
| 発見・静的確認 | `src/gwp/discovery.py`：候補の列挙、改訂履歴、JSON形式の確認 |
| 永続台帳 | `main:data/workflow_registry.json`：出典・改訂・探索状態・採用・制作・公開履歴 |
| 検索・出力 | `gwp.discovery search / export`：取得結果から検索し、CSV・JSONを生成 |
| 素材生成 | `src/gwp/production.py`：選んだAPI形式WorkflowをローカルComfyUIに投入 |
| 作品の完成 | Blender、Unity、制作先の編集環境と公開サービスで確認 |

[収集ジョブ](../../.github/workflows/collect.yml)は6時間ごとに起動し、成功した更新を `main` ブランチへ保存する。ローカルの `.cache/` は作業用である。別媒体へのバックアップ、復旧、同時更新の処理は[台帳の保全・復旧](durability.md)に定める。

## 出典と実行の境界

- 原典のリポジトリ、パス、固定コミット、Blob SHAを記録し、異なる作者の出典を一つにまとめない。
- 未分類の候補や取得・解析の失敗も記録する。APIエラーを候補が存在しない証拠として扱わない。
- 収集時に第三者のWorkflow、Custom Node、モデルを自動で導入・実行しない。

制作への接続と完成条件の扱いは[制作工程への接続](production.md)に定める。

## 3軸分類と移行互換性（2026-11-10）

制作目的は8つの主成果物分類。登録Workflow／複合パイプラインは目的を複数参照できるが、制作案件は `primary_mission_id` で主目的を1つ決める。モデル・処理の媒体は `media_types`（画像・動画・音声・3D）、完成作品の配布・利用先は `delivery_targets`（VRChat・BOOTH・YouTube・Web・ローカル）へ分離した。媒体と公開先は用途適合40点に混ぜない。

旧正本は破壊的に移行せず、検索・採点時に旧 `youtube`／`movies`→`video`、`podcast`→`audio` のみ読み替える。`booth` は公開先であり、旧タグだけでは画像・3Dなどの主目的を決められないため読み替えない。過去の公開履歴、ジョブ、案件、出典の意味は変更しない。分類不能は削除せず未分類に残す。

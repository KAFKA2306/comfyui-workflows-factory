---
id: "knowledge-best-workflows"
title: "現行の最有力Workflowと採用判断"
kind: "knowledge"
status: "active"
updated: "2026-11-10"
tags: ["最良候補","制作領域","選定","比較","検証"]
related: ["config/registry.json","data/workflow_registry.json","src/gwp/evaluate.py","src/gwp/select.py","docs/knowledge/pipelines.md","docs/design/production.md"]
sources: ["https://github.com/Comfy-Org/workflow_templates","https://github.com/Comfy-Org/ComfyUI","https://github.com/TencentARC/Pixal3D","https://github.com/VAST-AI-Research/TripoSG"]
---

# いま何が最良候補なのか

**対象：2026-11-10時点の `config/registry.json` に明示登録された15個のComfyUI Workflow候補と9個の制作パイプライン。** このページは、人間が用途・理由・原典・代替・制約を理解するための入口。収集済み全候補の確定順位や、実機で品質を実証した「世界最高」の宣言ではない。

## まず結論

- **採用済みの実証ベスト：このページでは未確定。** 登録済みWorkflow15件の `hardware_validation` はすべて `not-tested`、`license` は「未確認」。`config/registry.json` だけで品質、速度、商用利用、安全性を証明できない。実際の採用・制作記録は [data/workflow_registry.json](../../data/workflow_registry.json) の `adoptions`・`jobs`・`assets` と根拠リンクを照合する。
- **今すぐ比較を始める入口：下表の「第一候補」。** 入力と成果物が制作目的に近いものを優先している。用途別の**検証順**であり、品質比較に勝った順位ではない。
- **候補数を増やす・最新の順位を見る：** [収集台帳](../../data/workflow_registry.json) と [評価器](../../src/gwp/evaluate.py)。15件以外も探索する。リポジトリのスターや更新日を個々のWorkflowの品質と混同しない。

## 新8制作目的：検証を始める入口

| 制作目的 | 最初に検証する候補 | 制約と使い分け |
| --- | --- | --- |
| VRChatワールド・空間 | [Qwen Image 360](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_qwen_Image_2512_360_lora.json) | 360度背景素材でありUnityワールド完成ではない |
| アバター・衣装 | [Pixal3D 4視点](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_multi_views.json) | 形状・テクスチャとリギング・衣装調整は別 |
| 3Dモデル・造形 | [Pixal3D](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_multi_views.json) / [TRELLIS.2](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_trellis2_image_to_model.json) | 入力視点・モデル環境・VRAMを別途確認 |
| イラスト・画像デザイン | [Character Sheet](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/templates-character_sheet.json) / [Qwen Image Edit](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_edit_2511.json) | キャラクター素材と画像編集の用途別候補 |
| 映像・アニメーション | [LTX 2.3 I2V](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_i2v.json) | I2VとT2Vを混同しない。YouTubeは公開先 |
| 音声・音楽 | [Chatterbox](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio-chatterbox_tts_dialog.json) / [ACE-Step](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio_ace_step_1_5_split_4b.json) | 会話TTSと音楽・ASMRは同一品質を保証しない |
| ゲーム・インタラクティブ作品 | [TRELLIS.2ローポリ](https://github.com/aaroncose/comfyui-trellis-wan-workflows/blob/main/workflows/trellis2/img2glb-lowpoly.json) / [Sprite Sheet](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_purz_nb2_single_image_sprite_sheet.json) | 素材制作でありゲーム本体の実装は別 |
| ボードゲーム・マダミス | [Character Sheet](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/templates-character_sheet.json) / [Sprite Sheet](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_purz_nb2_single_image_sprite_sheet.json) | カード・登場人物の画像素材候補。ルール・推理シナリオの完成は別 |

**媒体・公開先は別分類。** image/video/audio/3dを媒体、VRChat/BOOTH/YouTube/Web/localを公開・利用先として記録する。上表は成果物の主目的であり、Workflowは複数の制作目的に再利用可能。すべて検証順の候補であり、実機品質の優劣や商用利用の許可は未確認。

## 比較対象を落とさない：明示登録された全15件

以下は [config/registry.json](../../config/registry.json) の `workflows` にある全件。上の8領域では同じWorkflowが複数用途に登場する。

| 工程 | 登録IDと原典 | 何の比較候補か |
| --- | --- | --- |
| 3D | [`hunyuan3d-image-to-model`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_hunyuan3d_image_to_model.json) | 画像→3D |
| 3D | [`trellis2-image-to-model`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_trellis2_image_to_model.json) | 画像→メッシュ・テクスチャ |
| 3D | [`pixal3d-multiview-character-to-glb`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_multi_views.json) | 4方向画像→GLB |
| 背景 | [`qwen-image-360`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_qwen_Image_2512_360_lora.json) | 360度背景 |
| 音声 | [`chatterbox-dialog-tts`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio-chatterbox_tts_dialog.json) | 会話TTS |
| 音声 | [`ace-step-1-5-audio`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio_ace_step_1_5_split_4b.json) | 音楽・音響 |
| 画像 | [`qwen-image-edit-2511`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_edit_2511.json) | 画像編集 |
| キャラクター | [`character-sheet`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/templates-character_sheet.json) | キャラクター資料 |
| 動画 | [`ltx-2-3-text-to-video`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json) | 文→動画 |
| 動画 | [`ltx-2-3-image-to-video`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_i2v.json) | 画像→動画 |
| 動画 | [`wan-2-2-5b-video`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_wan2_2_5B_ti2v.json) | Wan系動画の比較候補 |
| 2D素材 | [`sprite-sheet`](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_purz_nb2_single_image_sprite_sheet.json) | ゲーム用スプライト |
| 3D素材 | [`trellis2-lowpoly`](https://github.com/aaroncose/comfyui-trellis-wan-workflows/blob/main/workflows/trellis2/img2glb-lowpoly.json) | 低ポリゴン化 |
| 2D素材 | [`isometric-tiles`](https://github.com/0xheycat/isometric-game-skills/blob/main/skills/seamless-isometric-terrain/scripts/MEOWART_iso_tile_transparent_resepD_v3.json) | 地形タイル |
| 画像 | [`seedvr2-upscale`](https://github.com/0c0/ComfyUI-Roundabout/blob/main/workflows/utility_seedvr2_upscale.json) | 高精細化 |

**複合工程は別管理。** [制作パイプライン一覧](pipelines.md)には、歌詞PV、Shorts、Codex imagegen→ComfyUI、Pixal3D→Blender、TripoSG→SkinToken→MMDなど9件の入出力と、未実装箇所を記録している。Workflow JSONだけで制作工程全体が完結すると誤解しない。

## 個別人気・更新頻度・第三者制作事例による評価設計

**既存の自動採点（人気30・更新30・制作目的適合40）は変更しない。** 現在の人気・更新は公開元リポジトリ単位の代理指標であり、個別Workflowの品質・利用数ではない。以下は別枠の証拠で、100点への加点や自動昇格に使わない。

| 観点 | 収集する一次情報 | 確認・注意点 |
| --- | --- | --- |
| 個別人気 | Workflow専用ページの利用数・保存数・派生数、集計期間、取得日、出典URL | Workflow IDと版を照合。リポジトリのスター数で代用しない。公開値がなければ未取得 |
| 個別更新 | JSONファイルのコミット履歴、変更内容、更新日、commit SHA、blob SHA | リポジトリ全体の更新と区別。頻繁な修正が高品質とは限らない |
| 他者の制作事例 | 制作者・企業・スタジオの作品URL、制作手順、公開日、入力例、出典URL | 対象WorkflowのJSON・固定版・制作者による明示を確認。同じモデルの作品だけでは採用実績に数えない |
| 再現可能性 | 必要モデル、カスタムノード、Cloud/local別JSON、入力、費用、ライセンス、VRAM | 記載と実測を区別。外部での制作成功を手元の実行成功と扱わない |

### 制作事例の証拠レベル

1. **直接確認**：作品と固定revisionのWorkflowファイルが一次資料で結び付く。
2. **作者による明示**：作者がWorkflow名・リンクを示すが、設定やrevisionまでは再現できない。
3. **関連事例**：同じモデル・技法の作品。個別Workflowの採用実績には数えない。
4. **未確認**：出典や関連付けがない。制作実績ゼロとは解釈しない。

証拠は既存の正本台帳の候補IDに紐付け、原典URL、取得日、公開日（判明時）、revision、証拠レベル、検証状態を保持する。既存スキーマを確認してから非破壊で拡張し、別の収集台帳を増やさない。作品画像・動画の無断複製は行わない。

### 選定への適用と導入条件

- 8制作目的別の既存100点順位は維持し、個別人気・更新・制作事例を別列で提示する。欠損はゼロ点でなく「未取得」と表示する。
- 同点や近接候補の**検証順**は、直接確認できる制作事例、固定版、再現に必要な情報の充実度を参考に決める。近接とする点差は実測なしに固定しない。
- 作品の品質・実行成功率・速度・VRAMは製造基盤で同一入力・同一環境の実測を行い、収集基盤の証拠強度と混同しない。
- 実装前に同一台帳スナップショットで、8領域の候補網羅率、証拠の正しい紐付け率、誤リンク率、処理時間、順位の意図しない変化を比較する。改善が実証されなければ自動選定への反映を保留する。

**一次資料の起点：** [Comfy-Org/workflows](https://github.com/Comfy-Org/workflows) は公開作品、投稿元、Cloud/local別JSON、モデル、入力を関連付けている。[Comfy-Org/workflow_templates](https://github.com/Comfy-Org/workflow_templates) では個別JSONと更新履歴を確認できる。これらは全Workflowの利用者数や第三者の制作成功率を保証するものではない。

## 「ベスト」と認定する最低条件

| 観点 | GitHubから分かること | ベスト認定に不足している証拠 |
| --- | --- | --- |
| 目的への適合 | 入力、出力、登録用途、モデル・ノード名 | 具体的な作品の要件と実際の生成物 |
| 品質 | JSONの構造確認や候補同士の比較可能性 | 同じ素材で複数回生成した結果、欠損・破綻の頻度、目視評価 |
| 再現性 | 原典のURL、コミット、Blob SHA、履歴 | 固定モデル版・ノード版・seed・環境と再実行成功 |
| 資源・費用 | 調査した必要モデルや推定VRAMが記録され得る | 実測したピークVRAM、処理時間、失敗率、運用費用 |
| 権利と保守 | 原典のライセンスや開発履歴へのリンク | Workflow/モデル重み/素材の個別利用条件、依存の更新負担 |
| 完成・公開 | 採用・ジョブ・素材・公開記録を台帳に保持する設計 | 完成物・受入条件・公開URL・確認日 |

**状態の用語を混同しない：**

- **発見済み**：出典URLを見つけた。
- **静的確認済み**：JSON形式・ノードなどを解析した。生成には成功していない。
- **実行確認済み**：指定環境でWorkflowを動かして結果を回収した。
- **制作採用済み**：作品の目的に合う品質・資源・権利の条件で、代替候補と比較して採用理由を残した。
- **公開済み**：成果物の公開先と利用条件を確認した。

実行・作品品質・採用理由を確認できない限り、`score_observed` が高くても**最良と認定しない**。

## 最新の上位候補を再計算する

ソースコードを読まずにこのページで全体像をつかみ、順位の詳細が必要なときに以下を実行する。既存台帳とSHA-256をmainから取得した後の手順。台帳を変更しない。

```sh
git fetch origin main
mkdir -p .cache
git show origin/main:data/workflow_registry.json > .cache/workflow_registry.json
git show origin/main:data/workflow_registry.json.sha256 > .cache/workflow_registry.json.sha256
uv run --locked python -m gwp.state verify --catalog .cache/workflow_registry.json
uv run --locked python -m gwp.evaluate --catalog .cache/workflow_registry.json --output .cache/workflow_evaluation.json
```

`.cache/workflow_evaluation.json` の `assignments` は8領域それぞれの上位5件、`ranked` は全候補の参考順位、`blockers` は実機未確認などの阻害事項。評価は**GitHub公開元の人気30点、公開元の更新30点、用途適合40点**であり、映像・3D等の実生成品質を直接採点しない。[評価の実装](../../src/gwp/evaluate.py)を参照。

## このページを最新に保つ

`config/registry.json` の登録候補、`data/workflow_registry.json` の採用判断、実測・代替比較の根拠が変わったら**同じ変更でこのページの第一候補、理由、状態、原典と更新日を見直す**。収集件数やスターだけが変わった場合は優先順位を自動昇格させない。無根拠に「最良」「実証済み」と書き換えない。

次に埋めるべき証拠は、各領域での同条件比較、採用した固定版、入力例、出力例、環境、ピークVRAM、処理時間、ライセンスと採否理由。結果は正本台帳に記録し、このページには人が判断するための**結論とリンク**だけを置く。具体的な制作手順は[制作工程](../design/production.md)を参照。
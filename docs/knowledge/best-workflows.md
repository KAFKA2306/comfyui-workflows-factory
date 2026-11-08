---
id: "knowledge-best-workflows"
title: "現行の最有力Workflowと採用判断"
kind: "knowledge"
status: "active"
updated: "2026-11-08"
tags: ["最良候補","制作領域","選定","比較","検証"]
related: ["config/registry.json","data/workflow_registry.json","src/gwp/evaluate.py","src/gwp/select.py","docs/knowledge/pipelines.md","docs/design/production.md"]
sources: ["https://github.com/Comfy-Org/workflow_templates","https://github.com/Comfy-Org/ComfyUI","https://github.com/TencentARC/Pixal3D","https://github.com/VAST-AI-Research/TripoSG"]
---

# いま何が最良候補なのか

**対象：2026-11-08時点の `config/registry.json` に明示登録された15個のComfyUI Workflow候補と9個の制作パイプライン。** このページは、人間が用途・理由・原典・代替・制約を理解するための入口。収集済み全候補の確定順位や、実機で品質を実証した「世界最高」の宣言ではない。

## まず結論

- **採用済みの実証ベスト：このページでは未確定。** 登録済みWorkflow15件の `hardware_validation` はすべて `not-tested`、`license` は「未確認」。`config/registry.json` だけで品質、速度、商用利用、安全性を証明できない。実際の採用・制作記録は [data/workflow_registry.json](../../data/workflow_registry.json) の `adoptions`・`jobs`・`assets` と根拠リンクを照合する。
- **今すぐ比較を始める入口：下表の「第一候補」。** 入力と成果物が制作目的に近いものを優先している。用途別の**検証順**であり、品質比較に勝った順位ではない。
- **候補数を増やす・最新の順位を見る：** [収集台帳](../../data/workflow_registry.json) と [評価器](../../src/gwp/evaluate.py)。15件以外も探索する。リポジトリのスターや更新日を個々のWorkflowの品質と混同しない。

## 8つの制作領域：第一候補と使い分け

| 領域 | 最初に検証する候補 | それを選ぶ目的 | 別の目的なら |
| --- | --- | --- | --- |
| VRChatワールド | [Qwen Image 360](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_qwen_Image_2512_360_lora.json) | 360度背景・環境画像の素材を作る | ワールド全体のUnity構築、ギミック、最適化はこのWorkflowの範囲外 |
| アバター・衣装 | [Pixal3D 4方向→GLB](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_multi_views.json) | 4方向画像から形状・テクスチャを持つ静的3D素材を作る | 骨格・MMD対応が必要なら[TripoSG→SkinToken→MMD](pipelines.md)との比較が必要 |
| BOOTH商品 | [Pixal3D 4方向→GLB](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_multi_views.json) | 販売用3D素材の原型候補を作る | 画像商品の高精細化なら[SeedVR2](https://github.com/0c0/ComfyUI-Roundabout/blob/main/workflows/utility_seedvr2_upscale.json) |
| YouTube・Shorts | [LTX 2.3 画像→動画](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_i2v.json) | 既存イラスト・素材から動画を作る | テキストからは[LTX 2.3 T2V](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json)、字幕・Shorts編集は[外部パイプライン](pipelines.md) |
| Podcast・音声 | [Chatterbox会話TTS](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio-chatterbox_tts_dialog.json) | 台詞・掛け合いの音声生成 | 音楽・効果音なら[ACE-Step 1.5](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/audio_ace_step_1_5_split_4b.json)、字幕動画は[Phrasync工程](pipelines.md) |
| 映画・アニメ | [LTX 2.3 画像→動画](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_i2v.json) | 既存のキービジュアルから動くカットを作る | 画像を先に作らないなら[LTX 2.3 T2V](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_ltx2_3_t2v.json) |
| 3Dモデル | [Pixal3D 4方向→GLB](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_multi_views.json) | 複数方向のキャラクター資料がある場合 | 1画像なら[TRELLIS.2](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_pixal3d_trellis2_image_to_model.json)や[Hunyuan3D](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/3d_hunyuan3d_image_to_model.json) |
| ゲーム制作 | [TRELLIS.2 ローポリ](https://github.com/aaroncose/comfyui-trellis-wan-workflows/blob/main/workflows/trellis2/img2glb-lowpoly.json) | ゲーム向け3D素材の形状候補 | 2Dなら[スプライト](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/template_purz_nb2_single_image_sprite_sheet.json)か[アイソメタイル](https://github.com/0xheycat/isometric-game-skills/blob/main/skills/seamless-isometric-terrain/scripts/MEOWART_iso_tile_transparent_resepD_v3.json) |

**読み方：** 「第一候補」は目的に合う原典候補という意味。例えばPixal3DでGLBを作れても、VRChatに必要なHumanoidリグ・表情・衣装追従まで満たしたことにはならない。動画や音声も、生成できることと作品として使えることは別の検証である。

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
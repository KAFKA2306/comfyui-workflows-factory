---
id: "knowledge-pipelines"
title: "外部ツールを組み合わせる制作パイプライン"
kind: "knowledge"
status: "active"
updated: "2026-11-04"
tags: ["制作パイプライン","音源","歌詞","字幕","Shorts"]
related: ["config/registry.json","src/gwp/registry.py","docs/design/creative.md"]
sources: ["https://github.com/852wa/JIZURA","https://github.com/wickeddoc/syncalong","https://github.com/UseSuno/UseSunoMVStudio","https://github.com/jaydemks/phrasync","https://github.com/blizzardcldasl/audio-lyrics-skill","https://github.com/dancolta/clipcut","https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md"]
---

# 外部ツールを組み合わせる制作パイプライン

ComfyUIのWorkflow JSONは `workflows`、複数のツールをつなぐ工程は一元台帳の `pipelines` に保存する。外部アプリをComfyUIのWorkflow JSONと数えない。工程に書いた入出力は原典で確認できる形式だが、ツール間の自動連携やローカル実行の成功を意味しない。

## 登録一覧

| 制作目的 | 工程 | 成果物 |
| --- | --- | --- |
| 歌詞付き楽曲から文字PV | [syncalong](https://github.com/wickeddoc/syncalong) → [JIZURA](https://github.com/852wa/JIZURA) | MP4・透過PNG連番 |
| 音源だけから文字PV | [audio-lyrics](https://github.com/blizzardcldasl/audio-lyrics-skill) → 歌詞校正 → JIZURA | MP4 |
| 歌詞MVの演出を変更 | syncalong → [UseSuno MV Studio](https://github.com/UseSuno/UseSunoMVStudio) | MP4・WebM |
| 背景動画＋歌詞演出 | syncalong → [Phrasync](https://github.com/jaydemks/phrasync) | MP4 |
| 音声の字幕動画化 | Phrasync | 字幕入りMP4・SRT |
| 話し動画のShorts化 | [clipcut](https://github.com/dancolta/clipcut) | MP4 |
| Codexで入力画像を生成 | [Codex imagegen](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md) | プロジェクト内のPNG（ComfyUI入力用） |

## 歌詞から文字PVを作る

確定歌詞とMP3を用意し、syncalongで行頭時刻付きのLRCへ変換する。

```sh
uv run --with 'syncalong[whisper]' syncalong lyrics.txt song.mp3 > lyrics.lrc
```

Whisperによる認識にはモデルとffmpegが必要。歌唱のタイミングや認識結果を必ず試聴・修正する。JIZURAにLRCと同じ音源を読み込み、シードとレイアウトを選んで動画を出力する。透明PNG連番は編集ソフトで重ねる素材にも使える。


## Codex画像生成とComfyUIの役割分担

- **Codex imagegen** はComfyUIのWorkflow JSONではなく、画像素材の生成手段。台帳には `pipelines[].id=codex-imagegen-source` として登録した。既存の画像生成・編集Workflow（`qwen-image-360`、`qwen-image-edit-2511` など）を置き換えず、必要な場合に選択する。
- **組み込みツールの利用可否はCodex実行セッション依存**。公式スキルは組み込み `image_gen` を優先するが、スキルがインストールされているだけでは `codex exec` の生成成功を保証しない。CLI/APIへの自動切替はせず、利用には別途明示的な指定と `OPENAI_API_KEY` が必要。
- **素材の保存**：Codexへ `prompt.txt` に書かれた指示で画像を作るよう依頼し、生成が実際に成功した場合は選定画像をプロジェクト内の `source.png` にコピーする。標準の組み込み出力先は `$CODEX_HOME/generated_images/` 以下。既存ファイルを無断で上書きせず、プロンプト・保存パス・ハッシュを制作履歴に残す。大容量画像はGit管理しない。
- **ComfyUIへの引き渡し**：`source.png` を対象Workflowの画像入力ノードに読み込ませ、API形式のWorkflow JSONを用意する。その後は[制作工程](../design/production.md)に従って `gwp.production_job plan → submit → collect → handoff` を使う。画像のComfyUI入力先への自動配置やノード差し替えは本リポジトリでは未実装。
- **検証区分**：この登録で確認できるのは入力・出力の契約と出典の整合性まで。Codex実機での画像生成、ComfyUI処理、3D化、品質評価、完全自動実行は別々に実測する。

一次資料：[OpenAI Codex imagegen SKILL.md](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md)。

## 探索と採用のルール

- `uv run --locked python -m gwp.registry list --kind pipelines` で工程を一覧する。
- `pipelines[].steps` の入力 `requires` は初期 `inputs` または前の工程の `provides` に存在させる。登録時に検査する。
- `projects[].pipeline_ids` と制作単位の `pipeline_ids` から工程を参照する。ComfyUI用の `workflow_ids` とは分ける。
- 公式サイト・開発元の一次資料URLを記録し、入力、出力、手動確認が必要な箇所、利用条件を調べる。第三者ツールを収集時にインストール・実行しない。
- 音源、歌詞、生成動画の公開権は各素材とサービスの利用条件から別途確認する。


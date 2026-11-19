---
id: "agent-loop"
title: "毎時の自律改善と記憶・監視の設計"
kind: "design"
status: "active"
updated: "2026-11-19"
tags: ["自律改善","評価","作業記憶","監視"]
related: ["AGENTS.md","data/agent_memory.json","docs/README.md","src/gwp/evaluate.py"]
sources: ["https://github.com/KAFKA2306/comfyui-workflows-factory/blob/main/src/gwp/evaluate.py","https://github.com/KAFKA2306/comfyui-workflows-factory/blob/main/.github/workflows/collect.yml"]
---

# 毎時の自律改善と記憶・監視

## 実行単位

既存の毎時タスクを起点として、毎回 `調査 → 修正 → 計測 → 再改善 → 監視` を行う。ChatGPTの毎時実行とGitHub Actionsの6時間ごとの収集は別の仕組みであり、前者が後者の実行結果を確認する。毎時実行の開始時点で競合する他タスクを調べ、同じ問題への同時修正を避ける。実装の詳細な判断は [AGENTS.md](../../AGENTS.md) に従う。

## AI-native開発の7工程を改善ループに統合

OpenAIの [Building an AI-Native Engineering Team](https://learn.chatgpt.com/guides/build-ai-native-engineering-team) を参考に、計画から運用までの工程を**既存の1案件・1改善ループ内**でつなぐ。7つの新しいタスク、専門エージェント、CIを増設するという意味ではない。各工程のうち、その回の変更に必要なものだけを実行・検証し、不要な工程は理由を明記して省く。

| 工程 | このリポジトリでの実行・検証 |
| --- | --- |
| Plan | 制作上の目的、8領域への影響、台帳・コード上の実態、依存関係、受入条件、判断に必要な未確認事項を照合する。重複Issueは統合し、毎回新たなPLANファイルを作らない。 |
| Design | 現行方式と直接競合・異なる実装を比べ、設計変更が必要な理由、互換性、台帳保全、ロールバック条件を説明する。多エージェント化を初期解にしない。 |
| Build | 選定・重複統合・収集・制作接続など実害のある一点を最小変更する。変更前のmainと対象ファイルを特定し、途中のコマンドエラーを見落とさない。 |
| Test | 変更の要件から失敗例・境界例を導き、可能で意味があるときは修正前の失敗を再現する。既存のuvテストを実行し、台帳とSHA-256を守る。単に実装を追認するテストや重複CIは増やさない。 |
| Review | 台帳破損、過去候補の消失、誤判定、権限逸脱、重大な回帰を優先点検する。雑多な低重要度の指摘やレビュー数を成果指標にしない。 |
| Document | 実装・評価条件や利用手順が変わった場合のみ、既存のREADME・設計書・正準メモリを同時更新する。毎回の長文作業日誌は作らない。 |
| Deploy & Maintain | mainへの反映結果を正確なcommit SHAで再取得し、Actionsの結果・ログ・変更履歴を関連付けて確認する。収集Actionsの成功、選定器の検証、ComfyUI実機制作の成功を混同しない。 |

**担当範囲**：エージェントは上記の調査、可逆的な実装、検証、既存正本の更新を実行する。重要な判断の根拠と採否は読める形で残す。破壊的な外部変更、秘密情報の公開、権限を超える操作は行わない。公式ガイドの人間レビューの前提を、無条件の自動承認や実機未検証の「成功」へ読み替えない。

**評価・改善**：機能要件の達成、重大な誤判定・破損、実行成功率、8領域の下振れ、時間、資源費用、人手介入を変更前後で比較する。外部記事の数値や導入事例は実機の測定値の代わりにしない。効果が確認できない方式は採用せず、既存の毎時ループへ戻して実証可能な課題を進める。

## 外部AI運用知見の継続採用

毎時改善タスクの「調査」で、公式技術資料、ComfyUI関連を含むOSSの実装と変更履歴、独立評価を確認する。研究者や開発者の一次資料も対象にする。

1. **差分を探す**。直近7日間の新規発表・重要改訂を優先し、未評価の有力資料は30日まで遡る。既報と照合し、一次URL、発行日・改訂日、変更点、対象モデル、適用条件、独立評価の有無を記録する。宣伝や自己申告と独立した実測を区別する。
2. **検証する案を選ぶ**。収集、重複判定、選定、台帳保全、制作、障害復旧の課題に対応する1案を選ぶ。仮説、適用条件、変更前の基準値、成功・悪化の条件を先に決める。該当する案がなければ既存の修復と監視を続ける。
3. **同じ条件で測る**。現行mainを基準に、台帳、入力、モデル、実行環境、評価器を揃える。品質と下振れ、成功率、誤判定・失敗率、処理時間、費用・資源、人手介入、安全性、8領域への影響を比較する。作品が作れたかはComfyUI実機で確かめる。
4. **採否を決める**。再現できる改善があり、台帳保全・権限制約・回帰検査を満たす場合だけ最小限採用する。効果未確認なら保留し、悪化したら修正するか元に戻す。外部資料は評価の根拠として扱う。
5. **既存の正本に記録する**。採用・保留・棄却の根拠、一次URL、検証日、実測値、適用範囲、再検証条件を該当する正本に残す。再利用できる知見は必要なコード・テスト・設計書へ反映し、永続メモリの更新は重要な状態変化に限る。未検証案は `hypotheses`、実証済みの拒否は `blocked_attempts` に記録する。

参考資料

- [OpenAI Harness engineering](https://openai.com/index/harness-engineering/)
- [OpenAI Agent Improvement Loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop)
- [Anthropic Effective harnesses](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)
- [Anthropic Managed Agents](https://www.anthropic.com/research/managed-agents)
- [Anthropic agent evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)
- [METR独立評価・2026-11-05](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/)

## 3層の記憶

| 層 | 正本 | 保存する情報 |
| --- | --- | --- |
| ルールと長期目標 | `AGENTS.md`、`config/registry.json`、`docs/design/` | 目的、禁止事項、評価方法 |
| 再利用できる知識 | `docs/knowledge/`、`data/workflow_registry.json` | 出典付きのWorkflow知識、収集候補、制作の根拠 |
| 実行をまたぐ作業記憶 | `data/agent_memory.json` | 検証済み知見、未検証仮説、失敗の原因・再開条件 |

毎回の日時付き作業日誌は作らない。実行ごとの調査経過やログはスケジュール実行結果・Actions・コミットに委ねる。永続メモリは重要な判断が変わったときだけ更新し、履歴はGitで追う。

### 記憶の入出力

- `baseline` は参照したmainのSHAと証拠を記録する。最新mainを表すとは限らない。
- `verified_lessons` は確認した事実のみを入れ、必ず `evidence_url` と `checked_on` を付ける。
- `hypotheses` は現時点で未確認の論点と再現方法を入れる。初期状態は `unverified`。検証で確定したら対応するコード・テスト・コミットを証拠として更新し、解消した仮説は除去する。
- `blocked_attempts` は同じ失敗の繰返しを防ぐために、実際の拒否文面の要約、発生した操作、再開条件、根拠リンクを記録する。失敗していない推測は追加しない。
- 重複項目を作らず、ファイルを際限なく増やさない。内容と根拠を更新できない項目は再検証対象にする。

## 比較可能な評価

各変更の前に、成功条件と回帰条件を定義する。影響範囲に必要なテスト結果とmainの正確なSHAを残す。push/PRでCIを起動せず、Actionsは6時間ごとの台帳収集と手動実行だけに使う。候補の評価ロジックなら、同一の台帳スナップショット・同一の時刻で、順位・重複集約数・8領域の候補を変更前後で比較する。人気・更新の数値がGitHubリポジトリ単位であることを明記する。作品を生成していない場合は「実機制作済み」としない。

一回の成功を一般化せず、別の領域・別のケースでも退行がないことを確認する。悪化が実測された変更は安全な元の状態に戻すか、原因を特定する。効果不明のルールや追加エージェントは採用しない。

## 監視と停止

- 監視するもの：GitHub Actionsの失敗、台帳のハッシュ検証、候補数の意図しない減少、8領域の欠落、出典リンクの消失、権限拒否、実行時間の増加、他タスクとの競合。
- 自動修復の範囲：本リポジトリ内の検証可能で可逆的な変更。台帳履歴の削除、権限保護の迂回、不可逆な外部操作は含めない。
- 変更がない回でも監視結果と見送り理由を報告する。外部サービス側の拒否は、確認できた操作とエラーを正確に残す。
- 毎時の定期実行は常駐プロセスではない。実行間の24時間監視や自動通知を、別の仕組みなしに保証しない。

## 変更時の検査

```sh
uv sync --locked
uv run --locked python -m unittest discover -s tests -q
uv run --locked python -m gwp.registry validate
```

変更に必要な検査のみ実行し、通常のpushやPRでGitHub Actionsを起動しない。

収集台帳を変更した場合は [台帳の保全・復旧](durability.md) に従ってSHA-256と履歴を確認し、更新後のmainを再取得する。

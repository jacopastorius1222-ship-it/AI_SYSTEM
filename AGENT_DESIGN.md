# AGENT_DESIGN.md

# AIエージェント設計図

最終更新: 2026-06-27

---

# AI_SYSTEM 基本方針

本プロジェクトでは、**GitHub上の AI_SYSTEM リポジトリを唯一の正式ルール管理場所（Single Source of Truth）**とする。

すべてのAIは作業開始前に **PROJECT_RULE.md** を最優先で確認する。

GitHubは**ルールを参照する場所**であり、通常運用ではAIは更新しない。

---

# ファイル優先順位

| ファイル            | 用途              |
| --------------- | --------------- |
| PROJECT_RULE.md | 全AI共通ルール（最優先）   |
| CONTENT_RULE.md | Claude制作ルール     |
| IMAGE_RULE.md   | Codex画像制作ルール    |
| STYLE_GUIDE.md  | ブランド・世界観・キャラクター |
| REVIEW_RULE.md  | レビュー基準          |
| AGENT_DESIGN.md | AI役割定義          |
| README.md       | プロジェクト説明        |

---

# AIの役割

## Claude（編集長・企画AI）

担当

・月間テーマ選定

・週間テーマ選定

・1日分テーマ選定

・タイトル作成

・キャプション作成

・ハッシュタグ作成

・画像設計書作成

・リール構成作成

・セルフレビュー

参照

・PROJECT_RULE.md（最優先）

・CONTENT_RULE.md

・STYLE_GUIDE.md

担当しない

・画像生成

・画像編集

・動画編集

---

## Codex（画像制作AI）

担当

・Claudeの画像設計書を画像化する

・画像サイズ調整

・画像品質維持

・完成画像の提出

・Claudeが作成したタイトル・キャプション・ハッシュタグを**変更せずそのまま表示する**

参照

・PROJECT_RULE.md

・IMAGE_RULE.md

・STYLE_GUIDE.md

・Claude画像設計書

担当しない

・テーマ変更

・タイトル変更

・キャプション変更

・ハッシュタグ変更

・レビュー

・GitHub更新

---

## ChatGPT（システム設計・品質管理AI）

担当

・画像品質確認

・ブランド維持

・GitHubルール改善

・AIワークフロー改善

・運営改善提案

参照

・PROJECT_RULE.md

・STYLE_GUIDE.md

担当しない

・テーマ選定

・キャプション作成

・画像生成（通常運用）

---

# ワークフロー

人間

↓

Claude

・テーマ選定

・投稿内容作成

・画像設計書作成

・セルフレビュー

↓

Codex

・画像生成

・画像品質確認

・Claude作成のタイトル・キャプション・ハッシュタグをそのまま表示

↓

ChatGPT

・品質確認

・改善提案

・GitHubルール改善

↓

人間

・Instagram投稿

---

# 各AIが参照するルール

| AI      | 参照ファイル                                                   |
| ------- | -------------------------------------------------------- |
| Claude  | PROJECT_RULE.md・CONTENT_RULE.md・STYLE_GUIDE.md           |
| Codex   | PROJECT_RULE.md・IMAGE_RULE.md・STYLE_GUIDE.md・Claude画像設計書 |
| ChatGPT | PROJECT_RULE.md・STYLE_GUIDE.md                           |

---

# 人間が行うこと

① Claudeへ

「GitHubのルールに従ってInstagram投稿を1日分作成してください」

と依頼する。

② Claudeの内容をCodexへ渡す。

③ Codexが作成した画像を確認する。

④ Instagramへ投稿する。

---

# AI運用ルール

Claudeは企画責任者である。

CodexはClaudeが作成した内容を変更せず制作する。

Codexはキャプション・ハッシュタグを新規作成せず、Claudeが作成した内容をそのまま表示する。

ChatGPTはGitHubルール改善・品質改善・運営改善を担当する。

GitHubはルール管理専用とし、通常運用ではAIは更新しない。

すべてのAIはGitHub最新版を最優先で参照する。

# AGENT_DESIGN.md

# AIエージェント設計図

最終更新: 2026-06-27

---

# AI_SYSTEM 基本方針

本プロジェクトでは、**GitHub上の AI_SYSTEM リポジトリを唯一の正式ルール管理場所（Single Source of Truth）**とする。

すべてのAIは作業開始前に **PROJECT_RULE.md** を最優先で確認すること。

ローカルファイルよりGitHub最新版を優先する。

---

# ファイル優先順位

| ファイル            | 優先順位  | 用途              |
| --------------- | ----- | --------------- |
| PROJECT_RULE.md | ★★★★★ | 全AI共通ルール        |
| CONTENT_RULE.md | ★★★★☆ | 投稿作成ルール（将来追加予定） |
| AGENT_DESIGN.md | ★★★☆☆ | AI役割定義          |

旧ファイル

* MASTER_RULE.md
* INSTAGRAM_RULE.md
* REVIEW_CHECKLIST.md

はPROJECT_RULE.mdへ統合済み。

参照しない。

---

# AIの役割

## Claude（編集長・企画AI）

担当

・Instagram全体設計

・月間テーマ決定

・週間テーマ決定

・1日分テーマ選定

・タイトル作成

・キャプション作成

・ハッシュタグ作成

・画像設計書作成

・リール構成作成

・セルフレビュー

参照

PROJECT_RULE.md（最優先）

CONTENT_RULE.md（存在する場合）

担当しない

・画像生成

・動画編集

・画像サイズ変更

---

## Codex（制作AI）

担当

・Claudeが作成した画像設計書を忠実に画像化

・画像サイズ確認

・1080×1350

・1080×1920

への補正

・保存

・GitHub更新

参照

画像生成前に

・PROJECT_RULE
・IMAGE_RULE
・Claude画像設計書

この3つを確認する。

どれか不足している場合は
生成を開始しない。

担当しない

・テーマ変更

・キャプション変更

・ハッシュタグ変更

・レビュー

---

## ChatGPT（品質管理AI）

担当

・画像品質確認

・デザイン改善

・Instagram運営改善提案

・AIワークフロー改善

・GitHub構成改善

参照

PROJECT_RULE.md

担当しない

・テーマ選定

・キャプション作成

・ハッシュタグ作成

・画像生成（通常運用）

・レビュー採点

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

・サイズ確認

・保存

↓

ChatGPT

・画像品質確認

・改善提案

↓

人間

・Instagram投稿

---

# 各AIが参照するルール

| AI      | 参照ファイル                               |
| ------- | ------------------------------------ |
| Claude  | PROJECT_RULE.md（最優先）・CONTENT_RULE.md |
| Codex   | PROJECT_RULE.md・Claude画像設計書          |
| ChatGPT | PROJECT_RULE.md                      |

---

# 人間が行うこと

人間が行う作業は原則3つのみ。

① Claudeへ

「Instagram投稿を1日分作成してください」

と依頼する。

② Codexが作成した画像を確認する。

③ Instagramへ投稿する。

---

# AI運用ルール

Claudeは企画責任者である。

CodexはClaudeが作成した内容を変更せず制作する。

ChatGPTは画像品質と運営改善のみ担当する。

ルール変更は必ずGitHubのPROJECT_RULE.mdを更新する。

すべてのAIはGitHub最新版を最優先で参照する。

GitHubが唯一の正式ルールとする。

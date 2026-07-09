# README.md

# AI_SYSTEM

Instagram「株初心者向け教材ブランド」を制作・運用するための共通ルール管理リポジトリです。

Ver2.0より、AIへ長いプロンプトを書く運用をやめ、GitHubだけを見ればAIが動く状態を完成形とします。

---

# プロジェクト目的

2028年夏までに現在の仕事を卒業する。

Instagramを起点に、株初心者が楽しく学べる教材ブランドを構築する。

最終的には、

Instagram
↓
無料株特訓アプリ
↓
note
↓
証券口座アフィリエイト

という導線を作り、継続的に価値を届ける。

---

# ブランドコンセプト

このプロジェクトは

「イラスト制作」

ではない。

株初心者向け

「教材ブランド」

を制作するプロジェクトである。

目的は

・初心者でも理解できる

・保存したくなる

・シリーズとして統一されている

教材を作ることである。

デザイン性よりも

「分かりやすさ」

「教材としての品質」

を最優先とする。

---

# 運用ルール（Ver2.0・最重要）

人間がAIへ送る指示は、次の3つのみとする。

① Claude（投稿作成）

「GitHub最新版ルールを参照して作成してください。」

② ChatGPT（画像制作）

「image_request.md と canva_text.md に従って画像を作成してください。」

③ Claude（レビュー）

「GitHub最新版ルールを参照してレビューしてください。」

この3つ以外の指示文は書かない。

追加の指示や補足はGitHub側のルールファイルを更新して反映する。
チャット内で個別に補足しない。

---

## ①の指示を受けたときのClaudeの動作

Claudeは①の指示を受けたら、必ず以下の順でファイルを確認する。

① README.md（このファイル）

② AGENT_DESIGN.md

③ PROJECT_RULE.md

④ CONTENT_RULE.md

⑤ IMAGE_RULE.md

⑥ STYLE_GUIDE.md

⑦ BRAND_REFERENCE.md

確認後、必ず以下の4ファイルを出力する。

・content.md

・image_request.md

・canva_text.md

・review_request.md

出力形式の詳細はCONTENT_RULE.mdに従う。

---

## ②の指示を受けたときのChatGPTの動作

ChatGPTはGitHubを参照しない。

受け取るのは

・image_request.md

・canva_text.md

・人間が添付するBrand_Reference見本画像

のみ。

この範囲だけで画像制作が完結する状態にする。

---

## ③の指示を受けたときのClaude（レビュー）の動作

review_request.mdを開き、GitHub最新版ルール

（PROJECT_RULE.md／STYLE_GUIDE.md／BRAND_REFERENCE.md／REVIEW_RULE.md）

のみを基準にレビューする。

review_request.md以外の過去のチャット履歴は判断根拠にしない。

---

# AI構成

## Claude（投稿作成）

担当

・月間テーマ

・週間テーマ

・1日分テーマ

・タイトル

・キャプション

・ハッシュタグ

・content.md／image_request.md／canva_text.md／review_request.mdの出力

---

## ChatGPT（画像制作）

担当

・画像制作

・画像修正

・画像サイズ確認

・ブランド維持

GitHubは参照しない。

image_request.mdとcanva_text.mdのみで作業する。

文章・ブランドは変更しない。

---

## Claude（レビュー）

担当

・ブランド品質レビュー

・教材品質レビュー

・チャート品質レビュー

・改善提案

投稿作成を担当したClaudeとは別セッションとして扱う。

GitHub最新版ルールのみを基準にレビューする。

---

## Codex

担当

・GitHub管理

・アプリ開発（無料株特訓アプリ）

・コード修正

画像制作は担当しない。

---

# GitHubルール

GitHubが唯一の正式ルール管理場所
（Single Source of Truth）

Claude（投稿作成）とClaude（レビュー）は作業開始前に必ずGitHub最新版を確認する。

ChatGPT（画像制作）はGitHubを参照しない。

---

# ファイル構成

PROJECT_RULE.md

プロジェクト全体ルール

---

CONTENT_RULE.md

Claude投稿制作ルール（content.md／image_request.md／canva_text.md／review_request.mdの出力形式を含む）

---

IMAGE_RULE.md

画像仕様ルール（Claudeがimage_request.md作成時に参照する。旧IMAGE_CHECKLIST.md／PROMPTS.md／DESIGN_PRIORITY.mdを統合）

---

STYLE_GUIDE.md

ブランドデザイン仕様

---

REVIEW_RULE.md

レビュー基準（review_request.mdの形式を含む）

---

AGENT_DESIGN.md

AI役割・ワークフロー

---

BRAND_REFERENCE.md

ブランド見本・再現基準

---

## workspace/

content.md

Claude投稿出力の保存場所

image_request.md

ChatGPTへ渡す画像制作指示書（GitHubを見なくても完結する内容）

canva_text.md

Canvaへそのままコピペするテキスト集

review_request.md

Claude（レビュー）へ渡すレビュー依頼書

history.md

投稿履歴

review.md

レビュー結果の保存場所

---

# 基本ワークフロー

① Claude

「GitHub最新版ルールを参照して作成してください。」

↓

content.md／image_request.md／canva_text.md／review_request.md を出力

↓

② ChatGPT

「image_request.md と canva_text.md に従って画像を作成してください。」

↓

画像を制作

↓

③ Claude（レビュー）

「GitHub最新版ルールを参照してレビューしてください。」

↓

review_request.mdをもとにレビュー

↓

④ 人間

Instagram投稿

---

# 品質基準

このブランドは

「毎回違うデザイン」

を作るものではない。

シリーズ全体で

同じブランド

に見えることを最優先とする。

ブランドとは

・キャラクター

・クマ

・背景

・チャート

・色

・余白

・タイトル

・文字サイズ

・レイアウト

・情報設計

すべてを含む。

ブランド変更は禁止。

改善する場合も

ブランド維持を最優先とする。

詳細な変更可否の一覧はBRAND_REFERENCE.mdを参照する。

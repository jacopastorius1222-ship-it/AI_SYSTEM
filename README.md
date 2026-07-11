# README.md

# AI_SYSTEM

Instagram「株初心者向け教材ブランド」を制作・運用するための共通ルール管理リポジトリです。

Ver2.0より、AIへ長いプロンプトを書く運用をやめ、GitHubだけを見ればAIが動く状態を完成形とします。

**Ver3.0より、画像内の文字はChatGPTではなくClaude（auto_layout.py）が合成する方式に変更しました。詳細はCONTENT_RULE.md／IMAGE_RULE.mdを参照してください。**

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

# 運用ルール（Ver3.0・最重要）

人間がAIへ送る指示は、次の3つのみとする。

① Claude（投稿作成）

「GitHub最新版ルールを参照して作成してください。」

② ChatGPT（イラスト制作）

「image_request.md に従って、文字を含まないイラストを作成してください。」

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

⑧ auto_layout.py（文字合成ロジックの現在の実装）

確認後、必ず以下を行う。

・content.md／image_request.md／text_overlay.md／review_request.md の出力

・ChatGPTが生成した文字なしイラストに対して、auto_layout.pyで文字を合成

出力形式の詳細はCONTENT_RULE.mdに従う。

---

## ②の指示を受けたときのChatGPTの動作

ChatGPTはGitHubを参照しない。

受け取るのは

・image_request.md

・人間が添付するBrand_Reference見本画像

のみ。

**ChatGPTは文字を一切描かない。** イラスト・チャート・図形・色面だけを、この範囲だけで完結する状態にする。

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

・content.md／image_request.md／text_overlay.md／review_request.mdの出力

・**auto_layout.pyによる画像への文字合成**

---

## ChatGPT（イラスト制作）

担当

・**文字を含まないイラストの制作**

・イラスト修正

・画像サイズ確認

・ブランド維持

GitHubは参照しない。

image_request.mdのみで作業する。

文章・ブランドは変更しない。

**文字（タイトル・吹き出し・チャートラベル・CTA等）は描かない。**

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

# GitHubルール

GitHubが唯一の正式ルール管理場所
（Single Source of Truth）

Claude（投稿作成）とClaude（レビュー）は作業開始前に必ずGitHub最新版を確認する。

ChatGPT（イラスト制作）はGitHubを参照しない。

---

# ファイル構成

PROJECT_RULE.md

プロジェクト全体ルール

---

CONTENT_RULE.md

Claude投稿制作ルール（content.md／image_request.md／text_overlay.md／review_request.mdの出力形式を含む）

---

IMAGE_RULE.md

画像仕様ルール（Claudeがimage_request.md作成時に参照する。文字ゾーン設計ルールを含む）

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

auto_layout.py

**Claudeが画像に文字を合成するためのPythonスクリプト（Ver3.0で新設）。バッジ・白ボックス・チャート内カラーピル・チェックリストの丸アイコン等を色解析で自動検出し、文字を正確な位置・統一サイズで合成する。**

---

FONTS_SETUP.md

**auto_layout.pyが使うフォントの準備手順（Ver3.0で新設）。**

---

## workspace/

content.md

Claude投稿出力の保存場所

image_request_template.md

ChatGPTへ渡すイラスト制作指示書のテンプレート（文字を含まないイラストを依頼する内容）

text_overlay.md

**Claudeがauto_layout.pyで実際に合成した文字内容・スタイルの記録（Ver3.0でcanva_text.mdを置き換え）**

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

content.md／image_request.md／text_overlay.md／review_request.md を出力

↓

② ChatGPT

「image_request.md に従って、文字を含まないイラストを作成してください。」

↓

文字なしイラストを制作

↓

③ Claude

auto_layout.pyでイラストに文字を合成

↓

④ Claude（レビュー）

「GitHub最新版ルールを参照してレビューしてください。」

↓

review_request.mdをもとにレビュー

↓

⑤ 人間

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

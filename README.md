# AI_SYSTEM

Instagramで株初心者向けコンテンツを効率よく制作するためのAI運用ルールを管理するリポジトリです。

---

# プロジェクト目的

2028年夏までに現在の仕事を卒業する。

Instagramを起点に、株初心者が楽しく学べる環境を作る。

---

# コンテンツ導線

Instagram

↓

無料株特訓アプリ

↓

note

↓

証券口座アフィリエイト

---

# AI構成

## Claude（編集長）

担当

・テーマ選定

・投稿企画

・タイトル作成

・キャプション作成

・ハッシュタグ作成

・画像設計書作成

・リール構成

・セルフレビュー

---

## Codex（画像制作）

担当

・画像生成

・画像サイズ調整

・画像品質維持

・Claudeが作成したタイトル・キャプション・ハッシュタグを変更せず表示

---

## ChatGPT（システム設計・品質管理）

担当

・GitHubルール改善

・画像品質改善

・ブランド品質維持

・AIワークフロー改善

・Instagram運営改善

---

# ワークフロー

① Claude

↓

投稿内容作成

↓

② Codex

↓

画像生成

↓

③ ChatGPT

↓

品質改善・運用改善

↓

④ 人間

↓

Instagramへ投稿

---

# ルール

すべてのAIは作業開始前に

**PROJECT_RULE.md**

を最優先で確認すること。

GitHubを唯一の正式ルール管理場所（Single Source of Truth）とする。

---

# 現在の構成

* PROJECT_RULE.md（全AI共通ルール）
* CONTENT_RULE.md（Claude制作ルール）
* IMAGE_RULE.md（Codex画像制作ルール）
* STYLE_GUIDE.md（ブランド・デザインルール）
* REVIEW_RULE.md（レビュー基準）
* AGENT_DESIGN.md（AI役割分担）
* README.md（本ファイル）

---

# 基本運用

① Claudeへ

「GitHubのルールに従ってInstagram投稿を1日分作成してください」

↓

② Claudeの内容をCodexへ渡す

↓

③ Codexが画像を生成する

↓

④ 人間が内容を確認する

↓

⑤ Instagramへ投稿

---

# 運用方針

・PROJECT_RULE.md を最優先とする

・ブランドデザインは STYLE_GUIDE.md を最優先とする

・Claudeは文章を担当する

・Codexは画像を担当する

・ChatGPTはシステム改善・品質改善を担当する

・ルールは実運用で改善点が見つかった場合のみ更新する

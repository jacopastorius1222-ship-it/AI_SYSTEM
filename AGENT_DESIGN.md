# AIエージェント設計図

## 目的

人間の作業をできるだけ減らし、AI同士でInstagram投稿の作成・確認・修正を行う。

## 使用する場所

GitHubリポジトリ：AI_SYSTEM

## AIの役割

### ChatGPT

投稿作成担当。

MASTER_RULE.md と INSTAGRAM_RULE.md を読んで、Instagram投稿を作成する。

### Claude

品質確認担当。

REVIEW_CHECKLIST.md を読んで、改善点だけを指摘する。

### ChatGPT

Claudeのレビューをもとに修正版を作成する。

## 人間の役割

最初にテーマを入力する。

最後に完成版を確認する。

## 理想の流れ

1. 人間が投稿テーマを入力
2. ChatGPTがGitHubのルールを読む
3. ChatGPTが投稿を作る
4. Claudeがレビューする
5. ChatGPTが修正する
6. 完成版を保存する
7. 人間が最終確認する

## 最終目標

人間はテーマ入力と最終確認だけ行う。

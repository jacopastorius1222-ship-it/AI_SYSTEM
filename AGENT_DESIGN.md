# AIエージェント設計図

## 最優先ルール

PROJECT_RULE.md を最優先ルールとする。

MASTER_RULE.md、INSTAGRAM_RULE.md、REVIEW_CHECKLIST.md は参考元だが、実行時は PROJECT_RULE.md を優先する。

---

## 役割

### Codex

制作担当。

PROJECT_RULE.md を確認して、Instagram投稿・キャプション・ハッシュタグ・画像・リールを作成する。

### Claude

Instagram編集長。

Codexの作成物を PROJECT_RULE.md に従ってレビューする。

良い点は不要。

改善点のみ3個以上出す。

### ユーザー

最終判断担当。

Codexの作成物とClaudeのレビューを確認し、採用する修正だけをCodexへ戻す。

---

## 基本フロー

1. Codexが PROJECT_RULE.md を確認する
2. Codexが1日分のInstagram投稿を作成する
3. ClaudeがPROJECT_RULE.mdに従ってレビューする
4. ユーザーが採用する修正を選ぶ
5. Codexが修正版を作成する
6. ユーザーが最終確認する

---

## 注意点

初心者あるある投稿は6コマ漫画1枚完結。

初心者あるある投稿でイラスト案②③を要求しない。

リール1枚目には答えを入れない。

改善案は3個以上に統一する。

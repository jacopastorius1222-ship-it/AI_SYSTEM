# FONTS_SETUP.md

# auto_layout.py が使うフォントの準備手順

`auto_layout.py`は以下のフォントファイルを使用する。

・`/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc`（システム標準搭載、変換不要）
・`MPlusRounded-Bold.ttf`（装飾用に残しているが現在は未使用。M PLUS Rounded 1c, weight 800）
・`MPlusRounded-Medium.ttf`（同上、weight 500）
・`KosugiMaru.ttf`（同上、Kosugi Maru）

**Claudeの作業環境（サンドボックス）はセッションごとにリセットされるため、
`MPlusRounded-*.ttf` と `KosugiMaru.ttf` は毎回このコマンドで作り直す必要がある。**
（Google FontsはWOFF/WOFF2形式でしか配布されておらず、Pillowで直接読めないため、
npmでパッケージを取得し、fonttoolsでTTFに変換している。）

```bash
pip install fonttools --break-system-packages -q

npm pack @fontsource/kosugi-maru
npm pack @fontsource/m-plus-rounded-1c
tar xzf fontsource-kosugi-maru-*.tgz
tar xzf fontsource-m-plus-rounded-1c-*.tgz

python3 << 'EOF'
from fontTools.ttLib import TTFont

pairs = [
    ('package/files/kosugi-maru-japanese-400-normal.woff', 'KosugiMaru.ttf'),
]
for src, dst in pairs:
    f = TTFont(src)
    f.flavor = None
    f.save(dst)

# m-plus-rounded-1c は kosugi-maru とは別のpackageディレクトリに展開されるため
# 2回目のtar展開後に以下を実行
pairs2 = [
    ('package/files/m-plus-rounded-1c-japanese-800-normal.woff', 'MPlusRounded-Bold.ttf'),
    ('package/files/m-plus-rounded-1c-japanese-500-normal.woff', 'MPlusRounded-Medium.ttf'),
]
for src, dst in pairs2:
    f = TTFont(src)
    f.flavor = None
    f.save(dst)
EOF
```

生成された3つの`.ttf`ファイルを、`auto_layout.py`と同じディレクトリ（現状は`/home/claude/workspace/`）に置く。
`auto_layout.py`冒頭の`FONT_BOLD` / `FONT_REG` / `FONT_MARU`のパスを、実際に配置した場所に合わせて調整すること。

現状の主力スタイル（Ver3.0・qa_line_position_01.pngを参考にした太字ゴシック+白フチ）では
`FONT_BLACK`（システム標準のNoto Sans CJK Black）のみを使用しており、上記の変換は必須ではない。
丸ゴシック調のデザインに戻す場合にのみ必要になる。

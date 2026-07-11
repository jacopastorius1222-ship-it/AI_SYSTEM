"""
auto_layout.py (v2)
ブランドテンプレート内の「バッジ」「アイコン」「白ボックス」「クリーム色バー」
「チャート内カラーピル」を色解析で自動検出し、文字を正確な中心・統一サイズで
自動フィット描画するモジュール。

v2での修正点:
- テキスト配置がフォントの内部余白(ascent/descent)のせいで中心からズレていたバグを修正
  → 実際のインク(文字の黒い部分)のbboxを基準に配置するよう変更
- フォントをNoto Sans(角ゴシック)から丸ゴシック(M PLUS Rounded 1c / Kosugi Maru)へ変更
- 複数行アイテム(①②③など)のフォントサイズを行ごとにバラけさせず、統一サイズに
- チャート内の色つきピル(緑・赤・ピンク)を自動検出してラベルを描画する機能を追加
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

# 丸ゴシック体(Google Fonts: M PLUS Rounded 1c / Kosugi Maru) ※装飾用に残す
FONT_BOLD = '/home/claude/workspace/MPlusRounded-Bold.ttf'    # weight 800
FONT_REG  = '/home/claude/workspace/MPlusRounded-Medium.ttf'  # weight 500
FONT_MARU = '/home/claude/workspace/KosugiMaru.ttf'           # 手書き風の丸文字
# ブランド参考画像(qa_line_position_01.png)に合わせた、太字ゴシック+白フチスタイル
FONT_BLACK = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'

DARK_GREEN  = (2, 68, 21)
CREAM       = (253, 242, 216)
WHITE       = (250, 250, 248)
MED_GREEN   = (43, 140, 57)
PINK        = (253, 172, 161)
RED         = (230, 60, 35)


def _color_mask(arr, color, tol):
    return (np.abs(arr.astype(int) - np.array(color)).sum(axis=2) < tol)


def _largest_component_bbox(mask, min_area=400):
    labeled, n = ndimage.label(mask)
    if n == 0:
        return None
    sizes = ndimage.sum(mask, labeled, range(1, n + 1))
    best = np.argmax(sizes) + 1
    if sizes[best - 1] < min_area:
        return None
    ys, xs = np.where(labeled == best)
    return (xs.min(), ys.min(), xs.max(), ys.max())


def find_badge_and_icon(im, region, tol=55, icon_margin=4):
    x0, y0, x1, y1 = region
    arr = np.array(im.convert('RGB'))[y0:y1, x0:x1]
    bar_mask = _color_mask(arr, DARK_GREEN, tol)
    bar_bbox = _largest_component_bbox(bar_mask)
    if bar_bbox is None:
        return None, None
    bx0, by0, bx1, by1 = bar_bbox
    sub = arr[by0:by1, bx0:bx1]
    sub_bar_mask = _color_mask(sub, DARK_GREEN, tol)
    not_bar = ~sub_bar_mask
    h, w = not_bar.shape
    inner_mask = np.zeros_like(not_bar)
    inner_mask[icon_margin:h - icon_margin, icon_margin:w - icon_margin] = \
        not_bar[icon_margin:h - icon_margin, icon_margin:w - icon_margin]
    icon_bbox_rel = _largest_component_bbox(inner_mask, min_area=150)
    icon_bbox = None
    if icon_bbox_rel is not None:
        ix0, iy0, ix1, iy1 = icon_bbox_rel
        icon_bbox = (ix0 + bx0 + x0, iy0 + by0 + y0, ix1 + bx0 + x0, iy1 + by0 + y0)
    bar_bbox_abs = (bx0 + x0, by0 + y0, bx1 + x0, by1 + y0)
    return bar_bbox_abs, icon_bbox


def find_color_box(im, region, color, tol=30, min_area=800):
    x0, y0, x1, y1 = region
    arr = np.array(im.convert('RGB'))[y0:y1, x0:x1]
    mask = _color_mask(arr, color, tol)
    bbox = _largest_component_bbox(mask, min_area)
    if bbox is None:
        return None
    bx0, by0, bx1, by1 = bbox
    return (bx0 + x0, by0 + y0, bx1 + x0, by1 + y0)


def find_row_text_zone(im, row_region, tol=55, min_area=80):
    x0, y0, x1, y1 = row_region
    arr = np.array(im.convert('RGB'))[y0:y1, x0:x1]
    bg_dist = np.abs(arr.astype(int) - np.array(WHITE)).sum(axis=2)
    not_bg = bg_dist > 60
    labeled, n = ndimage.label(not_bg)
    if n == 0:
        return (x0, y0, x1, y1)
    boxes = []
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        if len(xs) < min_area:
            continue
        boxes.append((xs.min(), xs.max()))
    if not boxes:
        return (x0, y0, x1, y1)
    boxes.sort()
    left_edge, right_edge = x0, x1
    w = x1 - x0
    left_candidates = [b for b in boxes if b[0] < w * 0.3]
    if left_candidates:
        left_edge = x0 + max(b[1] for b in left_candidates) + 10
    right_candidates = [b for b in boxes if b[1] > w * 0.7]
    if right_candidates:
        right_edge = x0 + min(b[0] for b in right_candidates) - 10
    return (left_edge, y0, right_edge, y1)


def _ink_bbox(draw, text, font):
    lines = text.split('\n')
    boxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    widths = [b[2] - b[0] for b in boxes]
    heights = [b[3] - b[1] for b in boxes]
    return lines, boxes, widths, heights


def fit_font(draw, text, font_path, max_width, max_height, max_size=80, min_size=12):
    lo, hi = min_size, max_size
    best = min_size
    while lo <= hi:
        mid = (lo + hi) // 2
        font = ImageFont.truetype(font_path, mid)
        _, _, widths, heights = _ink_bbox(draw, text, font)
        ls = mid * 0.35
        total_h = sum(heights) + ls * (len(text.split(chr(10))) - 1)
        if max(widths) <= max_width and total_h <= max_height:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def draw_fitted(draw, box, text, font_path, fill, align='center', line_spacing_ratio=0.35,
                 max_size=80, fixed_size=None, stroke_width=0, stroke_fill=None):
    x0, y0, x1, y1 = box
    if stroke_width and not fixed_size:
        size = fit_font(draw, text, font_path, x1 - x0 - stroke_width*2, y1 - y0 - stroke_width*2, max_size=max_size)
    else:
        size = fixed_size if fixed_size else fit_font(draw, text, font_path, x1 - x0, y1 - y0, max_size=max_size)
    font = ImageFont.truetype(font_path, size)
    lines = text.split('\n')
    boxes = [draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width) for line in lines]
    widths = [b[2] - b[0] for b in boxes]
    heights = [b[3] - b[1] for b in boxes]
    ls = size * line_spacing_ratio
    total_h = sum(heights) + ls * (len(lines) - 1)
    cy = y0 + ((y1 - y0) - total_h) / 2
    for line, b, w, h in zip(lines, boxes, widths, heights):
        if align == 'center':
            cx = x0 + ((x1 - x0) - w) / 2
        elif align == 'left':
            cx = x0
        else:
            cx = x1 - w
        draw.text((cx - b[0], cy - b[1]), line, font=font, fill=fill,
                   stroke_width=stroke_width, stroke_fill=stroke_fill)
        cy += h + ls
    return size


def fit_multicolor(draw, lines_segments, font_path, max_width, max_height, stroke_width=0,
                    max_size=100, min_size=12, line_spacing_ratio=0.3):
    """
    lines_segments: [[(text,color), (text,color), ...], [...], ...]  # 行ごとにセグメントのリスト
    各行のセグメント幅合計がmax_widthに収まる最大フォントサイズを二分探索で求める
    """
    lo, hi = min_size, max_size
    best = min_size
    while lo <= hi:
        mid = (lo + hi) // 2
        font = ImageFont.truetype(font_path, mid)
        ok = True
        total_h = 0
        for segs in lines_segments:
            line_w = 0
            line_h = 0
            for txt, _ in segs:
                b = draw.textbbox((0, 0), txt, font=font, stroke_width=stroke_width)
                line_w += (b[2] - b[0])
                line_h = max(line_h, b[3] - b[1])
            if line_w > max_width:
                ok = False
            total_h += line_h
        total_h += mid * line_spacing_ratio * (len(lines_segments) - 1)
        if ok and total_h <= max_height:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def draw_multicolor_fitted(draw, box, lines_segments, font_path, align='center',
                            max_size=100, stroke_width=0, stroke_fill=(255, 255, 255),
                            line_spacing_ratio=0.3, fixed_size=None):
    """
    行ごとに複数色のセグメントを並べて描画する(例: [[("どっちが","black")],[("強いの？","orange")]])
    """
    x0, y0, x1, y1 = box
    size = fixed_size if fixed_size else fit_multicolor(
        draw, lines_segments, font_path, x1 - x0, y1 - y0, stroke_width=stroke_width,
        max_size=max_size, line_spacing_ratio=line_spacing_ratio)
    font = ImageFont.truetype(font_path, size)

    # 各行の幅・高さを計算
    line_infos = []
    for segs in lines_segments:
        seg_boxes = [draw.textbbox((0, 0), t, font=font, stroke_width=stroke_width) for t, _ in segs]
        widths = [b[2] - b[0] for b in seg_boxes]
        tops = [b[1] for b in seg_boxes]
        bottoms = [b[3] for b in seg_boxes]
        lefts = [b[0] for b in seg_boxes]
        line_infos.append((widths, tops, bottoms, lefts, max(bottoms) - min(tops) if seg_boxes else 0, min(tops) if seg_boxes else 0))

    ls = size * line_spacing_ratio
    total_h = sum(li[4] for li in line_infos) + ls * (len(lines_segments) - 1)
    cy = y0 + ((y1 - y0) - total_h) / 2

    for segs, (widths, tops, bottoms, lefts, h, top_min) in zip(lines_segments, line_infos):
        line_w = sum(widths)
        if align == 'center':
            cx = x0 + ((x1 - x0) - line_w) / 2
        elif align == 'left':
            cx = x0
        else:
            cx = x1 - line_w
        for (txt, color), w, left in zip(segs, widths, lefts):
            draw.text((cx - left, cy - top_min), txt, font=font, fill=color,
                       stroke_width=stroke_width, stroke_fill=stroke_fill)
            cx += w
        cy += h + ls
    return size


def uniform_fit_size(draw, texts, font_path, max_width, max_height, max_size=80):
    return min(fit_font(draw, t, font_path, max_width, max_height, max_size=max_size) for t in texts)


def soften_box(im, box, tint=(253, 240, 214), alpha=0.55):
    x0, y0, x1, y1 = [int(v) for v in box]
    overlay = Image.new('RGB', (x1 - x0, y1 - y0), tint)
    region = im.crop((x0, y0, x1, y1))
    blended = Image.blend(region, overlay, alpha)
    im.paste(blended, (x0, y0))

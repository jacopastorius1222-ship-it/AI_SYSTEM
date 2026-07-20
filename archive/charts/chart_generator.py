"""
chart_generator.py

ChatGPTに渡す「正解チャート」の参考画像を生成するモジュール。

背景・経緯：
ChatGPTに「移動平均線が交差するチャート」を文章だけで指示すると、
交差後に一方の線が消える／もう一方の線の色に変わる、という不具合が
繰り返し発生することが確認された（IMAGE_RULE.md 6-2章参照）。

対策として、Pythonでチャートの「正解画像」を先に生成し、
それをブランド見本画像と一緒にChatGPTへ添付し、
「チャート部分はこの添付画像を完全再現してください」と依頼する運用にした。
（chart_generator.py自体がそのままイラストに合成されるわけではなく、
 ChatGPTが参考にして描き直すための「お手本」を作る役割）

使い方：
    python3 chart_generator.py --pattern dead_cross --out chart_deadcross_reference.png
    python3 chart_generator.py --pattern golden_cross --out chart_goldencross_reference.png

または関数として：
    from chart_generator import generate_chart
    generate_chart(pattern="dead_cross", out_path="chart_deadcross_reference.png")
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


def _glow(ax, cx, cy, base_size, color):
    for size, alpha in [(base_size*2.6, 0.12), (base_size*1.8, 0.22),
                         (base_size*1.1, 0.35), (base_size*0.6, 0.55)]:
        ax.scatter([cx], [cy], s=size, color=color, alpha=alpha, zorder=6, linewidths=0)


def _sparkle(ax, cx, cy, scale, color):
    angles = [70, 90, 110]
    for a in angles:
        rad = np.radians(a)
        x0, y0 = cx + 0.35*scale*np.cos(rad), cy + 0.5*scale*np.sin(rad)
        x1, y1 = cx + 1.1*scale*np.cos(rad), cy + 1.6*scale*np.sin(rad)
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=3.2, solid_capstyle='round', zorder=7)


def _generate_perfect_order_chart(rng, n, x, out_path, rounded_border):
    """短期・中期・長期の3本の移動平均線がきれいに並ぶ（パーフェクトオーダー）形のチャートを生成する"""
    long_ma = 50 + 14 * (x / n) ** 1.1
    mid_ma = 52 + 20 * (x / n) ** 1.15
    short_ma = 54 + 27 * (x / n) ** 1.2

    close = short_ma + rng.normal(0, 1.4, n)
    close[0] = short_ma[0]
    open_ = np.roll(close, 1)
    open_[0] = close[0] - 1
    high = np.maximum(open_, close) + np.abs(rng.normal(1.1, 0.6, n))
    low = np.minimum(open_, close) - np.abs(rng.normal(1.1, 0.6, n))
    up = close >= open_

    volume = rng.uniform(4, 8, n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7),
                                    gridspec_kw={'height_ratios': [3, 1]}, facecolor='white')
    w = 0.32
    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax1.plot([i, i], [low[i], high[i]], color=color, linewidth=1.4, solid_capstyle='round', zorder=3)
        body_h = max(abs(close[i] - open_[i]), 0.5)
        ax1.add_patch(plt.Rectangle((i - w/2, min(open_[i], close[i])), w, body_h,
                                     facecolor=color, edgecolor=color, linewidth=0.4, zorder=3))

    for line_y, col in [(long_ma, '#1f7a3d'), (mid_ma, '#2f6fb0'), (short_ma, '#ff8c1a')]:
        ax1.plot(x, line_y, color='white', linewidth=6.0, solid_capstyle='round', zorder=4)
        ax1.plot(x, line_y, color=col, linewidth=3.4, solid_capstyle='round', zorder=5)
    ax1.axis('off')

    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax2.bar(i, volume[i], color=color, width=0.65, edgecolor=color, linewidth=0.3)
    ax2.axis('off')

    plt.subplots_adjust(hspace=0.05, left=0.02, right=0.98, top=0.98, bottom=0.02)
    tmp_path = out_path + ".tmp.png"
    fig.savefig(tmp_path, dpi=170, facecolor='white')
    plt.close(fig)
    _finalize(tmp_path, out_path, rounded_border)
    return out_path, None


def _generate_slope_chart(rng, n, x, out_path, rounded_border, steep=True):
    """移動平均線の傾き(急/緩やか)で勢いの違いを見せるチャートを生成する"""
    if steep:
        ma = 50 + 40 * (x / n) ** 1.15
    else:
        ma = 50 + 8 * (x / n) + 2 * np.sin(x / 9)

    close = ma + rng.normal(0, 1.6, n)
    close[0] = ma[0]
    open_ = np.roll(close, 1)
    open_[0] = close[0] - 1
    high = np.maximum(open_, close) + np.abs(rng.normal(1.3, 0.7, n))
    low = np.minimum(open_, close) - np.abs(rng.normal(1.3, 0.7, n))
    up = close >= open_

    volume = rng.uniform(3, 6, n) if not steep else rng.uniform(4, 9, n)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7),
                                    gridspec_kw={'height_ratios': [3, 1]}, facecolor='white')
    w = 0.32
    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax1.plot([i, i], [low[i], high[i]], color=color, linewidth=1.6, solid_capstyle='round', zorder=3)
        body_h = max(abs(close[i] - open_[i]), 0.5)
        ax1.add_patch(plt.Rectangle((i - w/2, min(open_[i], close[i])), w, body_h,
                                     facecolor=color, edgecolor=color, linewidth=0.5, zorder=3))

    ax1.plot(x, ma, color='white', linewidth=6.5, solid_capstyle='round', zorder=4)
    ax1.plot(x, ma, color='#1f7a3d', linewidth=3.6, solid_capstyle='round', zorder=5)
    ax1.axis('off')

    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax2.bar(i, volume[i], color=color, width=0.65, edgecolor=color, linewidth=0.3)
    ax2.axis('off')

    plt.subplots_adjust(hspace=0.05, left=0.02, right=0.98, top=0.98, bottom=0.02)
    tmp_path = out_path + ".tmp.png"
    fig.savefig(tmp_path, dpi=170, facecolor='white')
    plt.close(fig)
    _finalize(tmp_path, out_path, rounded_border)
    return out_path, None


def _generate_support_chart(rng, n, x, out_path, rounded_border):
    """価格が移動平均線に何度か近づいて跳ね返される（支持線として機能する）形のチャートを生成する"""
    # 移動平均線：ゆるやかな右肩上がり
    ma = 55 + 10 * (x / n) + 1.0 * np.sin(x / 14)

    # タッチポイント（跳ね返る位置）を3か所指定
    touch_idx = [int(n * 0.28), int(n * 0.55), int(n * 0.82)]

    close = np.zeros(n)
    close[0] = ma[0] + 8
    for i in range(1, n):
        # 直近のタッチポイントに向かって引き寄せられ、タッチ後は反発する
        nearest = min(touch_idx, key=lambda t: abs(t - i))
        dist = i - nearest
        if -4 <= dist <= 0:
            target = ma[i] + 6 * (1 - (dist + 4) / 4)
        elif 0 < dist <= 6:
            target = ma[i] + 2 + dist * 1.3
        else:
            target = ma[i] + 6 + rng.uniform(-1, 1)
        close[i] = target + rng.normal(0, 1.0)

    open_ = np.roll(close, 1)
    open_[0] = close[0] - 1
    high = np.maximum(open_, close) + np.abs(rng.normal(1.2, 0.7, n))
    low = np.minimum(open_, close) - np.abs(rng.normal(1.2, 0.7, n))
    # タッチ時は線に触れるところまでヒゲを伸ばす
    for t in touch_idx:
        low[t] = min(low[t], ma[t] - 0.3)
    up = close >= open_

    volume = rng.uniform(3, 6, n)
    for t in touch_idx:
        for d in range(-1, 2):
            if 0 <= t + d < n:
                volume[t + d] = rng.uniform(7, 10)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7),
                                    gridspec_kw={'height_ratios': [3, 1]}, facecolor='white')
    w = 0.32
    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax1.plot([i, i], [low[i], high[i]], color=color, linewidth=1.6, solid_capstyle='round', zorder=3)
        body_h = max(abs(close[i] - open_[i]), 0.5)
        ax1.add_patch(plt.Rectangle((i - w/2, min(open_[i], close[i])), w, body_h,
                                     facecolor=color, edgecolor=color, linewidth=0.5, zorder=3))

    ax1.plot(x, ma, color='white', linewidth=6.5, solid_capstyle='round', zorder=4)
    ax1.plot(x, ma, color='#1f7a3d', linewidth=3.6, solid_capstyle='round', zorder=5)

    for t in touch_idx:
        _glow(ax1, t, ma[t], 550, '#ffd23f')
        _sparkle(ax1, t, ma[t] + 2.5, 0.8, '#ffb200')

    ax1.axis('off')

    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax2.bar(i, volume[i], color=color, width=0.65, edgecolor=color, linewidth=0.3)
    ax2.axis('off')

    plt.subplots_adjust(hspace=0.05, left=0.02, right=0.98, top=0.98, bottom=0.02)
    tmp_path = out_path + ".tmp.png"
    fig.savefig(tmp_path, dpi=170, facecolor='white')
    plt.close(fig)
    _finalize(tmp_path, out_path, rounded_border)
    return out_path, touch_idx


def _generate_kairi_chart(rng, n, x, out_path, rounded_border):
    """価格が移動平均線から大きく上に乖離していく形のチャートを生成する"""
    # 移動平均線：ゆるやかな横ばい〜わずかな上昇
    ma = 55 + 4 * (x / n) + 1.5 * np.sin(x / 10)

    # 価格：前半は線に沿う。後半、線から大きく上に離れていく
    gap_base = np.clip((x - n * 0.55) / (n * 0.45), 0, None)
    gap = np.where(x < n * 0.55, 0, gap_base ** 1.6 * 22)
    close = ma + gap + rng.normal(0, 1.6, n)
    close[0] = ma[0]
    open_ = np.roll(close, 1)
    open_[0] = close[0] - 1
    high = np.maximum(open_, close) + np.abs(rng.normal(1.4, 0.8, n))
    low = np.minimum(open_, close) - np.abs(rng.normal(1.4, 0.8, n))
    up = close >= open_

    # 出来高：乖離が広がる終盤で増加
    volume = rng.uniform(3, 6, n)
    for i in range(int(n * 0.75), n):
        volume[i] = rng.uniform(6, 10)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7),
                                    gridspec_kw={'height_ratios': [3, 1]}, facecolor='white')
    w = 0.32
    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax1.plot([i, i], [low[i], high[i]], color=color, linewidth=1.6, solid_capstyle='round', zorder=3)
        body_h = max(abs(close[i] - open_[i]), 0.5)
        ax1.add_patch(plt.Rectangle((i - w/2, min(open_[i], close[i])), w, body_h,
                                     facecolor=color, edgecolor=color, linewidth=0.5, zorder=3))

    ax1.plot(x, ma, color='white', linewidth=6.5, solid_capstyle='round', zorder=4)
    ax1.plot(x, ma, color='#1f7a3d', linewidth=3.6, solid_capstyle='round', zorder=5)

    # 乖離幅を示す縦の両矢印（終盤の1本で）
    gi = n - 3
    y0, y1 = ma[gi], close[gi]
    ax1.annotate('', xy=(gi, y1), xytext=(gi, y0),
                 arrowprops=dict(arrowstyle='<->', color='#ff8c1a', linewidth=3))
    _glow(ax1, gi, (y0 + y1) / 2, 700, '#ffd23f')
    _sparkle(ax1, gi - 2, (y0 + y1) / 2, 0.9, '#ffb200')

    ax1.axis('off')

    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax2.bar(i, volume[i], color=color, width=0.65, edgecolor=color, linewidth=0.3)
    ax2.axis('off')

    plt.subplots_adjust(hspace=0.05, left=0.02, right=0.98, top=0.98, bottom=0.02)
    tmp_path = out_path + ".tmp.png"
    fig.savefig(tmp_path, dpi=170, facecolor='white')
    plt.close(fig)
    _finalize(tmp_path, out_path, rounded_border)
    return out_path, (gi, (y0 + y1) / 2)


def _finalize(tmp_path, out_path, rounded_border):
    if rounded_border:
        im = Image.open(tmp_path).convert('RGB')
        pad = 24
        canvas = Image.new('RGB', (im.width + pad*2, im.height + pad*2), 'white')
        canvas.paste(im, (pad, pad))
        mask = Image.new('L', canvas.size, 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([4, 4, canvas.size[0]-4, canvas.size[1]-4], radius=32, fill=255)
        rounded = Image.new('RGB', canvas.size, (255, 255, 255))
        rounded.paste(canvas, (0, 0), mask)
        d = ImageDraw.Draw(rounded)
        d.rounded_rectangle([4, 4, canvas.size[0]-4, canvas.size[1]-4], radius=32,
                             outline=(20, 90, 40), width=7)
        rounded.save(out_path)
    else:
        Image.open(tmp_path).save(out_path)
    import os
    os.remove(tmp_path)


def generate_chart(pattern="dead_cross", n=40, seed=11, out_path="chart_reference.png",
                    rounded_border=True):
    """
    pattern: "dead_cross"（25日線が上から下へ）／"golden_cross"（25日線が下から上へ）／
             "kairi"（価格が移動平均線から大きく上に乖離する形）
    n: ローソク足の本数（＝出来高バーの本数。常に一致する）
    seed: 乱数シード（同じ値なら毎回同じチャートになる）
    out_path: 出力PNGパス
    """
    rng = np.random.default_rng(seed)
    x = np.arange(n)

    if pattern == "kairi":
        return _generate_kairi_chart(rng, n, x, out_path, rounded_border)
    if pattern == "support_line":
        return _generate_support_chart(rng, n, x, out_path, rounded_border)
    if pattern == "slope_steep":
        return _generate_slope_chart(rng, n, x, out_path, rounded_border, steep=True)
    if pattern == "slope_flat":
        return _generate_slope_chart(rng, n, x, out_path, rounded_border, steep=False)
    if pattern == "perfect_order":
        return _generate_perfect_order_chart(rng, n, x, out_path, rounded_border)

    green_base = 72 - 6 * (x / n) - 2 * np.sin(x / 12)
    orange_base = 90 - 55 * (x / n) ** 1.3
    if pattern == "dead_cross":
        green, orange = green_base, orange_base
    elif pattern == "golden_cross":
        # dead_crossの形をx軸方向に反転して使うことで、交差位置を中央付近に保つ
        rev = (n - 1 - x)
        green = 72 - 6 * (rev / n) - 2 * np.sin(rev / 12)
        orange = 90 - 55 * (rev / n) ** 1.3
    else:
        raise ValueError("pattern must be 'dead_cross' or 'golden_cross'")

    diff = orange - green
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    cross_i = sign_changes[0] if len(sign_changes) else n // 2
    cx = cross_i + (0 - diff[cross_i]) / (diff[cross_i + 1] - diff[cross_i])
    cy = np.interp(cx, x, green)

    noise = rng.normal(0, 3.6, n)
    wave = 2.8 * np.sin(x / 2.3 + 1.0)
    close = orange + noise + wave
    close[0] = orange[0]
    open_ = np.roll(close, 1)
    open_[0] = close[0] - 1
    high = np.maximum(open_, close) + np.abs(rng.normal(1.8, 1.0, n))
    low = np.minimum(open_, close) - np.abs(rng.normal(1.8, 1.0, n))
    up = close >= open_

    volume = rng.uniform(3, 7, n)
    spike_idx = int(round(cx))
    for d in range(-1, 2):
        if 0 <= spike_idx + d < n:
            volume[spike_idx + d] = 11 - abs(d) * 3

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7),
                                    gridspec_kw={'height_ratios': [3, 1]}, facecolor='white')

    w = 0.32
    for i in range(n):
        color = '#2e8b3d' if up[i] else '#c0392b'
        ax1.plot([i, i], [low[i], high[i]], color=color, linewidth=1.6,
                  solid_capstyle='round', zorder=3)
        body_h = max(abs(close[i] - open_[i]), 0.5)
        ax1.add_patch(plt.Rectangle((i - w/2, min(open_[i], close[i])), w, body_h,
                                     facecolor=color, edgecolor=color, linewidth=0.5, zorder=3))

    for line_x, line_y, col in [(x, orange, '#ff8c1a'), (x, green, '#1f7a3d')]:
        ax1.plot(line_x, line_y, color='white', linewidth=6.5, solid_capstyle='round', zorder=4)
        ax1.plot(line_x, line_y, color=col, linewidth=3.6, solid_capstyle='round', zorder=5)

    _glow(ax1, cx, cy, 900, '#ffd23f')
    _sparkle(ax1, cx, cy + 2.2, 1.0, '#ffb200')
    ax1.axis('off')

    for i in range(n):
        color = '#c0392b' if i in range(spike_idx - 1, spike_idx + 2) else \
            ('#2e8b3d' if up[i] else '#c0392b')
        ax2.bar(i, volume[i], color=color, width=0.65, edgecolor=color, linewidth=0.3)
    _sparkle(ax2, spike_idx, volume[spike_idx] + 1.0, 0.7, '#c0392b')
    ax2.axis('off')

    plt.subplots_adjust(hspace=0.05, left=0.02, right=0.98, top=0.98, bottom=0.02)

    tmp_path = out_path + ".tmp.png"
    fig.savefig(tmp_path, dpi=170, facecolor='white')
    plt.close(fig)

    if rounded_border:
        im = Image.open(tmp_path).convert('RGB')
        pad = 24
        canvas = Image.new('RGB', (im.width + pad*2, im.height + pad*2), 'white')
        canvas.paste(im, (pad, pad))
        mask = Image.new('L', canvas.size, 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([4, 4, canvas.size[0]-4, canvas.size[1]-4], radius=32, fill=255)
        rounded = Image.new('RGB', canvas.size, (255, 255, 255))
        rounded.paste(canvas, (0, 0), mask)
        d = ImageDraw.Draw(rounded)
        d.rounded_rectangle([4, 4, canvas.size[0]-4, canvas.size[1]-4], radius=32,
                             outline=(20, 90, 40), width=7)
        rounded.save(out_path)
    else:
        Image.open(tmp_path).save(out_path)

    import os
    os.remove(tmp_path)
    return out_path, (cx, cy)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", choices=["dead_cross", "golden_cross", "kairi", "support_line", "slope_steep", "slope_flat", "perfect_order"], default="dead_cross")
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--out", default="chart_reference.png")
    args = parser.parse_args()
    path, cross = generate_chart(args.pattern, args.n, args.seed, args.out)
    if cross:
        print(f"saved: {path}  crossing at x={cross[0]:.1f}")
    else:
        print(f"saved: {path}")

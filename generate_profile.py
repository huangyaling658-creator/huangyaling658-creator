#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 GitHub Profile Generator
=============================
一键生成精美的 GitHub 个人主页所有资产：
  - 顶部 Banner（渐变 + 人物 + 花体字）
  - 作品卡片（粉绿主题宝藏卡）
  - 技能图谱 + 成长路线（背景人物 + 进度条）
  - README.md（完整 Markdown）

使用方法:
  1. 修改 profile_config.yaml 中的文字和图片路径
  2. 运行: python3 generate_profile.py
  3. 推送: git add -A && git commit -m "update profile" && git push
"""

import yaml
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# ============================================================
#  工具函数
# ============================================================

def load_config(path="profile_config.yaml"):
    """加载 YAML 配置"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_font(names, size):
    """在系统字体目录中查找可用字体"""
    search_dirs = [
        "/System/Library/Fonts/",
        "/System/Library/Fonts/Supplemental/",
        "/Library/Fonts/",
        os.path.expanduser("~/Library/Fonts/"),
        # Linux 常见路径
        "/usr/share/fonts/truetype/",
        "/usr/share/fonts/",
        # Windows 常见路径
        "C:/Windows/Fonts/",
    ]
    for name in names:
        for d in search_dirs:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    print(f"  ⚠️  未找到字体 {names}，使用默认字体")
    return ImageFont.load_default()


def is_chinese(text):
    """判断文本是否包含中文"""
    return any('\u4e00' <= c <= '\u9fff' for c in text)


def draw_heart(draw, cx, cy, size, fill):
    """绘制爱心形状"""
    pts = []
    for deg in range(360):
        t = math.radians(deg)
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) -
              2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((int(x / 17 * size + cx), int(y / 17 * size + cy)))
    if len(pts) > 2:
        draw.polygon(pts, fill=fill)


def draw_outlined_text(d, pos, text, font, fill=(255, 255, 255, 255),
                       outline=(0, 0, 0, 200), width=1):
    """绘制带描边的文字"""
    x, y = pos
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx == 0 and dy == 0:
                continue
            d.text((x + dx, y + dy), text, fill=outline, font=font)
    d.text((x, y), text, fill=fill, font=font)


def draw_sparkle(d, cx, cy, size, fill):
    """绘制闪光装饰"""
    d.line([(cx - size, cy), (cx + size, cy)], fill=fill, width=2)
    d.line([(cx, cy - size), (cx, cy + size)], fill=fill, width=2)
    s = max(size * 2 // 3, 1)
    d.line([(cx - s, cy - s), (cx + s, cy + s)], fill=fill, width=1)
    d.line([(cx + s, cy - s), (cx - s, cy + s)], fill=fill, width=1)


def draw_mini_heart(d, cx, cy, size, fill):
    """绘制迷你爱心装饰"""
    draw_heart(d, cx, cy, size, fill)


# ============================================================
#  1. 生成顶部 Banner
# ============================================================

def generate_banner(cfg):
    """生成顶部 Banner 图片"""
    print("🎨 [1/4] 生成顶部 Banner ...")

    banner_cfg = cfg["banner"]
    style = cfg["style"]
    W, H = style["banner_width"], style["banner_height"]

    # --- 渐变背景 ---
    img = Image.new("RGBA", (W, H))
    c1 = tuple(banner_cfg["gradient_start"])
    c2 = tuple(banner_cfg["gradient_end"])
    for y in range(H):
        for x in range(W):
            t = (x / W * 0.6 + y / H * 0.4)
            r = int(c1[0] * (1 - t) + c2[0] * t)
            g = int(c1[1] * (1 - t) + c2[1] * t)
            b = int(c1[2] * (1 - t) + c2[2] * t)
            img.putpixel((x, y), (r, g, b, 255))

    draw = ImageDraw.Draw(img)

    # --- 装饰爱心 ---
    deco_hearts = [
        (180, 55, 7, (180, 140, 170, 60)),
        (140, 180, 5, (200, 160, 190, 50)),
        (820, 40, 6, (190, 150, 180, 55)),
        (880, 260, 5, (180, 140, 170, 45)),
        (950, 80, 4, (170, 130, 160, 40)),
    ]
    for hx, hy, hs, hc in deco_hearts:
        draw_heart(draw, hx, hy, hs, hc)

    # --- 字体 ---
    font_hi = find_font(["Georgia.ttf", "Times New Roman.ttf"], 28)
    font_name = find_font(["Snell Roundhand.ttc", "SnellRoundhand.ttc", "Zapfino.ttf"], 72)
    font_cn = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 18)

    # --- 人物 ---
    char_path = banner_cfg["character_image"]
    if os.path.exists(char_path):
        char_img = Image.open(char_path).convert("RGBA")
        char_h = int(H * 1.0)
        char_w = int(char_img.width * char_h / char_img.height)
        char_img = char_img.resize((char_w, char_h), Image.LANCZOS)
    else:
        print(f"  ⚠️  人物图片不存在: {char_path}，将跳过人物")
        char_img = None
        char_w = 0

    # --- 布局：文字 + 人物居中 ---
    text_block_w = 420
    gap = banner_cfg.get("text_gap", 20)
    total_content_w = text_block_w + gap + char_w
    start_x = (W - total_content_w) // 2
    text_center_x = start_x + text_block_w // 2
    char_x = start_x + text_block_w + gap

    # --- 绘制 "Hi, I'm" ---
    hi_text = banner_cfg["greeting"]
    hi_bb = draw.textbbox((0, 0), hi_text, font=font_hi)
    hi_w = hi_bb[2] - hi_bb[0]
    hi_x = text_center_x - hi_w // 2
    hi_y = 45
    draw.text((hi_x + 1, hi_y + 1), hi_text, fill=(40, 20, 50, 120), font=font_hi)
    draw.text((hi_x, hi_y), hi_text, fill=(230, 210, 225, 255), font=font_hi)

    # --- 爱心 + 名字 + 爱心 ---
    name_text = banner_cfg["name"]
    name_bb = draw.textbbox((0, 0), name_text, font=font_name)
    name_w = name_bb[2] - name_bb[0]

    heart_size = 16
    heart_gap = 12
    total_name_w = heart_size * 2 + heart_gap + name_w + heart_gap + heart_size * 2
    name_start_x = text_center_x - total_name_w // 2

    # 左侧双爱心
    lh_x = name_start_x + heart_size
    lh_y = 135
    draw_heart(draw, lh_x - 8, lh_y, heart_size - 4, (180, 140, 170, 160))
    draw_heart(draw, lh_x + 8, lh_y, heart_size, (190, 150, 180, 180))

    # 名字
    name_x = name_start_x + heart_size * 2 + heart_gap
    name_y = 100
    draw.text((name_x + 2, name_y + 2), name_text, fill=(30, 15, 40, 150), font=font_name)
    draw.text((name_x, name_y), name_text, fill=(245, 230, 240, 255), font=font_name)

    # 右侧爱心
    rh_x = name_x + name_w + heart_gap + heart_size
    rh_y = 135
    draw_heart(draw, rh_x, rh_y, heart_size, (190, 150, 180, 180))

    # --- 副标题 ---
    cn_text = banner_cfg["subtitle"]
    cn_bb = draw.textbbox((0, 0), cn_text, font=font_cn)
    cn_w = cn_bb[2] - cn_bb[0]
    cn_x = text_center_x - cn_w // 2
    cn_y = 200
    draw.text((cn_x + 1, cn_y + 1), cn_text, fill=(30, 15, 40, 100), font=font_cn)
    draw.text((cn_x, cn_y), cn_text, fill=(210, 190, 210, 255), font=font_cn)

    # --- 粘贴人物 ---
    if char_img:
        char_y = (H - char_img.height) // 2
        img.paste(char_img, (char_x, char_y), char_img)

    # --- 保存 ---
    os.makedirs("assets", exist_ok=True)
    img.convert("RGB").save("assets/header-banner.png", quality=95)
    print("  ✅ assets/header-banner.png")


# ============================================================
#  2. 生成作品卡片
# ============================================================

def generate_project_cards(cfg):
    """生成作品卡片图片"""
    print("🃏 [2/4] 生成作品卡片 ...")

    style = cfg["style"]
    CW, CH = style["card_width"], style["card_height"]
    cards = cfg["projects"]["cards"]

    font_name_en = find_font(["Avenir Next.ttc", "Helvetica.ttc", "Arial.ttf"], 24)
    font_name_cn = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 26)
    font_desc = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 14)
    font_tech = find_font(["Avenir Next.ttc", "Helvetica.ttc", "Arial.ttf"], 13)
    font_initial_en = find_font(["Avenir Next.ttc", "Helvetica.ttc", "Arial.ttf"], 22)
    font_initial_cn = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 20)

    WHITE = (255, 255, 255, 255)
    BLACK = (30, 30, 30, 255)
    BLACK_OUTLINE = (0, 0, 0, 200)

    os.makedirs("assets/projects", exist_ok=True)

    for idx, card in enumerate(cards):
        tr, tg, tb = card["color_top"]
        br, bg_c, bb = card["color_bottom"]

        # 圆角遮罩
        mask = Image.new("L", (CW, CH), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, CW - 1, CH - 1), radius=20, fill=255)

        # 渐变背景
        bg = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bg)
        for y in range(CH):
            t = y / CH
            bd.line([(0, y), (CW, y)],
                    fill=(int(tr * (1 - t) + br * t),
                          int(tg * (1 - t) + bg_c * t),
                          int(tb * (1 - t) + bb * t), 245))
        # 顶部高光
        for y in range(CH // 3):
            bd.line([(0, y), (CW, y)],
                    fill=(255, 255, 255, int(50 * (1 - y / (CH // 3)))))

        result = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        result.paste(bg, mask=mask)
        d = ImageDraw.Draw(result)
        d.rounded_rectangle((0, 0, CW - 1, CH - 1), radius=20,
                            outline=(255, 255, 255, 200), width=2)

        # 圆形图标 — 显示项目名首字
        cx_i, cy_i = 42, 48
        ir = 24
        d.ellipse([(cx_i - ir, cy_i - ir), (cx_i + ir, cy_i + ir)],
                  fill=(255, 255, 255, 220))
        initial = card["name"][0].upper() if not is_chinese(card["name"][0]) else card["name"][0]
        ini_font = font_initial_cn if is_chinese(initial) else font_initial_en
        ib = d.textbbox((0, 0), initial, font=ini_font)
        iw, ih = ib[2] - ib[0], ib[3] - ib[1]
        d.text((cx_i - iw // 2, cy_i - ih // 2 - 2), initial,
               fill=(80, 30, 100, 255), font=ini_font)

        # 项目名
        nf = font_name_cn if is_chinese(card["name"]) else font_name_en
        draw_outlined_text(d, (80, 30), card["name"], nf,
                           fill=WHITE, outline=BLACK_OUTLINE, width=1)

        # 描述
        draw_outlined_text(d, (80, 60), card["desc"], font_desc,
                           fill=WHITE, outline=BLACK_OUTLINE, width=1)

        # 技术标签
        tt = card["tech"]
        tb2 = d.textbbox((0, 0), tt, font=font_tech)
        tw, th = tb2[2] - tb2[0], tb2[3] - tb2[1]
        tx, ty = 80, 92
        d.rounded_rectangle((tx, ty, tx + tw + 18, ty + th + 8), radius=8,
                            fill=(255, 255, 255, 180), outline=(200, 200, 200, 150))
        d.text((tx + 9, ty + 3), tt, fill=BLACK, font=font_tech)

        # 装饰
        dc = (255, 255, 255, 120)
        if idx % 3 == 0:
            draw_sparkle(d, CW - 35, 28, 10, dc)
        elif idx % 3 == 1:
            draw_mini_heart(d, CW - 32, 30, 9, (255, 255, 255, 100))
        else:
            d.ellipse([(CW - 30, 22), (CW - 22, 30)], fill=(255, 255, 255, 100))

        # 底部圆点装饰
        for i in range(3):
            dx = 28 + i * 12
            sz = [2, 3, 2][i]
            d.ellipse([(dx, CH - 22), (dx + sz * 2, CH - 22 + sz * 2)],
                      fill=(255, 255, 255, 80 + i * 20))

        out_path = f"assets/projects/card-{idx + 1}.png"
        result.save(out_path, quality=95)
        print(f"  ✅ {out_path} — [{initial}] {card['name']}")


# ============================================================
#  3. 生成技能图谱 + 成长路线
# ============================================================

def generate_skills_timeline(cfg):
    """生成技能图谱 + 成长路线合并图"""
    print("📊 [3/4] 生成技能图谱 + 成长路线 ...")

    skills_cfg = cfg["skills"]
    timeline_cfg = cfg["timeline"]
    style = cfg["style"]
    W, H = style["skills_width"], style["skills_height"]

    PURPLE = (60, 20, 80)
    PURPLE_LIGHT = (100, 45, 120)
    PURPLE_MID = (75, 30, 95)

    # --- 背景 ---
    bg_path = skills_cfg["background_image"]
    opacity = skills_cfg.get("background_opacity", 0.4)
    overlay_color = tuple(skills_cfg.get("overlay_color", [240, 200, 220, 50]))

    if os.path.exists(bg_path):
        bg_img = Image.open(bg_path).convert("RGBA")
        bg_img = bg_img.resize((W, H), Image.LANCZOS)
        alpha = bg_img.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        bg_img.putalpha(alpha)
        base = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        img = Image.alpha_composite(base, bg_img)
    else:
        print(f"  ⚠️  背景图不存在: {bg_path}，使用纯白背景")
        img = Image.new("RGBA", (W, H), (255, 255, 255, 255))

    # 蒙层
    overlay = Image.new("RGBA", (W, H), overlay_color)
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # --- 字体 ---
    font_section = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 30)
    font_skill_name = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 20)
    font_pct = find_font(["Avenir Next.ttc", "Helvetica.ttc", "Arial.ttf"], 18)
    font_skill_desc = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 14)
    font_tl_date = find_font(["Avenir Next.ttc", "Helvetica.ttc", "Arial.ttf"], 18)
    font_tl_title = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 22)
    font_tl_desc = find_font(["PingFang.ttc", "STHeiti Light.ttc", "SimHei.ttf"], 14)

    WHITE_OUTLINE = (255, 255, 255)

    # --- 左侧：技能图谱 ---
    left_x = 50
    top_y = 35
    draw_outlined_text(draw, (left_x, top_y), "🗂 技能图谱", font_section,
                       fill=PURPLE, outline=(*WHITE_OUTLINE, 180), width=2)

    bar_start_y = top_y + 55
    bar_w = 440
    bar_h = 16

    for i, skill in enumerate(skills_cfg["items"]):
        y = bar_start_y + i * 110
        draw_outlined_text(draw, (left_x, y), skill["name"], font_skill_name,
                           fill=PURPLE, outline=(*WHITE_OUTLINE, 180), width=2)
        pct_text = f"{skill['percent']}%"
        draw_outlined_text(draw, (left_x + bar_w + 10, y), pct_text, font_pct,
                           fill=PURPLE_LIGHT, outline=(*WHITE_OUTLINE, 180), width=2)

        bar_y = y + 30
        draw.rounded_rectangle((left_x, bar_y, left_x + bar_w, bar_y + bar_h),
                               radius=bar_h // 2, fill=(255, 255, 255, 160))
        fill_w = int(bar_w * skill["percent"] / 100)
        r, g, b = skill["color"]
        draw.rounded_rectangle((left_x, bar_y, left_x + fill_w, bar_y + bar_h),
                               radius=bar_h // 2, fill=(r, g, b, 210))

        # 进度条圆点
        dot_r = bar_h // 2 + 3
        dot_x = left_x + fill_w
        draw.ellipse([(dot_x - dot_r, bar_y + bar_h // 2 - dot_r),
                      (dot_x + dot_r, bar_y + bar_h // 2 + dot_r)],
                     fill=(r, g, b, 230), outline=(255, 255, 255, 200), width=2)

        draw_outlined_text(draw, (left_x, bar_y + bar_h + 6), skill["desc"],
                           font_skill_desc, fill=PURPLE_MID,
                           outline=(*WHITE_OUTLINE, 180), width=2)

    # --- 右侧：成长路线 ---
    right_x = W // 2 + 100
    draw_outlined_text(draw, (right_x, top_y), "🌱🌸 成长路线", font_section,
                       fill=PURPLE, outline=(*WHITE_OUTLINE, 180), width=2)

    tl_start_y = top_y + 60
    tl_spacing = 110
    line_x = right_x + 85

    for i, item in enumerate(timeline_cfg["items"]):
        y = tl_start_y + i * tl_spacing
        r, g, b = item["color"]

        draw_outlined_text(draw, (right_x, y + 5), item["date"], font_tl_date,
                           fill=PURPLE, outline=(*WHITE_OUTLINE, 180), width=2)

        # 时间线连接线
        if i < len(timeline_cfg["items"]) - 1:
            draw.line([(line_x, y + 28), (line_x, y + tl_spacing)],
                      fill=(180, 140, 170, 180), width=2)

        # 节点
        node_r = 11
        draw.ellipse([(line_x - node_r, y + 8), (line_x + node_r, y + 8 + node_r * 2)],
                     fill=(255, 255, 255, 200), outline=(r, g, b, 220), width=3)
        inner_r = 4
        draw.ellipse([(line_x - inner_r, y + 8 + node_r - inner_r),
                      (line_x + inner_r, y + 8 + node_r + inner_r)],
                     fill=(r, g, b, 220))

        # 标题和描述
        title_x = line_x + 22
        draw_outlined_text(draw, (title_x, y + 2), item["title"], font_tl_title,
                           fill=(r, g, b), outline=(*WHITE_OUTLINE, 180), width=2)
        for j, line in enumerate(item["lines"]):
            draw_outlined_text(draw, (title_x, y + 30 + j * 22), line, font_tl_desc,
                               fill=PURPLE_MID, outline=(*WHITE_OUTLINE, 180), width=2)

    img.convert("RGB").save("assets/skills-timeline.png", quality=95)
    print("  ✅ assets/skills-timeline.png")


# ============================================================
#  4. 生成 README.md
# ============================================================

def generate_readme(cfg):
    """生成完整的 README.md"""
    print("📝 [4/4] 生成 README.md ...")

    gh = cfg["github"]
    about = cfg["about_me"]
    projects = cfg["projects"]
    skills = cfg["skills"]
    activity = cfg["activity"]
    emoji = cfg["style"]["section_emoji"]

    username = gh["username"]
    repo = gh["repo"]
    raw_base = f"https://raw.githubusercontent.com/{username}/{repo}/main"

    lines = []

    # --- Banner ---
    lines.append('<div align="center">')
    lines.append('')
    lines.append(f'<img width="100%" src="{raw_base}/assets/header-banner.png"/>')
    lines.append('')
    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')

    # --- About Me ---
    lines.append(f'### {emoji} About Me')
    lines.append('')
    for item in about:
        lines.append(f'{item["emoji"]} **{item["label"]}:** &ensp; {item["value"]}')
        lines.append('')
    lines.append('---')
    lines.append('')

    # --- 作品展示 ---
    lines.append('<div align="center">')
    lines.append('')
    lines.append(f'### {emoji} {projects["section_title"]}')
    lines.append('')
    lines.append('<br/>')
    lines.append('')

    cards = projects["cards"]
    for i, card in enumerate(cards):
        card_url = f'{raw_base}/assets/projects/card-{i + 1}.png'
        repo_url = f'https://github.com/{username}/{card["repo"]}'
        line = f'<a href="{repo_url}"><img src="{card_url}" width="30%" /></a>'
        # 每行 3 个卡片
        if (i + 1) % 3 == 0:
            lines.append(line)
            lines.append('')
        else:
            lines.append(line + '&ensp;')

    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')

    # --- 技能图谱 ---
    lines.append('<div align="center">')
    lines.append('')
    lines.append(f'### {emoji} {skills["section_title"]}')
    lines.append('')
    lines.append('<br/>')
    lines.append('')
    lines.append(f'<img width="94%" src="{raw_base}/assets/skills-timeline.png"/>')
    lines.append('')
    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')

    # --- 近日足迹 ---
    a = activity
    lines.append('<div align="center">')
    lines.append('')
    lines.append(f'### {emoji} {a["section_title"]}')
    lines.append('')
    lines.append('<br/>')
    lines.append('')
    graph_url = (
        f'https://github-readme-activity-graph.vercel.app/graph'
        f'?username={username}'
        f'&bg_color={a["bg_color"]}'
        f'&color={a["text_color"]}'
        f'&line={a["line_color"]}'
        f'&point={a["point_color"]}'
        f'&area=true&hide_border=true'
        f'&area_color={a["area_color"]}'
    )
    lines.append(f'<img src="{graph_url}" width="94%"/>')
    lines.append('')
    lines.append('</div>')

    readme_content = '\n'.join(lines)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  ✅ README.md")


# ============================================================
#  主入口
# ============================================================

def main():
    print("=" * 56)
    print("  🌸 GitHub Profile Generator")
    print("=" * 56)
    print()

    config_path = sys.argv[1] if len(sys.argv) > 1 else "profile_config.yaml"

    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        print("   请先创建 profile_config.yaml，参考模板修改内容后再运行。")
        sys.exit(1)

    cfg = load_config(config_path)
    print(f"📋 已加载配置: {config_path}")
    print(f"   用户: {cfg['github']['username']}")
    print()

    generate_banner(cfg)
    generate_project_cards(cfg)
    generate_skills_timeline(cfg)
    generate_readme(cfg)

    print()
    print("=" * 56)
    print("  🎉 全部生成完毕！")
    print("=" * 56)
    print()
    print("  接下来推送到 GitHub：")
    print("    git add -A")
    print('    git commit -m "update profile"')
    print("    git push origin main")
    print()


if __name__ == "__main__":
    main()

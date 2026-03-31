# 🌸 GitHub Profile Generator 使用说明

一键生成精美的 GitHub 个人主页，包含**顶部 Banner**、**个人介绍**、**作品卡片**、**技能图谱 + 成长路线**、**活动足迹**五大板块。

## 📁 文件结构

```
github-profile/
├── generate_profile.py      # 🎯 主脚本 — 运行即可生成全部资产
├── profile_config.yaml      # ✏️  配置文件 — 只需改这个文件
├── README.md                # 自动生成的主页
├── assets/
│   ├── header-banner.png    # 自动生成 — 顶部横幅
│   ├── skills-timeline.png  # 自动生成 — 技能+成长路线
│   ├── mitsuri-action.png   # 👤 你的人物图（Banner 用）
│   ├── mitsuri-bg.png       # 👤 你的人物图（技能背景用）
│   └── projects/
│       ├── card-1.png       # 自动生成 — 作品卡片
│       ├── card-2.png
│       └── ...
└── HOW-TO-USE.md            # 本说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install Pillow pyyaml
```

### 2. 准备人物图片

放入 `assets/` 目录：
- **Banner 人物图**（推荐 PNG 透明背景，1024×1024 以上）
- **技能背景图**（推荐 PNG，1200×650 以上）

### 3. 修改配置文件

编辑 `profile_config.yaml`，只需要改文字和图片路径：

```yaml
# 基本信息
github:
  username: "你的GitHub用户名"

# Banner — 改名字和人物图
banner:
  name: "YourName"
  greeting: "Hi, I'm"
  subtitle: "你的一句话介绍"
  character_image: "assets/你的人物图.png"

# 个人介绍 — 改文案
about_me:
  - emoji: "🍁"
    label: "Position"
    value: "你的职位"

# 作品 — 增删改项目
projects:
  cards:
    - name: "项目名"
      desc: "一句话描述"
      tech: "技术栈"
      repo: "仓库名"
      color_top: [245, 180, 195]   # 卡片颜色
      color_bottom: [235, 155, 175]

# 技能 — 改技能和百分比
skills:
  items:
    - name: "技能名"
      percent: 80
      color: [232, 130, 154]
      desc: "关键词描述"

# 成长路线 — 改时间线
timeline:
  items:
    - date: "2025.01"
      title: "里程碑"
      lines: ["第一行", "第二行"]
```

### 4. 一键生成

```bash
python3 generate_profile.py
```

### 5. 推送到 GitHub

```bash
git add -A
git commit -m "update profile"
git push origin main
```

## 🎨 自定义指南

### 修改颜色

配置文件中所有颜色均为 `[R, G, B]` 格式（0-255）：

| 位置 | 配置项 | 说明 |
|------|--------|------|
| Banner 背景 | `banner.gradient_start/end` | 渐变起止色 |
| 作品卡片 | `cards[].color_top/bottom` | 每张卡片渐变色 |
| 技能进度条 | `skills.items[].color` | 进度条颜色 |
| 时间节点 | `timeline.items[].color` | 节点和标题颜色 |
| 技能蒙层 | `skills.overlay_color` | RGBA 蒙层色 |
| 活动图 | `activity.*_color` | 十六进制色值 |

### 修改尺寸

```yaml
style:
  banner_width: 1200    # Banner 宽
  banner_height: 300    # Banner 高
  card_width: 340       # 卡片宽
  card_height: 150      # 卡片高
  skills_width: 1200    # 技能图宽
  skills_height: 650    # 技能图高
```

### 增减作品数量

在 `projects.cards` 列表中增删项目即可，脚本会自动生成对应数量的卡片和 README 布局（每行 3 个）。

### 更换人物

1. 将新的人物图片放入 `assets/`
2. 修改配置中的路径：
   ```yaml
   banner:
     character_image: "assets/新人物.png"
   skills:
     background_image: "assets/新背景.png"
   ```
3. 重新运行 `python3 generate_profile.py`

## ⚠️ 注意事项

- 人物图片推荐使用 **PNG 透明背景**，效果最佳
- GitHub 会剥离 CSS/style 属性，所以所有样式都通过图片生成实现
- 字体使用系统字体，macOS / Linux / Windows 均已做兼容
- 作品卡片圆形图标会自动取项目名第一个字（中英文均支持）

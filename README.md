# 简单计算器 / Simple Calculator

一个用 Python 编写的命令行计算器程序，支持加、减、乘、除运算。

A command-line calculator program written in Python, supporting addition, subtraction, multiplication, and division.

## 使用方法 / Usage

```bash
python main.py
```

按提示输入表达式，例如：

Enter expressions as prompted, e.g.:

```
3 + 4
10 - 2.5
6 * 7
9 / 3
```

输入 `q` 退出程序。Enter `q` to quit.

## 功能 / Features

- 加法 / Addition (`+`)
- 减法 / Subtraction (`-`)
- 乘法 / Multiplication (`*`)
- 除法 / Division (`/`)
- 除零保护 / Division-by-zero protection

---

# SVG 批量排版工具 / SVG Batch Layout Tool

将多个 SVG 文件按网格排列并合并为一个 SVG 文件的命令行工具。

A command-line tool that arranges multiple SVG files in a grid and merges them into a single SVG file.

## 使用方法 / Usage

```bash
# 将目录中所有 SVG 排列成 4 列网格 / Arrange all SVGs in a directory into a 4-column grid
python svg_layout.py icons/ -o output.svg --cols 4

# 指定具体文件 / Specify individual files
python svg_layout.py a.svg b.svg c.svg -o grid.svg --cols 3

# 隐藏文件名标签 / Hide filename labels
python svg_layout.py icons/ -o output.svg --no-labels

# 自定义单元格大小和间距 / Custom cell size and padding
python svg_layout.py icons/ -o output.svg --cell-width 120 --cell-height 120 --padding 20
```

## 参数说明 / Options

| 参数 / Option | 默认值 / Default | 说明 / Description |
|---|---|---|
| `input` | — | SVG 文件或目录 / SVG files or directories |
| `-o / --output` | `output.svg` | 输出文件路径 / Output file path |
| `--cols` | `4` | 列数 / Number of columns |
| `--padding` | `10` | 间距 px / Padding in px |
| `--no-labels` | off | 隐藏文件名标签 / Hide filename labels |
| `--cell-width` | 自动 / auto | 固定格宽 px / Fixed cell width |
| `--cell-height` | 自动 / auto | 固定格高 px / Fixed cell height |

---

# 医院助手 WeChat Mini Program

一款帮助家长**独自带娃就诊**的微信小程序，解决在陌生医院跑上跑下、手忙脚乱的痛点。

A WeChat Mini Program to help parents navigate hospital visits alone with a sick child.

## 功能页面 / Pages

### 🏠 首页 (Home)
- 时间问候、当日日期
- 待办 / 完成任务计数
- 输液进行中横幅（带进度条）
- 四个快捷操作按钮：任务清单、输液计时、添加任务、叫护士

### 📋 任务清单 (Tasks)
- 按「全部 / 待办 / 完成」三栏筛选
- 点击状态圆圈循环切换：待办 → 进行中 → 已完成
- 内置 11 个常用模板（挂号、缴费、抽血、送检、取药、输液…）
- 添加自定义任务，填写任务名 + 就诊地点 + 优先级
- 一键清除已完成任务

### ⏱️ 输液计时 (Infusion Timer)
- 配置袋数（1–5 袋）和每袋时长（分钟）
- 开始 / 暂停 / 继续 / 重置
- 大字倒计时 + 进度条
- 每袋完成后震动提醒，提示护士换药
- 所有袋完成后弹窗提醒护士拔针

## 开发环境 / Setup

1. 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 打开 `miniprogram/` 目录作为小程序项目
3. 在 `project.config.json` 中填入你的 AppID
4. 点击「预览」或「真机调试」

```
miniprogram/
├── app.js / app.json / app.wxss   # 全局逻辑与样式
├── pages/
│   ├── index/    # 首页
│   ├── tasks/    # 任务清单
│   └── infusion/ # 输液计时
└── project.config.json
```